from termcolor import colored

# Pass mean target coverage values for warn: 200 and error: 100
pass_mean_coverages = [
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_AJV7P3_X005_d05",
        "coverage": 908.58603,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 843.729729,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_AJV7P3_G006_d06",
        "coverage": 747.236097,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 480.459346,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_VXXWFY_X006_d05",
        "coverage": 288.388097,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_VXXWFY_G007_d06",
        "coverage": 767.894311,
    },
]

# Warning and Error mean target coverage values for warn: 700 and error: 500
warn_error_mean_coverages = [
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_AJV7P3_X005_d05",
        "coverage": 908.58603,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "FFPEPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 843.729729,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_AJV7P3_G006_d06",
        "coverage": 747.236097,
    },
    {
        "autostatus": colored("ERROR", color="red", attrs=["bold"]),
        "sample": "FROZENPOOLEDNORMAL_IMPACT505_V2",
        "coverage": 480.459346,
    },
    {
        "autostatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("ERROR", color="red", attrs=["bold"]),
        "sample": "s_C_VXXWFY_X006_d05",
        "coverage": 288.388097,
    },
    {
        "autostatus": colored("WARNING", color="yellow", attrs=["bold"]),
        "sample": "s_C_VXXWFY_N008_d07",
        "coverage": 614.823368,
    },
    {
        "autostatus": colored("PASS", color="green", attrs=["bold"]),
        "sample": "s_C_VXXWFY_G007_d06",
        "coverage": 767.894311,
    },
]