from termcolor import colored
from metric import Metric
from tabulate import tabulate


def process_metric(metric):
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

    return


if __name__ == "__main__":
    metric = Metric()
    process_metric(metric)
