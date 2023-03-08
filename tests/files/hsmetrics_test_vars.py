from termcolor import colored

# Pass mean target coverage values for warn: 200 and error: 100
pass_mean_coverages = [
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_X005_d05",
        "Mean Target Coverage": 908.58603,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "Mean Target Coverage": 843.729729,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_G006_d06",
        "Mean Target Coverage": 747.236097,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "Mean Target Coverage": 480.459346,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Mean Target Coverage": 614.823368,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_X006_d05",
        "Mean Target Coverage": 288.388097,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Mean Target Coverage": 614.823368,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_G007_d06",
        "Mean Target Coverage": 767.894311,
    },
]

# Warning and Error mean target coverage values for warn: 700 and error: 500
warn_error_mean_coverages = [
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_X005_d05",
        "Mean Target Coverage": 908.58603,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "Mean Target Coverage": 843.729729,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_AJV7P3_G006_d06",
        "Mean Target Coverage": 747.236097,
    },
    {
        "AutoStatus": colored("ERROR", color="red", attrs=["bold"]),
        "Sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "Mean Target Coverage": 480.459346,
    },
    {
        "AutoStatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Mean Target Coverage": 614.823368,
    },
    {
        "AutoStatus": colored("ERROR", color="red", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_X006_d05",
        "Mean Target Coverage": 288.388097,
    },
    {
        "AutoStatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_N008_d07",
        "Mean Target Coverage": 614.823368,
    },
    {
        "AutoStatus": colored("PASS", color="green", attrs=["bold"]),
        "Sample": "s_C_VXXWFY_G007_d06",
        "Mean Target Coverage": 767.894311,
    },
]