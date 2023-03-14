from termcolor import colored

peak_analysis_results = [
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_X005_d05",
        "Peaks": 1,
        "Max Peak": 158,
        "Reason": "",
    },
    {
        "AutoStatus": colored("FAIL", color="red", attrs=["bold"]),
        "Sample": "three_peaks",
        "Peaks": 3,
        "Max Peak": 169,
        "Reason": "3 peaks detected. Expected 1 peak.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "Peaks": 1,
        "Max Peak": 143,
        "Reason": "",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "Peaks": 1,
        "Max Peak": 215,
        "Reason": "",
    },
    {
        "AutoStatus": colored("FAIL", color="red", attrs=["bold"]),
        "Sample": "two_peaks",
        "Peaks": 2,
        "Max Peak": 169,
        "Reason": "2 peaks detected. Expected 1 peak.",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_G006_d06",
        "Peaks": 1,
        "Max Peak": 169,
        "Reason": "",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_X006_d05",
        "Peaks": 1,
        "Max Peak": 128,
        "Reason": "",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Peaks": 1,
        "Max Peak": 193,
        "Reason": "",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Peaks": 1,
        "Max Peak": 193,
        "Reason": "",
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_G007_d06",
        "Peaks": 1,
        "Max Peak": 157,
        "Reason": "",
    },
]
