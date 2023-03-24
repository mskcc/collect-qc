from termcolor import colored

one_pass_match_matrix = [
    {
        "AutoStatus": colored("ERROR", "red", attrs=["bold"]),
        "Sample": "s_C_Patient_1_N009_d07",
        "Reason": "s_C_Patient_1_G007_d06 fell below the 80 match threshold.",
    },
    {
        "AutoStatus": colored("ERROR", "red", attrs=["bold"]),
        "Sample": "s_C_Patient_1_N009_d07",
        "Reason": "s_C_Patient_2_X005_d05 exceeded the 70 mismatch threshold.",
    },
]

warn_error_match_matrix = [
    {
        "AutoStatus": colored("ERROR", "red", attrs=["bold"]),
        "Sample": "s_C_Patient_1_N009_d07",
        "Reason": "s_C_Patient_1_G007_d06 fell below the 49 match threshold.",
    },
    {
        "AutoStatus": colored("ERROR", "red", attrs=["bold"]),
        "Sample": "s_C_Patient_1_N009_d07",
        "Reason": "s_C_Patient_2_X005_d05 exceeded the 60 mismatch threshold.",
    },
    {
        "AutoStatus": colored("WARNING", "yellow", attrs=["bold"]),
        "Sample": "s_C_Patient_1_N008_d07",
        "Reason": "s_C_Patient_2_X005_d05, s_C_Patient_2_G006_d06 fell within the 43.41 and 60 mismatch thresholds.",
    },
]
