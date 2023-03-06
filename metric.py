from termcolor import colored
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from scipy.signal import find_peaks
import yaml


class Metric:
    def __init__(self):
        self.config = None
        self.qc_folder = None

    def load_config(self, config_file):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        self.qc_folder = os.path.join(os.getcwd(), self.config["qc_folder"])
        if not os.path.exists("plots"):
            os.mkdir("plots")
        return self.config

    def hsmetrics(self, operator, operand):
        runs = os.listdir(self.qc_folder)
        hsmetrics_data = []
        for run in runs:
            run_path = os.path.join(self.qc_folder, run)
            for run_file in os.listdir(run_path):
                if run_file.endswith(".hsmetrics"):
                    with open(os.path.join(run_path, run_file)) as f:
                        hsmetrics_row1_flag = False
                        hsmetrics_row2_flag = False
                        for line in f:
                            if line.startswith("## METRICS CLASS"):
                                hsmetrics_row1_flag = True
                            elif hsmetrics_row1_flag:
                                hsmetrics_row1 = line
                                hsmetrics_row1_flag = False
                                hsmetrics_row2_flag = True
                            elif hsmetrics_row2_flag:
                                hsmetrics_row2 = line
                                hsmetrics_row2_flag = False
                                break
                        # Index out MEAN_TARGET_COVERAGE
                        hsmetrics_row1 = hsmetrics_row1.split("\t")
                        hsmetrics_row2 = hsmetrics_row2.split("\t")
                        mean_target_coverage_idx = hsmetrics_row1.index(
                            "MEAN_TARGET_COVERAGE"
                        )
                        mean_target_coverage = float(
                            hsmetrics_row2[mean_target_coverage_idx]
                        )

                        if operator == "mean_target_coverage":
                            if operand["warn"] and operand["error"]:
                                if operand["warn"] == operand["error"]:
                                    return colored(
                                        '"warn" and "error" cannot be the same value."',
                                        color="red",
                                        attrs=["bold"],
                                    )
                                elif operand["warn"] < operand["error"]:
                                    return colored(
                                        '"warn" cannot be less than "error".',
                                        color="red",
                                        attrs=["bold"],
                                    )
                                else:
                                    pass
                            else:
                                return colored(
                                    '"warn" and/or "error" not specified in the config file.',
                                    color="red",
                                    attrs=["bold"],
                                )
                        else:
                            return colored(
                                "Incorrect function specified in the config file.",
                                color="red",
                                attrs=["bold"],
                            )
                        fun = Function(operator, operand)
                        sample_cov = fun(mean_target_coverage)
                        hsmetrics_data.append(
                            f"{sample_cov} {run_file.split('.')[0]} Mean Target Coverage: {mean_target_coverage}"
                        )

        hsmetrics_out = "\n".join(hsmetrics_data)
        return hsmetrics_out

    def insert_size(self, operator, operand):
        runs = os.listdir(self.qc_folder)
        insert_size_data = []
        fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=True)
        x_lim = float("inf")
        for run in runs:
            run_path = os.path.join(self.qc_folder, run)
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
                            return colored(
                                f"Incorrect columns specified in the config file.",
                                color="red",
                                attrs=["bold"],
                            )
                        fun = Function(operator, {"columns": [1, 2]})
                        tab_data = fun(hist_data)
                        tab_data = tab_data.rename(
                            {
                                tab_data.columns[0]: "insert_size",
                                tab_data.columns[1]: run_file.split(".")[0],
                            },
                            axis=1,
                        )
                        peak_data = tab_data.iloc[:, 1]

                        max_peak_idx = peak_data.idxmax()
                        max_peak = tab_data.iloc[:, 0].iloc[max_peak_idx]
                        legend_label = f'{run_file.split(".")[0]} Peak: {max_peak}'
                        sns.lineplot(
                            data=tab_data,
                            x=tab_data.columns[0],
                            y=tab_data.columns[1],
                            ax=ax,
                            label=legend_label,
                        )
                        x_lim = min(x_lim, tab_data.iloc[:, 0].max())

                        peaks = find_peaks(
                            peak_data, height=max_peak / 3, distance=10, width=10
                        )
                        peak_amt = len(peaks[0])
                        if peak_amt == 1:
                            insert_size_data.append(
                                f'{colored("PASS", color="green", attrs=["bold"])} {run_file.split(".")[0]}, Peaks: {len(peaks[0])}, Max Peak: {max_peak}'
                            )
                        else:
                            insert_size_data.append(
                                f'{colored("FAIL", color="red", attrs=["bold"])} {run_file.split(".")[0]}, Peaks: {len(peaks[0])}, Max Peak: {max_peak}'
                            )
        ax.set_facecolor("#eeeeee")
        plt.ylabel("")
        plt.xlabel("Insert Size")
        plt.xlim(0, round(x_lim / 100) * 100)
        plt.grid()
        plt.tight_layout(pad=3)
        plt.title("Insert Size Distribution", loc="left", fontsize=20)
        plt.savefig("plots/insert_size.png")
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
            return colored(
                f"{self.operator} is not an available function.",
                color="red",
                attrs=["bold"],
            )

    def mean_target_coverage(self, data):
        warn = self.operand["warn"]
        error = self.operand["error"]

        if data > warn:
            return colored("PASS", "green", attrs=["bold"])
        elif data > error and data <= warn:
            return colored("WARNING", "yellow", attrs=["bold"])
        elif data <= error:
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
