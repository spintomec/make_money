import random

def calculer_capacite_emprunt(salaire, taux_mensuel, duree):
    return salaire * 0.35 * ((1 + taux_mensuel) ** duree - 1) / (taux_mensuel * (1 + taux_mensuel) ** duree)

def calculer_mensualite(montant_credit, taux_mensuel, duree):
    return montant_credit * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree)

def mise_a_jour_salaire(salaire, taux_annuel):
    return salaire * (1 + taux_annuel / 12)

def calculer_revenu_locatif(montant, taux, annee, mois):
    return montant * (1 + taux) ** (annee - 2024 + mois / 12)

def generer_depense_imprevue(nb_credit):
    depense = random.uniform(0, 85) * nb_credit
    return depense

def mettre_a_jour_epargne(epargne, epargne_mensuelle, revenu_net, mensualite, nb_credit, montant_credit, travaux, depense):
    epargne += epargne_mensuelle + (revenu_net - mensualite) * nb_credit - depense
    return epargne, epargne >= montant_credit + travaux