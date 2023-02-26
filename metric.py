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
                        peak_amt = len(peaks[0])
                        if peak_amt == 1:
                            insert_size_data.append(
                                f'{colored("PASS", color="green", attrs=["bold"])} {run_file.split(".")[0]}, peaks: {len(peaks[0])}, max_peak: {max_peak}'
                            )
                        else:
                            insert_size_data.append(
                                f'{colored("FAIL", color="red", attrs=["bold"])} {run_file.split(".")[0]}, peaks: {len(peaks[0])}, max_peak: {max_peak}'
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
        else:
            return f"{self.operator} is not an available function."

    def table(self, data):
        cols = []
        # Convert from 1-based to 0-based indexing
        if self.operand["columns"]:
            for i in range(0, len(self.operand["columns"])):
                cols.append(self.operand["columns"][i] - 1)

            return data.iloc[:, cols]
        else:
            return data
