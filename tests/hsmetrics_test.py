import os
import pytest
import sys
from termcolor import colored


# Import Metric from the scripts folder
test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))

from metric import Metric

# Initialize the Metric class and set the qc_folder
metric = Metric()
metric.qc_folder = os.path.join(test_dir, "collect-qc-test-data")

# Mean target coverage values for warn: 700 and error: 500
correct_coverages = [
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "file": "s_C_AJV7P3_X005_d05.rg.md.hsmetrics",
        "sample": "s_C_AJV7P3_X005_d05",
        "coverage": 908.58603,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "file": "FFPEPOOLEDNORMAL_IMPACT505_V2.rg.md.hsmetrics",
        "sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 843.729729,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "file": "s_C_AJV7P3_G006_d06.rg.md.hsmetrics",
        "sample": "s_C_AJV7P3_G006_d06",
        "coverage": 747.236097,
    },
    {
        "autostatus": colored("ERROR", color="red", attrs=["bold"]),
        "file": "FROZENPOOLEDNORMAL_IMPACT505_V2.rg.md.hsmetrics",
        "sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 480.459346,
    },
    {
        "autostatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "file": "s_C_VXXWFY_N008_d07.rg.md.hsmetrics",
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("ERROR", color="red", attrs=["bold"]),
        "file": "s_C_VXXWFY_X006_d05.rg.md.hsmetrics",
        "sample": "s_C_VXXWFY_X006_d05",
        "coverage": 288.388097,
    },
    {
        "autostatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "file": "s_C_VXXWFY_N008_d07.rg.md.hsmetrics",
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "file": "s_C_VXXWFY_G007_d06.rg.md.hsmetrics",
        "sample": "s_C_VXXWFY_G007_d06",
        "coverage": 767.894311,
    },
]


def test_mean_target_coverage():
    correct_mean_target_coverages = metric.hsmetrics(
        operator="coverage",
        operand={"mean_target_coverage": {"warn": 700, "error": 500}},
    )
    assert correct_mean_target_coverages == correct_coverages

    incorrect_mean_target_coverages = metric.hsmetrics(
        operator="coverage",
        operand={"mean_target_coverage": {"warn": 0, "error": 0}},
    )
    assert incorrect_mean_target_coverages != correct_coverages
