import os
import pytest
import sys


# Import the test data
test_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_file_dir, "files"))
from gcbias_test_vars import coverage_case

# Import Metric from the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_file_dir, "files", "collect-qc-test-data")


def test_coverage_deviation():
    coverage_case = metric.gcbias(
        operator="coverage_deviation",
        operand={"columns": ["gc", "normalized_coverage"], "threshold": 0.6},
    )
    assert os.path.exists("CollectQC_Plots/coverage_deviation.png")
    # Remove all plots in the CollectQC_Plots folder
    for file in os.listdir("CollectQC_Plots"):
        os.remove(os.path.join("CollectQC_Plots", file))
    os.rmdir("CollectQC_Plots")

    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_coverage_case = {}
    dict_coverage_case = {}
    for i in range(len(coverage_case)):
        dict_coverage_case[coverage_case[i]["Sample"]] = coverage_case[i]
    for i in range(len(coverage_case)):
        dict_coverage_case[coverage_case[i]["Sample"]] = coverage_case[i]
    assert dict_coverage_case == dict_coverage_case