def obtenir_scenarios():
    return {
        "optimiste": {
            "description": "Croissance élevée",
            "taux_annuel": 0.025,
            "taux_augmentation_salaire": 0.03,
            "taux_croissance_loyer": 0.03,
            "taux_croissance_bien": 0.0275,
            "taux_vacance_locative": 0.05,
            "taux_impayes": 0.02,
        },
        "realiste": {
            "description": "Croissance modérée",
            "taux_annuel": 0.035,
            "taux_augmentation_salaire": 0.02,
            "taux_croissance_loyer": 0.025,
            "taux_croissance_bien": 0.025,
            "taux_vacance_locative": 0.07,
            "taux_impayes": 0.03,
        },
        "pessimiste": {
            "description": "Croissance faible",
            "taux_annuel": 0.04,
            "taux_augmentation_salaire": 0.01,
            "taux_croissance_loyer": 0.02,
            "taux_croissance_bien": 0.015,
            "taux_vacance_locative": 0.1,
            "taux_impayes": 0.05,
        }
    }
