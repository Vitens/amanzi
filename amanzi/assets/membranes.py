MEMBRANE_DB =  {
    "SUEZ AK-400H": {
        "nominal_flow": 41.6, #m3/day
        "salt_rejection": 99.65, # %
        "retention": {"Na": 0.9965, "Cl": 0.9965},
        # "Qf_max": 17.0, #m3/h
        "dP_max": 1.03, # bar
        "P_max": 27.56, # bar
        "flux_avg": 25., # L/m2h
        "A_e": 40.9, # m2
        "test_conditions": {
            "C_feed": 500, # mg/L NaCl
            "P_feed": 7.93, # bar
            "recovery": 15, # %
            "temperature": 25, # C
        }
    },
    # "ESPA2-LD": {
    #     "nominal_flow": 27.3, #m3/day
    #     "salt_rejection": 99.7, # %
    #     "retention": {"Na": 0.997, "Cl": 0.997},
    #     "Qf_max": 17.0, #m3/h
    #     "Qc_min": 2.7, #m3/h
    #     "dP_max": 1.0, # bar
    #     "P_max": 41.4, # bar
    #     "flux_avg": 15., # L/m2h
    #     "A_e": 40.9, # m2
    #     "test_conditions": {
    #         "C_feed": 32000, # mg/L NaCl
    #         "P_feed": 55, # bar
    #         "recovery": 10, # %
    #         "temperature": 25, # C
    #     }
    # },
    # "ESPA2": {
    #     "nominal_flow": 27.3, #m3/day
    #     "salt_rejection": 95.7, # %
    #     "retention": {"Na": 0.957, "Cl": 0.957},
    #     "Qf_max": 19.0, #m3/h
    #     "dP_max": 2.0, # bar
    #     "flux_avg": 15., # L/m2h
    #     "A_e": 35.9, # m2
    #     "test_conditions": {
    #         "C_feed": 32000, # mg/L NaCl
    #         "P_feed": 55, # bar
    #         "recovery": 10, # %
    #         "temperature": 25, # C
    #     }
    # }
}