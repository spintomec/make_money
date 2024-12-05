import random

def calculer_capacite_emprunt(salaire_mensuel, taux_mensuel, duree_emprunt):
    return salaire_mensuel * 0.35 * ((1 + taux_mensuel) ** duree_emprunt - 1) / (taux_mensuel * (1 + taux_mensuel) ** duree_emprunt)

def calculer_mensualite(montant_credit_hypothetique, taux_mensuel, duree_emprunt):
    return montant_credit_hypothetique * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_emprunt)

def mise_a_jour_salaire(salaire_mensuel, taux_augmentation):
    return salaire_mensuel * (1 + taux_augmentation/12)

def calculer_revenu_locatif(montant, taux, annee, mois):
    return montant * (1 + taux) ** (annee - 2024 + mois / 12)

def generer_depense_imprevue():
    return random.uniform(0, 500)

def mettre_a_jour_epargne(epargne, revenu_net, mensualite, nb_credit, montant_credit, travaux, depense):
    epargne += 500 + (revenu_net - mensualite) * nb_credit - depense
    return (epargne, epargne >= montant_credit + travaux)
