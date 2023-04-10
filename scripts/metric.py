from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
from scipy.signal import find_peaks
import seaborn as sns
from termcolor import colored
import yaml


class Metric:
    def __init__(self):
        self.config = None
        self.qc_folder = None

    def load_config(self, config_file):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        self.qc_folder = os.path.join(os.getcwd(), self.config["qc_folder"])
        return self.config

    def concordance(self, operator, operand):
        runs = os.listdir(self.qc_folder)
        concordance_data = []
        for run in runs:
            run_path = os.path.join(self.qc_folder, run)
            for run_file in os.listdir(run_path):
                if run_file.endswith("_concordance.txt"):
                    concord_file = open(os.path.join(run_path, run_file))
                    concord_data = pd.read_csv(concord_file, sep="\t")
                    patient_N_full = concord_data.loc[:, "concordance"].iloc[0]
                    patient_N = re.search(r"Patient_(\d+)", patient_N_full).group()
                    filter_match_data = concord_data.filter(regex=patient_N)
                    match_data = pd.concat(
                        [concord_data.iloc[:, 0], filter_match_data], axis=1
                    )
                    unmatch_data = concord_data.filter(
                        regex="^((?!" + patient_N + ").)*$"
                    )

                    if operator == "match_sample_matrix":
                        # Error handling for missing operand keys and the threshold values
                        if operand.keys() == {
                            "match_error_lt",
                            "match_warn_lt",
                            "unmatch_warn_gt",
                            "unmatch_error_gt",
                        }:
                            if operand["match_error_lt"] == operand["match_warn_lt"]:
                                return colored(
                                    '"match_error_lt" and "match_warn_lt" cannot be the same value."',
                                    color="red",
                                    attrs=["bold"],
                                )
                            elif operand["match_error_lt"] > operand["match_warn_lt"]:
                                return colored(
                                    '"match_error_lt" must be less than "match_warn_lt".',
                                    color="red",
                                    attrs=["bold"],
                                )
                            elif (
                                operand["unmatch_warn_gt"]
                                == operand["unmatch_error_gt"]
                            ):
                                return colored(
                                    '"unmatch_warn_gt" and "unmatch_error_gt" cannot be the same value."',
                                    color="red",
                                    attrs=["bold"],
                                )
                            elif (
                                operand["unmatch_warn_gt"] > operand["unmatch_error_gt"]
                            ):
                                return colored(
                                    '"unmatch_warn_gt" must be greater than "unmatch_error_gt".',
                                    color="red",
                                    attrs=["bold"],
                                )
                        else:
                            return colored(
                                "The match_sample_matrix function requires the following thresholds: 'match_error_lt', 'match_warn_lt', 'unmatch_warn_gt', and 'unmatch_error_gt'.",
                                color="red",
                                attrs=["bold"],
                            )

                        # Call the match_sample_matrix function
                        fun = Function("match_sample_matrix", operand)
                        data = {"match": match_data, "unmatch": unmatch_data}
                        (
                            match_error_cols,
                            match_warn_cols,
                            unmatch_error_cols,
                            unmatch_warn_cols,
                        ) = fun(data)

                        # Plot a heatmap of concord_data
                        fig, ax = plt.subplots(
                            figsize=(20, 10), sharex=True, sharey=True
                        )
                        concord_data.set_index("concordance", inplace=True)
                        sns.heatmap(
                            concord_data.transpose(),
                            cmap="RdYlGn",
                            ax=ax,
                            cbar_kws={"label": "Percent Concordance"},
                        )
                        ax.grid(False)
                        fig.tight_layout(pad=16)
                        ax.set_title("Concordance among Samples", loc="left", fontsize=20)
                        ax.set_xlabel("Normal Sample", labelpad=10)
                        ax.set_ylabel("Tumor Samples", labelpad=10)
                        plt.yticks(rotation=0)

                        if not os.path.exists("CollectQC_Plots"):
                            os.mkdir("CollectQC_Plots")
                        fig.savefig(
                            f"CollectQC_Plots/concordance_{patient_N_full}.png",
                            bbox_inches="tight",
                        )

                        if match_warn_cols:
                            concordance_data.append(
                                {
                                    "AutoStatus": colored(
                                        "WARNING", color="yellow", attrs=["bold"]
                                    ),
                                    "Sample": patient_N_full,
                                    "Reason": f"{', '.join(match_warn_cols)} fell within the {operand['match_error_lt']} and {operand['match_warn_lt']} match thresholds.",
                                }
                            )
                        if match_error_cols:
                            concordance_data.append(
                                {
                                    "AutoStatus": colored(
                                        "ERROR", color="red", attrs=["bold"]
                                    ),
                                    "Sample": patient_N_full,
                                    "Reason": f"{', '.join(match_error_cols)} fell below the {operand['match_error_lt']} match threshold.",
                                }
                            )
                        if unmatch_warn_cols:
                            concordance_data.append(
                                {
                                    "AutoStatus": colored(
                                        "WARNING", color="yellow", attrs=["bold"]
                                    ),
                                    "Sample": patient_N_full,
                                    "Reason": f"{', '.join(unmatch_warn_cols)} fell within the {operand['unmatch_warn_gt']} and {operand['unmatch_error_gt']} mismatch thresholds.",
                                }
                            )
                        if unmatch_error_cols:
                            concordance_data.append(
                                {
                                    "AutoStatus": colored(
                                        "ERROR", color="red", attrs=["bold"]
                                    ),
                                    "Sample": patient_N_full,
                                    "Reason": f"{', '.join(unmatch_error_cols)} exceeded the {operand['unmatch_error_gt']} mismatch threshold.",
                                }
                            )
                    else:
                        return colored(
                            f'"{operator}" is not a valid operator for "concordance".',
                            color="red",
                            attrs=["bold"],
                        )

        return concordance_data

    def gcbias(self, operator, operand):
        def gcBin(df):
            gc_bin_list = np.arange(0.3, 0.9, 0.05)
            gc_dict = {}
            nc_dict = {}
            first_bin = gc_bin_list[0]
            for single_bin in gc_bin_list:
                gc_dict[single_bin] = []
                nc_dict[single_bin] = []
            for gc, norm_coverage in zip(df["%gc"], df["normalized_coverage"]):
                added_to_bin = False
                for single_bin in np.flip(gc_bin_list):
                    if gc >= single_bin and not added_to_bin:
                        gc_dict[single_bin].append(gc)
                        nc_dict[single_bin].append(norm_coverage)
                        added_to_bin = True
                if not added_to_bin:
                    gc_dict[first_bin].append(gc)
                    nc_dict[first_bin].append(norm_coverage)
                gc_data = []
            nc_data = []
            for single_bin in gc_bin_list:
                if gc_dict[single_bin] != [] and nc_dict[single_bin] != []:
                    gc_data.append(np.mean(gc_dict[single_bin]))
                    nc_data.append(np.mean(nc_dict[single_bin]))
            gc_bin_data = {"%gc": gc_data, "normalized_coverage": nc_data}
            gc_df = pd.DataFrame(gc_bin_data)
            return gc_df

        runs = os.listdir(self.qc_folder)
        gcbias_data = []
        fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=True)
        for run in runs:
            run_path = os.path.join(self.qc_folder, run)
            for run_file in os.listdir(run_path):
                if run_file.endswith(".hstmetrics"):
                    gcbias_file = open(os.path.join(run_path, run_file))
                    gcbias_df = pd.read_csv(gcbias_file, sep="\t")

                    if operator == "coverage_deviation":
                        if operand["columns"] and operand["threshold"]:
                            if set(operand["columns"]) != {
                                "gc",
                                "normalized_coverage",
                            }:
                                return colored(
                                    f'The "columns" parameter must be set to [gc, normalized_coverage].',
                                    color="red",
                                    attrs=["bold"],
                                )
                            else:
                                binned = gcBin(gcbias_df)
                                fun = Function("coverage_deviation", operand)
                                fun_input = {
                                    "df": binned,
                                    "threshold": operand["threshold"],
                                    "columns": ["%gc", "normalized_coverage"],
                                }
                                cov_dev = fun(fun_input)
                                if cov_dev["AutoStatus"] == colored(
                                    "FAIL", color="red", attrs=["bold"]
                                ):
                                    gcbias_data.append(
                                        {
                                            "AutoStatus": cov_dev["AutoStatus"],
                                            "Sample": run_file.split(".")[0],
                                            "Reason": f'The coverage deviation of {cov_dev["auc"]} is greater than the {operand["threshold"]} threshold.',
                                        }
                                    )
                                elif cov_dev["AutoStatus"] == colored(
                                    "PASS", color="green", attrs=["bold"]
                                ):
                                    gcbias_data.append(
                                        {
                                            "AutoStatus": cov_dev["AutoStatus"],
                                            "Sample": run_file.split(".")[0],
                                            "Reason": "",
                                        }
                                    )
                                else:
                                    return colored(
                                        f'"Invalid result for "coverage_deviation".',
                                        color="red",
                                        attrs=["bold"],
                                    )

                                legend_label = (
                                    f'{run_file.split(".")[0]}'
                                )
                                sns.lineplot(
                                    data=binned,
                                    x="%gc",
                                    y="normalized_coverage",
                                    ax=ax,
                                    label=legend_label,
                                )
                        else:
                            return colored(
                                "The coverage_deviation function requires the following inputs: 'columns' and 'threshold'.",
                                color="red",
                                attrs=["bold"],
                            )
                    else:
                        return colored(
                            f'"{operator}" is not a valid function for "gcbias".',
                            color="red",
                            attrs=["bold"],
                        )

        if operator == "coverage_deviation":
            ax.set_facecolor("#eeeeee")
            ax.set_ylabel("Normalized Coverage", labelpad=10, fontsize=12)
            ax.set_xlabel("GC Content", labelpad=10, fontsize=12)
            ax.grid()
            fig.tight_layout(pad=3)
            ax.set_title("Normalized Coverage vs GC-Content", loc="left", fontsize=20)
            if not os.path.exists("CollectQC_Plots"):
                os.mkdir("CollectQC_Plots")
            fig.savefig(
                "CollectQC_Plots/coverage_deviation.png",
                bbox_inches="tight",
            )

        return gcbias_data

    def hsmetrics(self, operator, operand):
        runs = os.listdir(self.qc_folder)
        hsmetrics_data = []
        fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=True)
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

                        if operator == "threshold":
                            if operand["column"] == "mean_target_coverage":
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
                                        fun = Function(
                                            "mean_target_coverage",
                                            operand,
                                        )
                                        sample_cov = fun(mean_target_coverage)
                                        if sample_cov == colored(
                                            "ERROR", color="red", attrs=["bold"]
                                        ):
                                            reason = f'Mean Target Coverage of {mean_target_coverage} fell below the {operand["error"]} threshold.'
                                        elif sample_cov == colored(
                                            "WARNING", color="yellow", attrs=["bold"]
                                        ):
                                            reason = f'Mean Target Coverage of {mean_target_coverage} fell below the {operand["warn"]} threshold.'
                                        else:
                                            reason = ""
                                        hsmetrics_data.append(
                                            {
                                                "AutoStatus": sample_cov,
                                                "Sample": run_file.split(".")[0],
                                                "Mean Target Coverage": mean_target_coverage,
                                                "Reason": reason,
                                            }
                                        )
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
                        else:
                            return colored(
                                "Incorrect function specified in the config file.",
                                color="red",
                                attrs=["bold"],
                            )

        # Make plots
        if operand["column"] == "mean_target_coverage":
            sns.barplot(
                data=pd.DataFrame(hsmetrics_data),
                x="Sample",
                y="Mean Target Coverage",
                zorder=2,
                ax=ax,
                color="#616161",
            )
            plt.axhline(y=operand["warn"], color="yellow", linestyle="-", zorder=2)
            plt.axhline(y=operand["error"], color="red", linestyle="-", zorder=2)
            ax.set_facecolor("#eeeeee")
            ax.grid(zorder=0)
            fig.tight_layout(pad=3)
            ax.set_title("Mean Target Coverage", loc="left", fontsize=20)
            ax.set_ylabel("Mean Coverage")
            ax.set_xlabel("")

            if not os.path.exists("CollectQC_Plots"):
                os.mkdir("CollectQC_Plots")
            fig.savefig("CollectQC_Plots/mean_target_coverage.png")

        return hsmetrics_data

    def insert_size(self, operator, operand):
        runs = os.listdir(self.qc_folder)
        insert_size_data = []
        fig, ax = plt.subplots(figsize=(20, 10), sharex=True, sharey=True)
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

                        if operator == "peak_analysis":
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

                            peaks = find_peaks(
                                peak_data, height=max_peak / 3, distance=10, width=10
                            )
                            peak_amt = len(peaks[0])
                            if peak_amt == 1:
                                insert_size_data.append(
                                    {
                                        "AutoStatus": colored(
                                            "PASS", color="green", attrs=["bold"]
                                        ),
                                        "Sample": run_file.split(".")[0],
                                        "Peaks": peak_amt,
                                        "Max Peak": max_peak,
                                        "Reason": "",
                                    }
                                )
                            else:
                                insert_size_data.append(
                                    {
                                        "AutoStatus": colored(
                                            "FAIL", color="red", attrs=["bold"]
                                        ),
                                        "Sample": run_file.split(".")[0],
                                        "Peaks": peak_amt,
                                        "Max Peak": max_peak,
                                        "Reason": f"{peak_amt} peaks detected. Expected 1 peak.",
                                    }
                                )
                        else:
                            return colored(
                                "Incorrect function specified in the config file.",
                                color="red",
                                attrs=["bold"],
                            )

        if operator == "peak_analysis":
            ax.set_facecolor("#eeeeee")
            ax.set_ylabel("")
            ax.set_xlabel("Insert Size")
            ax.grid()
            fig.tight_layout(pad=3)
            ax.set_title("Insert Size Distribution", loc="left", fontsize=20)
            if not os.path.exists("CollectQC_Plots"):
                os.mkdir("CollectQC_Plots")
            fig.savefig("CollectQC_Plots/insert_size.png")

        return insert_size_data


