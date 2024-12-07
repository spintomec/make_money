from models import (
    calculer_capacite_emprunt,
    calculer_mensualite,
    mise_a_jour_salaire,
    mettre_a_jour_epargne,
    generer_depense_imprevue,
)

def calculer_valeur_totale_biens(liste_credit_montant, taux_croissance_bien, annee_courante, mois_courant):
    return sum(liste_credit_montant) * (1 + taux_croissance_bien) ** (annee_courante - 2024 + mois_courant / 12)

def effectuer_simulation(salaire_mensuel, taux_mensuel, duree_emprunt, rentabilite_net, enveloppe_travaux, epargne, epargne_mensuelle, parametres, liste_mois):
    taux_croissance_loyer = parametres["taux_croissance_loyer"]
    taux_croissance_bien = parametres["taux_croissance_bien"]
    taux_vacance_locative = parametres["taux_vacance_locative"]
    taux_impayes = parametres["taux_impayes"]

    resultats = []
    patrimoine_statut = []
    liste_credit_montant = []
    nb_credit = 0
    annee_courante = 2025
    mois_courant = 3
    delais_credit_counter = 0

    max_iterations = 30 * 12  # Maximum de 30 ans * 12 mois
    iteration_count = 0  # Compteur d'itérations

    while iteration_count < max_iterations:  # Limitation du nombre d'itérations
        iteration_count += 1
        mois_courant += 1
        if mois_courant > 12:
            mois_courant = 1
            annee_courante += 1
            salaire_mensuel = mise_a_jour_salaire(salaire_mensuel, 0.025 / 12)

        montant_credit_hypothetique = 120000  # Montant fixe du crédit
        montant_credit_hypothetique *= 1.08  # Ajout 8% de frais de notaire
        revenu_locatif_additionnel = montant_credit_hypothetique * (rentabilite_net / 1000)

        revenu_locatif_actuel = revenu_locatif_additionnel * (1 + taux_croissance_loyer) ** (
            annee_courante - 2024 + mois_courant / 12
        )
        revenu_locatif_net = revenu_locatif_actuel * (1 - taux_vacance_locative - taux_impayes)
        revenu_total = salaire_mensuel + revenu_locatif_net * nb_credit

        depense_imprevue = generer_depense_imprevue(nb_credit)

        mensualite = calculer_mensualite(montant_credit_hypothetique, taux_mensuel, duree_emprunt)
        epargne, credit_possible = mettre_a_jour_epargne(
            epargne, epargne_mensuelle, revenu_locatif_net, mensualite, nb_credit,
            montant_credit_hypothetique, enveloppe_travaux, depense_imprevue
        )

        capacite_emprunt = calculer_capacite_emprunt(revenu_total, taux_mensuel, duree_emprunt) - sum(liste_credit_montant)

        if capacite_emprunt < montant_credit_hypothetique:
            if capacite_emprunt + epargne >= montant_credit_hypothetique + enveloppe_travaux:
                if delais_credit_counter == 3:
                    epargne = epargne + capacite_emprunt - montant_credit_hypothetique - enveloppe_travaux
                    liste_credit_montant.append(capacite_emprunt)
                    capacite_emprunt = 0
                    nb_credit += 1
                    delais_credit_counter = 0
                else:
                    delais_credit_counter += 1
        elif capacite_emprunt >= montant_credit_hypothetique:
            if delais_credit_counter == 3:
                liste_credit_montant.append(montant_credit_hypothetique)
                epargne -= enveloppe_travaux
                nb_credit += 1
            else:
                delais_credit_counter += 1

        mensualite_totale = sum(
            calculer_mensualite(credit, taux_mensuel, duree_emprunt) for credit in liste_credit_montant
        )
        epargne += max(0, revenu_locatif_net - mensualite_totale) * nb_credit

        valeur_totale_biens = calculer_valeur_totale_biens(
            liste_credit_montant, taux_croissance_bien, annee_courante, mois_courant
        )

        resultats.append({
            "annee": annee_courante, "mois": liste_mois[mois_courant - 1],
            "nombre_de_credits": nb_credit,
            "revenu_total": round(revenu_total),
            "valeur_totale_biens": round(valeur_totale_biens),
            "epargne": round(epargne),
            "capacite_emprunt_restante": round(capacite_emprunt),
            "valeur_totale_credits": round(sum(liste_credit_montant)),
            "montant_total_remboursement": round(mensualite_totale * 12),
            "depense_imprevue": round(depense_imprevue),
        })

        if valeur_totale_biens >= 1000000:
            patrimoine_statut.append({
                "message": f"Le patrimoine atteint 1 million d'euros en {liste_mois[mois_courant - 1]} {annee_courante}",
                "success": True
            })
            break

    if valeur_totale_biens < 1000000:
        patrimoine_statut.append({
            "message": "Le patrimoine n'a pas atteint 1 million d'euros après 30 ans.",
            "success": False
        })

    return resultats, patrimoine_statut
