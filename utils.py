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