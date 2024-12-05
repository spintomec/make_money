from flask import Flask, render_template, request
import random

app = Flask(__name__)

def calculer_capacite_emprunt(salaire_mensuel, taux_mensuel, duree_emprunt):
    return salaire_mensuel * 0.35 * ((1 + taux_mensuel) ** duree_emprunt - 1) / (taux_mensuel * (1 + taux_mensuel) ** duree_emprunt)

def calculer_mensualite(montant_credit_hypothetique, taux_mensuel, duree_emprunt):
    return montant_credit_hypothetique * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_emprunt)

def mise_a_jour_salaire(salaire_mensuel, taux_augmentation):
    return salaire_mensuel * (1 + taux_augmentation)

def calculer_revenu_locatif(revenu_locatif_additionnel, taux_croissance_loyer, annee_courante, mois_courant):
    return revenu_locatif_additionnel * (1 + taux_croissance_loyer) ** (annee_courante - 2024 + mois_courant / 12)

def generer_depense_imprevue():
    return random.uniform(0, 500) # Génère une dépense imprévue entre 0€ et 500€ par mois

def mettre_a_jour_epargne(epargne, revenu_locatif_net, mensualite, nb_credit, montant_credit_hypothetique, enveloppe_travaux, depense_imprevue):
    epargne += 1600 + (revenu_locatif_net - mensualite) * nb_credit - depense_imprevue
    if epargne >= montant_credit_hypothetique + enveloppe_travaux:
        epargne -= montant_credit_hypothetique + enveloppe_travaux
        return epargne, True
    return epargne, False


@app.route("/", methods=["GET", "POST"])
def index():
    scenarios = {
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
    resultats = []
    if request.method == "POST":
        try:
           
            scenario_choisi = request.form.get("scenarios", "optimiste")
            parametres = scenarios[scenario_choisi]

            taux_annuel = parametres["taux_annuel"]
            taux_croissance_loyer = parametres["taux_croissance_loyer"]
            taux_croissance_bien = parametres["taux_croissance_bien"]
            taux_vacance_locative = parametres["taux_vacance_locative"]
            taux_impayes = parametres["taux_impayes"]

            salaire_mensuel = float(request.form.get("salaire_mensuel", 0))
            taux_mensuel = taux_annuel / 12
            duree_emprunt = int(request.form.get("duree_emprunt", 0)) * 12  # En mois
            rentabilite_net = float(request.form.get("rentabilite_net", 0))
            enveloppe_travaux = float(request.form.get("enveloppe_travaux", 0))
            epargne = float(request.form.get("epargne", 0))
            nb_credit = 0
            annee_courante = 2025
            mois_courant = 3

            # Vérifications supplémentaires pour éviter les NaN
            if salaire_mensuel <= 0 or duree_emprunt <= 0 or rentabilite_net <= 0 or enveloppe_travaux <= 0 or epargne <= 0:
                raise ValueError("Veuillez saisir des valeurs valides pour tous les champs.")

            liste_mois = [
                "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
            ]

            liste_credit_montant = []
            
            
            capacite_emprunt = calculer_capacite_emprunt(salaire_mensuel, taux_mensuel, duree_emprunt)
            delais_credit_counter = 0
            
            max_iterations = 500  # Exemple de limite
            iteration = 0

            while True: # On continue tant que l'on est pas millionnaire
                mois_courant += 1
                if mois_courant > 12:
                    mois_courant = 1
                    annee_courante += 1
                    salaire_mensuel = mise_a_jour_salaire(salaire_mensuel, 0.02)

                # montant_credit_hypothetique = random.randint(100000, 160000)  # Montant aléatoire du crédit
                montant_credit_hypothetique = 120000  # Montant fixe du crédit
                montant_credit_hypothetique *= 1.08  # Ajout 8% de frais de notaire
                revenu_locatif_additionnel = montant_credit_hypothetique * (rentabilite_net / 1000)

                revenu_locatif_actuel = revenu_locatif_additionnel * (1 + taux_croissance_loyer) ** (annee_courante - 2024 + mois_courant / 12)
                revenu_locatif_net = revenu_locatif_actuel * (1 - taux_vacance_locative - taux_impayes)
                revenu_total = salaire_mensuel + revenu_locatif_net * nb_credit

                # Génère une dépense imprévue aléatoire pour le mois courant
                depense_imprevue = generer_depense_imprevue()

                mensualite = calculer_mensualite(montant_credit_hypothetique, taux_mensuel, duree_emprunt)
                epargne, credit_possible = mettre_a_jour_epargne(epargne, revenu_locatif_net, mensualite, nb_credit, montant_credit_hypothetique, enveloppe_travaux, depense_imprevue)

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

                def enregistrer_resultats_txt(resultats, nom_fichier="resultats-web.txt"):
                    with open(nom_fichier, "w", encoding="utf-8") as file:
                        for resultat in resultats:
                            file.write(f"{resultat['mois']} {resultat['annee']}:\n")
                            file.write(f"  - Crédit n°{resultat['nombre_de_credits']}:\n")
                            file.write(f"  - Revenu mensuel : {resultat['revenu_total']} €\n")
                            file.write(f"  - Patrimoine : {resultat['valeur_totale_biens']} €\n")
                            file.write(f"  - Epargne : {resultat['epargne']} €\n")
                            file.write(f"  - Capacité d'emprunt : {resultat['capacite_emprunt_restante']} €\n")
                            file.write(f"  - Montant des crédits : {resultat['valeur_totale_credits']} €\n")
                            file.write(f"  - Montant à rembourser (annuel) : {resultat['montant_total_remboursement']} €\n")
                            file.write(f"  - Dépense imprévue : {resultat['depense_imprevue']} €\n\n")

                # Enregistrement des résultats dans un fichier texte
                enregistrer_resultats_txt(resultats)
        except (ValueError, TypeError) as e:
            error_message = f"Erreur dans les données saisies : {e}"

            return render_template("index.html", error_message=error_message)

    return render_template("index.html", resultats=resultats)

if __name__ == "__main__":
    app.run(debug=True)
