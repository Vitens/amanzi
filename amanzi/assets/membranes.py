MEMBRANE_DB =  {
    "ESPA2-LD": {
        "nominal_flow": 27.3, #m3/day
        "salt_rejection": 99.7, # %
        "retention": {"Na": 0.997, "Cl": 0.997},
        "feed_flow_max": 17.0, #m3/h
        "dP_max_element": 1.0, # bar
        "flux_avg": 15., # L/m2h
        "A_e": 40.9, # m2
        "test_conditions": {
            "C_feed": 32000, # mg/L NaCl
            "P_feed": 55, # bar
            "recovery": 10, # %
            "temperature": 25, # C
        }
    },
    "ESPA2": {
        "nominal_flow": 27.3, #m3/day
        "salt_rejection": 95.7, # %
        "retention": {"Na": 0.957, "Cl": 0.957},
        "feed_flow_max": 19.0, #m3/h
        "dP_max_element": 2.0, # bar
        "flux_avg": 15., # L/m2h
        "A_e": 35.9, # m2
        "test_conditions": {
            "C_feed": 32000, # mg/L NaCl
            "P_feed": 55, # bar
            "recovery": 10, # %
            "temperature": 25, # C
        }
    }
}