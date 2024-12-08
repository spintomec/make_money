import random

# Calcul de la capacité d'emprunt en fonction du salaire, de la durée d'emprunt et des taux d'intéret annuels
def calculer_capacite_emprunt(salaire, taux_mensuel, duree):
    return salaire * 0.35 * ((1 + taux_mensuel) ** duree - 1) / (taux_mensuel * (1 + taux_mensuel) ** duree)

def calculer_mensualite(montant_credit, taux_mensuel, duree):
    return montant_credit * taux_mensuel / (1 - (1 + taux_mensuel) ** - duree)

def mise_a_jour_salaire(salaire, taux_annuel):
    return salaire * (1 + taux_annuel / 12)

def calculer_revenu_locatif(montant, taux, annee, mois):
    # Calcul des années et mois écoulés depuis 2024
    annees_ecoulees = annee - 2024
    mois_ecoules = annees_ecoulees * 12 + mois
    # Application de l'intérêt composé
    return montant * (1 + taux) ** (mois_ecoules / 12)

def generer_depense_imprevue(nb_credit):
    depense = random.uniform(0, 85) * nb_credit
    return depense

def mettre_a_jour_epargne(epargne, epargne_mensuelle, revenu_net, mensualite, nb_credit, montant_credit, travaux, depense):
    # Calcul de l'épargne après ajout de l'épargne mensuelle et des excédents de revenus
    epargne += epargne_mensuelle + (revenu_net - mensualite) * nb_credit - depense
    # Vérification si l'épargne permet d'atteindre le montant requis pour le crédit et les travaux
    peut_acheter = epargne >= montant_credit + travaux
    return epargne, peut_acheter