class Function:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __call__(self, data):
        if self.operator == "coverage_deviation":
            return self.coverage_deviation(data)
        elif self.operator == "match_sample_matrix":
            return self.match_sample_matrix(data)
        elif self.operator == "mean_target_coverage":
            return self.mean_target_coverage(data)
        elif self.operator == "peak_analysis":
            return self.peak_analysis(data)
        else:
            return colored(
                f"{self.operator} is not an available function.",
                color="red",
                attrs=["bold"],
            )

    def coverage_deviation(self, data):
        df = data["df"]

        auc = np.trapz(x=df.loc[:, "%gc"], y=df.loc[:, "normalized_coverage"])
        if auc > data["threshold"]:
            return {
                "AutoStatus": colored("FAIL", color="red", attrs=["bold"]),
                "auc": round(auc, 3),
            }
        else:
            return {
                "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
                "auc": round(auc, 3),
            }

    def match_sample_matrix(self, data):
        match_data = data["match"]
        unmatch_data = data["unmatch"]
        match_warn = self.operand["match_warn_lt"]
        match_error = self.operand["match_error_lt"]
        unmatch_warn = self.operand["unmatch_warn_gt"]
        unmatch_error = self.operand["unmatch_error_gt"]

        match_error_cols = (
            match_data.iloc[:, 1:]
            .where(match_data.iloc[:, 1:] < match_error)
            .dropna(axis=1)
            .columns.tolist()
        )
        match_warn_cols = (
            match_data.iloc[:, 1:]
            .where(
                (match_data.iloc[:, 1:] < match_warn)
                & (match_data.iloc[:, 1:] >= match_error)
            )
            .dropna(axis=1)
            .columns.tolist()
        )

        unmatch_error_cols = (
            unmatch_data.iloc[:, 1:]
            .where(unmatch_data.iloc[:, 1:] >= unmatch_error)
            .dropna(axis=1)
            .columns.tolist()
        )
        unmatch_warn_cols = (
            unmatch_data.iloc[:, 1:]
            .where(
                (unmatch_data.iloc[:, 1:] >= unmatch_warn)
                & (unmatch_data.iloc[:, 1:] < unmatch_error)
            )
            .dropna(axis=1)
            .columns.tolist()
        )

        return match_error_cols, match_warn_cols, unmatch_error_cols, unmatch_warn_cols

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

    def peak_analysis(self, data):
        cols = []
        # Convert from 1-based to 0-based indexing
        if self.operand["columns"]:
            for i in range(0, len(self.operand["columns"])):
                cols.append(self.operand["columns"][i] - 1)

            return data.iloc[:, cols]
        else:
            return data
