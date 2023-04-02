from termcolor import colored

coverage_case = [
    {
        "AutoStatus": colored("FAIL", color="red", attrs=["bold"]),
        "Sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "Reason": "The coverage deviation of 0.68 is greater than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_X005_d05",
        "Reason": "The coverage deviation of 0.525 is less than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("FAIL", color="red", attrs=["bold"]),
        "Sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "Reason": "The coverage deviation of 0.785 is greater than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_G006_d06",
        "Reason": "The coverage deviation of 0.537 is less than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_X006_d05",
        "Reason": "The coverage deviation of 0.499 is less than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Reason": "The coverage deviation of 0.524 is less than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_G007_d06",
        "Reason": "The coverage deviation of 0.525 is less than the 0.6 threshold.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Reason": "The coverage deviation of 0.524 is less than the 0.6 threshold.",
    },
]
