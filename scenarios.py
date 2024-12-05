def obtenir_scenarios():
    return {
        "optimiste": {
            "taux_croissance_loyer": 0.03,
            "taux_croissance_bien": 0.03,
            "taux_vacance_locative": 0.05,
            "taux_impayes": 0.02,
            "taux_annuel": 0.025
        },
        "neutre": {
            "taux_croissance_loyer": 0.025,
            "taux_croissance_bien": 0.025,
            "taux_vacance_locative": 0.07,
            "taux_impayes": 0.03,
            "taux_annuel": 0.035
        },
        "pessimiste": {
            "taux_croissance_loyer": 0.02,
            "taux_croissance_bien": 0.015,
            "taux_vacance_locative": 0.1,
            "taux_impayes": 0.05,
            "taux_annuel": 0.04
        }
    }
