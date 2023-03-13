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
                        insert_size_sample.values()
                        for insert_size_sample in insert_size_results
                    ]
                    print(tabulate(rows, header, tablefmt="simple"))
                    results.append(insert_size_results)
                else:
                    print(insert_size_results)
                print("\n")
            elif file_specifier == "hsmetrics":
                print(colored("HsMetrics", attrs=["bold"]))
                hsmetrics_results = metric.hsmetrics(operator=operator, operand=operand)
                if type(hsmetrics_results) is list:
                    header = hsmetrics_results[0].keys()
                    rows = [
                        hsmetrics_sample.values()
                        for hsmetrics_sample in hsmetrics_results
                    ]
                    print(tabulate(rows, header, tablefmt="simple"))
                    results.append(hsmetrics_results)
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


def summary(results, config):
    fail = []
    warning = []
    # TODO: Add function, metric, and reason to the dictionaries when appending to fail and warning
    for result in results:
        for sample in result:
            if sample["AutoStatus"] == colored("FAIL", color="red", attrs=["bold"]):
                fail.append(sample)
            elif sample["AutoStatus"] == colored("ERROR", color="red", attrs=["bold"]):
                fail.append(sample)
            elif sample["AutoStatus"] == colored(
                "WARNING", color="yellow", attrs=["bold"]
            ):
                warning.append(sample)
            else:
                continue

    if len(fail) > 0 and len(warning) > 0:
        print(
            f'{colored("Results:", attrs=["bold"])} {colored("Failed", color="red", attrs=["bold"])}'
        )
        print("\n")

        print(colored("FAILED", color="red", attrs=["bold"]))
        header = fail[0].keys()
        rows = [sample.values() for sample in fail]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

        print(colored("WARNING", color="yellow", attrs=["bold"]))
        header = warning[0].keys()
        rows = [sample.values() for sample in warning]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

    elif len(fail) > 0:
        print(f'Results: {colored("Failed", color="red", attrs=["bold"])}')
        print("\n")

        print(colored("FAILED", color="red", attrs=["bold"]))
        header = fail[0].keys()
        rows = [sample.values() for sample in fail]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")

    elif len(warning) > 0:
        print(
            f'Results: {colored("Passed with warnings", color="yellow", attrs=["bold"])}'
        )
        print("\n")

        print(colored("WARNING", color="yellow", attrs=["bold"]))
        header = warning[0].keys()
        rows = [sample.values() for sample in warning]
        print(tabulate(rows, header, tablefmt="simple"))
        print("\n")
    else:
        print(f'Results: {colored("Passed", color="green", attrs=["bold"])}')
        print("\n")

    print(colored("config.yaml", attrs=["bold"]))
    print(open("config.yaml").read())

    return


if __name__ == "__main__":
    metric = Metric()
    results = process_metric(metric)
    summary(results, config=metric.config)
