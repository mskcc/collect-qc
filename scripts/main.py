from metric import Metric
from tabulate import tabulate
from termcolor import colored


class CollectQC:
    def __init__(self):
        self.metric = Metric()

    def process_metric(self):
        metric = self.metric
        results = []
        config_file = metric.load_config(config_file="config.yaml")

        for file_specifier in config_file["metrics"]:
            metric_functions = config_file["metrics"][file_specifier]
            if metric_functions is None:
                print(
                    colored(
                        f"{file_specifier} is not an available metric.",
                        color="red",
                        attrs=["bold"],
                    )
                )
                return
            for operator in metric_functions["function"]:
                operand = metric_functions["function"][operator]
                if file_specifier == "insert_size":
                    print(colored("Insert Size", attrs=["bold"]))
                    insert_size_results = metric.insert_size(
                        operator=operator, operand=operand
                    )
                    if type(insert_size_results) is list:
                        header = insert_size_results[0].keys()
                        rows = [
                            insert_size_sample_data.values()
                            for insert_size_sample_data in insert_size_results
                        ]
                        print(tabulate(rows, header, tablefmt="simple"))
                        results_ops = {
                            "metric": "insert_size",
                            "operator": operator,
                            "results": insert_size_results,
                        }
                        results.append(results_ops)
                    else:
                        print(insert_size_results)
                    print("\n")
                elif file_specifier == "hsmetrics":
                    print(colored("HsMetrics", attrs=["bold"]))
                    hsmetrics_results = metric.hsmetrics(
                        operator=operator, operand=operand
                    )
                    if type(hsmetrics_results) is list:
                        header = hsmetrics_results[0].keys()
                        rows = [
                            hsmetrics_sample_data.values()
                            for hsmetrics_sample_data in hsmetrics_results
                        ]
                        print(tabulate(rows, header, tablefmt="simple"))
                        results_ops = {
                            "metric": "hsmetrics",
                            "operator": operator,
                            "results": hsmetrics_results,
                        }
                        results.append(results_ops)
                    else:
                        print(hsmetrics_results)
                    print("\n")
                else:
                    print(
                        colored(
                            f"{file_specifier} is not an available metric.",
                            color="red",
                            attrs=["bold"],
                        )
                    )

        self.summary(results)
        return

    def summary(self, results):
        with open("CollectQC_Summary.txt", "w") as f:
            if len(results) == 0:
                f.write("No results from Collect QC.")
                return

            fail = []
            warning = []

            for metric_result in results:
                for sample_data in metric_result["results"]:
                    if sample_data["AutoStatus"] == colored(
                        "FAIL", color="red", attrs=["bold"]
                    ):
                        sample_fail = {}
                        sample_fail["AutoStatus"] = "FAIL"
                        sample_fail["Sample"] = sample_data["Sample"]
                        sample_fail["Metric"] = metric_result["metric"]
                        sample_fail["Function"] = metric_result["operator"]
                        sample_fail["Reason"] = sample_data["Reason"]
                        fail.append(sample_fail)
                    elif sample_data["AutoStatus"] == colored(
                        "ERROR", color="red", attrs=["bold"]
                    ):
                        sample_fail = {}
                        sample_fail["AutoStatus"] = "ERROR"
                        sample_fail["Sample"] = sample_data["Sample"]
                        sample_fail["Metric"] = metric_result["metric"]
                        sample_fail["Function"] = metric_result["operator"]
                        sample_fail["Reason"] = sample_data["Reason"]
                        fail.append(sample_fail)
                    elif sample_data["AutoStatus"] == colored(
                        "WARNING", color="yellow", attrs=["bold"]
                    ):
                        sample_warning = {}
                        sample_warning["AutoStatus"] = "WARNING"
                        sample_warning["Sample"] = sample_data["Sample"]
                        sample_warning["Metric"] = metric_result["metric"]
                        sample_warning["Function"] = metric_result["operator"]
                        sample_warning["Reason"] = sample_data["Reason"]
                        warning.append(sample_warning)
                    else:
                        continue

            if len(fail) > 0 and len(warning) > 0:
                f.write(f"Results: FAILED \n \n")

                f.write("FAILED \n")
                header = fail[0].keys()
                rows = [sample_data.values() for sample_data in fail]
                f.write(tabulate(rows, header, tablefmt="simple"))
                f.write("\n \n")

                f.write("WARNING \n")
                header = warning[0].keys()
                rows = [sample_data.values() for sample_data in warning]
                f.write(tabulate(rows, header, tablefmt="simple"))
                f.write("\n \n")

            elif len(fail) > 0:
                f.write("Results: FAILED \n \n")

                f.write("FAILED \n")
                header = fail[0].keys()
                rows = [sample_data.values() for sample_data in fail]
                f.write(tabulate(rows, header, tablefmt="simple"))
                f.write("\n \n")

            elif len(warning) > 0:
                f.write("Results: Passed with warnings \n \n")

                f.write("WARNING \n")
                header = warning[0].keys()
                rows = [sample_data.values() for sample_data in warning]
                f.write(tabulate(rows, header, tablefmt="simple"))
                f.write("\n \n")
            else:
                f.write("Results: PASSED \n \n")

            f.write("\nconfig.yaml \n")
            f.write(open("config.yaml").read())

        return


if __name__ == "__main__":
    qc = CollectQC()
    qc.process_metric()
