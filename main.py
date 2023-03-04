from termcolor import colored
from metric import Metric


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
                print(colored("insert_size", attrs=["bold", "underline"]))
                print(metric.insert_size(operator=operator, operand=operand))
                print("\n")
            elif file_specifier == "hsmetrics":
                print(colored("hsmetrics", attrs=["bold", "underline"]))
                hsmetrics_results = metric.hsmetrics(operator=operator, operand=operand)
                if type(hsmetrics_results) is list:
                    for hsmetric_result in hsmetrics_results:
                        if type(hsmetric_result) is dict:
                            print(
                                f'{hsmetric_result["autostatus"]} {hsmetric_result["sample"]} Mean Target Coverage: {hsmetric_result["coverage"]}'
                            )
                        else:
                            print(hsmetric_result)
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
