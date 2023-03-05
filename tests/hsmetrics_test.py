import os
import pytest
import sys
from termcolor import colored


test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))

from metric import Metric

metric = Metric()
metric.qc_folder = os.path.join(test_dir, "collect-qc-test-data")

correct_mean_target_coverage = [{}]


def test_mean_target_coverage():
    hsmetrics_results = metric.hsmetrics(
        operator="coverage",
        operand={"mean_target_coverage": {"warn": 500, "error": 300}},
    )
    assert hsmetrics_results == correct_mean_target_coverage
