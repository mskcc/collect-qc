from termcolor import colored
from metric import Metric


def process_metric(metric):
    config_file = metric.load_config(config_file="config.yaml")

    for file_specifier in config_file["metrics"]:
        metric_functions = config_file["metrics"][file_specifier]
        if metric_functions is None:
            print(f"{file_specifier} is not an available metric.")
            return
        for operator in metric_functions["function"]:
            operand = metric_functions["function"][operator]
            if file_specifier == "insert_size":
                print(colored("insert_size", attrs=["bold"]))
                print(metric.insert_size(operator=operator, operand=operand))
            else:
                print(f"{file_specifier} is not an available metric.")

    return


if __name__ == "__main__":
    metric = Metric()
    process_metric(metric)
