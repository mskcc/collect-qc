import os
import pytest
import sys


# Import the test data
test_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_file_dir, "files"))
from concordance_test_vars import one_pass_match_matrix, warn_error_match_matrix

# Import Metric from the scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_file_dir, "files", "collect-qc-test-data")


def test_match_sample_matrix():
    warn_error_case = metric.concordance(
        operator="match_sample_matrix",
        operand={
            "match_error_lt": 49,
            "match_warn_lt": 90,
            "unmatch_warn_gt": 43.41,
            "unmatch_error_gt": 60,
        },
    )
    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_warn_error_case = {}
    dict_warn_error_match_matrix = {}
    for i in range(len(warn_error_case)):
        dict_warn_error_case[warn_error_case[i]["Sample"]] = warn_error_case[i]
    for i in range(len(warn_error_match_matrix)):
        dict_warn_error_match_matrix[
            warn_error_match_matrix[i]["Sample"]
        ] = warn_error_match_matrix[i]
    assert dict_warn_error_case == dict_warn_error_match_matrix

    one_pass_case = metric.concordance(
        operator="match_sample_matrix",
        operand={
            "match_error_lt": 80,
            "match_warn_lt": 90,
            "unmatch_warn_gt": 50,
            "unmatch_error_gt": 70,
        },
    )
    # GitHub Actions will test the results out of order, so we need to use dictionaries
    dict_pass_case = {}
    dict_pass_match_matrix = {}
    for i in range(len(one_pass_case)):
        dict_pass_case[one_pass_case[i]["Sample"]] = one_pass_case[i]
    for i in range(len(one_pass_match_matrix)):
        dict_pass_match_matrix[
            one_pass_match_matrix[i]["Sample"]
        ] = one_pass_match_matrix[i]
    assert dict_pass_case == dict_pass_match_matrix
