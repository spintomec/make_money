from flask import Flask, render_template, request
from models import (
    calculer_capacite_emprunt,
    calculer_mensualite,
    mise_a_jour_salaire,
    mettre_a_jour_epargne,
    generer_depense_imprevue,
    calculer_revenu_locatif,
)
from scenarios import obtenir_scenarios
from utils import enregistrer_resultats_txt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    scenarios = obtenir_scenarios()
    resultats = []
    form_data = {}
    if request.method == "POST":
        try:
            scenario_choisi = request.form.get("scenario")
            parametres = scenarios[scenario_choisi]
            taux_croissance_loyer = parametres["taux_croissance_loyer"]
            taux_croissance_bien = parametres["taux_croissance_bien"]
            taux_vacance_locative = parametres["taux_vacance_locative"]
            taux_impayes = parametres["taux_impayes"]

            salaire_mensuel = float(request.form.get("salaire_mensuel", 0))
            taux_mensuel = parametres["taux_annuel"] / 12
            duree_emprunt = int(request.form.get("duree_emprunt", 0)) * 12
            rentabilite_net = float(request.form.get("rentabilite_net", 0))
            enveloppe_travaux = float(request.form.get("enveloppe_travaux", 0))
            epargne = float(request.form.get("epargne", 0))
            epargne_mensuelle = float(request.form.get("epargne_mensuelle", 0))
            nb_credit = 0
            annee_courante = 2025
            mois_courant = 3

            if salaire_mensuel <= 0 or duree_emprunt <= 0 or rentabilite_net <= 0 or enveloppe_travaux <= 0 or epargne <= 0:
                raise ValueError("Veuillez saisir des valeurs valides pour tous les champs.")
            
            form_data = {
                'scenario': scenario_choisi,
                'salaire_mensuel': round(salaire_mensuel),
                'duree_emprunt': round(duree_emprunt / 12),
                'rentabilite_net': round(rentabilite_net),
                'enveloppe_travaux': round(enveloppe_travaux),
                'epargne': round(epargne),
                'epargne_mensuelle': round(epargne_mensuelle),
            }

            liste_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            liste_credit_montant = []
            capacite_emprunt = calculer_capacite_emprunt(salaire_mensuel, taux_mensuel, duree_emprunt)
            delais_credit_counter = 0

            while True:
                mois_courant += 1
                if mois_courant > 12:
                    mois_courant = 1
                    annee_courante += 1
                    salaire_mensuel = mise_a_jour_salaire(salaire_mensuel, 0.02)
                    
                montant_credit_hypothetique = 120000  # Montant fixe du crédit
                montant_credit_hypothetique *= 1.08  # Ajout 8% de frais de notaire
                revenu_locatif_additionnel = montant_credit_hypothetique * (rentabilite_net / 1000)

                revenu_locatif_actuel = revenu_locatif_additionnel * (1 + taux_croissance_loyer) ** (annee_courante - 2024 + mois_courant / 12)
                revenu_locatif_net = revenu_locatif_actuel * (1 - taux_vacance_locative - taux_impayes)
                revenu_total = salaire_mensuel + revenu_locatif_net * nb_credit
                
                # Génère une dépense imprévue aléatoire pour le mois courant
                depense_imprevue = generer_depense_imprevue()

                mensualite = calculer_mensualite(montant_credit_hypothetique, taux_mensuel, duree_emprunt)
                epargne, credit_possible = mettre_a_jour_epargne(epargne, epargne_mensuelle, revenu_locatif_net, mensualite, nb_credit, montant_credit_hypothetique, enveloppe_travaux, depense_imprevue)

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

                mensualite_totale = sum(calculer_mensualite(credit, taux_mensuel, duree_emprunt) for credit in liste_credit_montant)
                epargne += max(0, revenu_locatif_net - mensualite_totale) * nb_credit

                valeur_totale_biens = sum(liste_credit_montant) * (1 + taux_croissance_bien) ** (annee_courante - 2024 + mois_courant / 12)
                
                resultats.append({
                        "annee": annee_courante, "mois": liste_mois[mois_courant - 1],
                        "nombre_de_credits": nb_credit,
                        "revenu_total": round(revenu_total),
                        "valeur_totale_biens": round(valeur_totale_biens),
                        "epargne": round(epargne),
                        "capacite_emprunt_restante": round(capacite_emprunt),
                        "valeur_totale_credits": round(sum(liste_credit_montant)),
                        "montant_total_remboursement": round(mensualite_totale * 12),
                        "depense_imprevue": round(depense_imprevue)
                    })
                
                if valeur_totale_biens >= 1000000:
                    break
            enregistrer_resultats_txt(resultats)

        except (ValueError, TypeError) as e:
            error_message = f"Erreur : {e}"
            return render_template("index.html", error_message=error_message, form_data=form_data)

    return render_template("index.html", resultats=resultats, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
