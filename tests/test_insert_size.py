import os
import pytest
import sys


# Import the test data
test_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_file_dir, "files"))
from insert_size_test_vars import peak_analysis_results

# Import Metric from the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_file_dir, "files", "collect-qc-test-data")


def test_peak_analysis():
    peak_analysis_test = metric.insert_size(
        operator="peak_analysis", operand={"columns": [1, 2]}
    )
    assert os.path.exists("CollectQC_Plots/insert_size.png")
    # Remove all plots in the CollectQC_Plots folder
    for file in os.listdir("CollectQC_Plots"):
        os.remove(os.path.join("CollectQC_Plots", file))
    os.rmdir("CollectQC_Plots")

    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_peak_analysis_test = {}
    dict_peak_analysis_results = {}
    for i in range(len(peak_analysis_test)):
        dict_peak_analysis_test[peak_analysis_test[i]["Sample"]] = peak_analysis_test[i]

    for i in range(len(peak_analysis_results)):
        dict_peak_analysis_results[
            peak_analysis_results[i]["Sample"]
        ] = peak_analysis_results[i]

    assert dict_peak_analysis_test == dict_peak_analysis_results
