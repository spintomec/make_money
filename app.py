from flask import Flask, render_template, request
from simulation import effectuer_simulation
from scenarios import obtenir_scenarios
from utils import enregistrer_resultats_txt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    scenarios = obtenir_scenarios()
    resultats = []
    form_data = {}
    liste_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    if request.method == "POST":
        try:
            scenario_choisi = request.form.get("scenario")
            parametres = scenarios[scenario_choisi]
            
            # Récupération des données du formulaire
            salaire_mensuel = float(request.form.get("salaire_mensuel", 0))
            taux_mensuel = parametres["taux_annuel"] / 12
            duree_emprunt = int(request.form.get("duree_emprunt", 0)) * 12
            rentabilite_net = float(request.form.get("rentabilite_net", 0))
            enveloppe_travaux = float(request.form.get("enveloppe_travaux", 0))
            epargne = float(request.form.get("epargne", 0))
            epargne_mensuelle = float(request.form.get("epargne_mensuelle", 0))

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

            # Appel de la simulation
            resultats = effectuer_simulation(
                salaire_mensuel, taux_mensuel, duree_emprunt, rentabilite_net,
                enveloppe_travaux, epargne, epargne_mensuelle, parametres, liste_mois
            )
            
            # Enregistrement des résultats
            # enregistrer_resultats_txt(resultats)

        except (ValueError, TypeError) as e:
            error_message = f"Erreur : {e}"
            return render_template("index.html", error_message=error_message, form_data=form_data)

    return render_template("index.html", resultats=resultats, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
