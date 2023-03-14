from metric import Metric
from tabulate import tabulate
from termcolor import colored


def process_metric(metric):
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
                        "operand": operand,
                        "results": insert_size_results,
                    }
                    results.append(results_ops)
                else:
                    print(insert_size_results)
                print("\n")
            elif file_specifier == "hsmetrics":
                print(colored("HsMetrics", attrs=["bold"]))
                hsmetrics_results = metric.hsmetrics(operator=operator, operand=operand)
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
                        "operand": operand,
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

    return results


def summary(results):
    if len(results) == 0:
        print(colored("No results from Collect QC.", color="red", attrs=["bold"]))
        return

    fail = []
    warning = []

    for metric_result in results:
        for sample_data in metric_result["results"]:
            if sample_data["AutoStatus"] == colored(
                "FAIL", color="red", attrs=["bold"]
            ) or sample_data["AutoStatus"] == colored(
                "ERROR", color="red", attrs=["bold"]
            ):
                sample_fail = {}
                sample_fail["AutoStatus"] = sample_data["AutoStatus"]
                sample_fail["Sample"] = sample_data["Sample"]
                sample_fail["Metric"] = metric_result["metric"]
                sample_fail["Function"] = metric_result["operator"]
                sample_fail["Reason"] = sample_data["Reason"]
                fail.append(sample_fail)
            elif sample_data["AutoStatus"] == colored(
                "WARNING", color="yellow", attrs=["bold"]
            ):
                sample_warning = {}
                sample_warning["AutoStatus"] = sample_data["AutoStatus"]
                sample_warning["Sample"] = sample_data["Sample"]
                sample_warning["Metric"] = metric_result["metric"]
                sample_warning["Function"] = metric_result["operator"]
                sample_warning["Reason"] = sample_data["Reason"]
                warning.append(sample_warning)
            else:
                continue

    if len(fail) > 0 and len(warning) > 0:
        print(
            f'{colored("Results:", attrs=["bold"])} {colored("FAILED", color="red", attrs=["bold"])}'
        )
        print("\n")

        print(colored("FAILED", color="red", attrs=["bold"]))
        header = fail[0].keys()
        rows = [sample_data.values() for sample_data in fail]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

        print(colored("WARNING", color="yellow", attrs=["bold"]))
        header = warning[0].keys()
        rows = [sample_data.values() for sample_data in warning]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

    elif len(fail) > 0:
        print(f'Results: {colored("FAILED", color="red", attrs=["bold"])}')
        print("\n")

        print(colored("FAILED", color="red", attrs=["bold"]))
        header = fail[0].keys()
        rows = [sample_data.values() for sample_data in fail]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

    elif len(warning) > 0:
        print(
            f'Results: {colored("Passed with warnings", color="yellow", attrs=["bold"])}'
        )
        print("\n")

        print(colored("WARNING", color="yellow", attrs=["bold"]))
        header = warning[0].keys()
        rows = [sample_data.values() for sample_data in warning]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")
    else:
        print(f'Results: {colored("PASSED", color="green", attrs=["bold"])}')
        print("\n")

    print(colored("config.yaml", attrs=["bold"]))
    print(open("config.yaml").read())

    return


if __name__ == "__main__":
    metric = Metric()
    results = process_metric(metric)
    summary(results)
