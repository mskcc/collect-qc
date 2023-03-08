import os
import pytest
import sys
from termcolor import colored


# Import the test data
test_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_file_dir, "files", "hsmetrics"))
from hsmetrics_test_vars import pass_mean_coverages, warn_error_mean_coverages

# Import Metric from the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_file_dir, "files", "hsmetrics", "hsmetrics_test_data")


def test_mean_target_coverage():
    warn_error_case = metric.hsmetrics(
        operator="threshold",
        operand={"column": "mean_target_coverage", "warn": 700, "error": 500},
    )
    assert warn_error_case == warn_error_mean_coverages

    pass_case = metric.hsmetrics(
        operator="threshold",
        operand={"column": "mean_target_coverage", "warn": 200, "error": 100},
    )
    assert pass_case == pass_mean_coverages
