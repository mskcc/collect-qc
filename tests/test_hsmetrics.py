import os
import pytest
import sys


# Import the test data
test_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_file_dir, "files"))
from hsmetrics_test_vars import pass_mean_coverages, warn_error_mean_coverages

# Import Metric from the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_file_dir, "files", "collect-qc-test-data")


def test_mean_target_coverage():
    warn_error_case = metric.hsmetrics(
        operator="threshold",
        operand={"column": "mean_target_coverage", "warn": 700, "error": 500},
    )
    assert os.path.exists("CollectQC_Plots/mean_target_coverage.png")
    # Remove all plots in the CollectQC_Plots folder
    for file in os.listdir("CollectQC_Plots"):
        os.remove(os.path.join("CollectQC_Plots", file))
    os.rmdir("CollectQC_Plots")

    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_warn_error_case = {}
    dict_warn_error_mean_coverages = {}
    for i in range(len(warn_error_case)):
        dict_warn_error_case[warn_error_case[i]["Sample"]] = warn_error_case[i]
    for i in range(len(warn_error_mean_coverages)):
        dict_warn_error_mean_coverages[
            warn_error_mean_coverages[i]["Sample"]
        ] = warn_error_mean_coverages[i]
    assert dict_warn_error_case == dict_warn_error_mean_coverages

    pass_case = metric.hsmetrics(
        operator="threshold",
        operand={"column": "mean_target_coverage", "warn": 200, "error": 100},
    )
    assert os.path.exists("CollectQC_Plots/mean_target_coverage.png")
    # Remove all plots in the CollectQC_Plots folder
    for file in os.listdir("CollectQC_Plots"):
        os.remove(os.path.join("CollectQC_Plots", file))
    os.rmdir("CollectQC_Plots")

    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_pass_case = {}
    dict_pass_mean_coverages = {}
    for i in range(len(pass_case)):
        dict_pass_case[pass_case[i]["Sample"]] = pass_case[i]
    for i in range(len(pass_mean_coverages)):
        dict_pass_mean_coverages[
            pass_mean_coverages[i]["Sample"]
        ] = pass_mean_coverages[i]
    assert dict_pass_case == dict_pass_mean_coverages
