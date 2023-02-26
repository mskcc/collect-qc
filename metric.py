from colorama import just_fix_windows_console

just_fix_windows_console()
from termcolor import colored
from io import StringIO
import os
import pandas as pd
from scipy.signal import find_peaks
import yaml


class Metric:
    def __init__(self):
        self.config = None
        self.qc_data_path = None

    def load_config(self, config_file):
        with open(config_file) as f:
            config = yaml.safe_load(f)
        self.qc_data_path = config["qc_data_path"]
        return config

    def hsmetric(self, operator, operand):
        runs = os.listdir(self.qc_data_path)
        hsmetric_data = []
        for run in runs:
            run_path = os.path.join(self.qc_data_path, run)
            for run_file in os.listdir(run_path):
                if run_file.endswith(".hsmetrics"):
                    with open(os.path.join(run_path, run_file)) as f:
                        hsmetric_row1_flag = False
                        hsmetric_row2_flag = False
                        for line in f:
                            if line.startswith("## METRICS CLASS"):
                                hsmetric_row1_flag = True
                            elif hsmetric_row1_flag:
                                hsmetric_row1 = line
                                hsmetric_row1_flag = False
                                hsmetric_row2_flag = True
                            elif hsmetric_row2_flag:
                                hsmetric_row2 = line
                                hsmetric_row2_flag = False
                                break
                        # Index out MEAN_TARGET_COVERAGE
                        hsmetric_row1 = hsmetric_row1.split("\t")
                        hsmetric_row2 = hsmetric_row2.split("\t")
                        mean_target_coverage_idx = hsmetric_row1.index(
                            "MEAN_TARGET_COVERAGE"
                        )
                        mean_target_coverage = float(
                            hsmetric_row2[mean_target_coverage_idx]
                        )

                        fun = Function(operator, operand)
                        sample_cov = fun(mean_target_coverage)
                        hsmetric_data.append(
                            f"{sample_cov} {run_file.split('.')[0]} Mean Target Coverage: {mean_target_coverage}"
                        )

        hsmetric_out = "\n".join(hsmetric_data)
        return hsmetric_out

    def insert_size(self, operator, operand):
        runs = os.listdir(self.qc_data_path)
        insert_size_data = []
        for run in runs:
            run_path = os.path.join(self.qc_data_path, run)
            for run_file in os.listdir(run_path):
                if run_file.endswith(".ismetrics"):
                    with open(os.path.join(run_path, run_file)) as f:
                        hist_flag = False
                        hist = []
                        for line in f:
                            if line.startswith("## HISTOGRAM"):
                                hist_flag = True
                            elif hist_flag:
                                hist.append(line)

                        hist_data = pd.read_csv(StringIO("\n".join(hist)), sep="\t")
                        if set(operand["columns"]) != {1, 2}:
                            return f"Incorrect columns specified in the config file."
                        fun = Function(operator, {"columns": [1, 2]})
                        tab_data = fun(hist_data)
                        peak_data = tab_data.iloc[:, 1]
                        max_peak_idx = peak_data.idxmax()
                        max_peak = tab_data.iloc[:, 0].iloc[max_peak_idx]
                        peaks = find_peaks(
                            peak_data, height=max_peak / 3, distance=10, width=10
                        )
                        insert_size_data.append(
                            f'{run_file.split(".")[0]}, peaks: {len(peaks[0])}, max_peak: {max_peak}'
                        )
        insert_size_out = "\n".join(insert_size_data)

        return insert_size_out


class Function:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __call__(self, data):
        if self.operator == "table":
            return self.table(data)
        elif self.operator == "mean_target_coverage":
            return self.mean_target_coverage(data)
        else:
            return f"{self.operator} is not an available function."

    def mean_target_coverage(self, data):
        warn = self.operand["warn"]
        error = self.operand["error"]

        if data > warn:
            return colored("PASS", "green", attrs=["bold"])
        elif data > error and data <= warn:
            return colored("WARNING", "yellow", attrs=["bold"])
        elif data < error:
            return colored("ERROR", "red", attrs=["bold"])
        else:
            return colored(
                "Mean target coverage could not be determined", "red", attrs=["bold"]
            )

    def table(self, data):
        cols = []
        # Convert from 1-based to 0-based indexing
        if self.operand["columns"]:
            for i in range(0, len(self.operand["columns"])):
                cols.append(self.operand["columns"][i] - 1)

            return data.iloc[:, cols]
        else:
            return data
