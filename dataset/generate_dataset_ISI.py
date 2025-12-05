import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# ============================
# PARAMÈTRES GÉNÉRAUX
# ============================
N = 7000

type_bac_list = ["Mathématiques", "Sciences", "Technique", "Informatique"]
type_bac_weights = [0.25, 0.20, 0.15, 0.40]

parcours_list = ["Licence", "Cycle Ingénieur", "Master"]
parcours_weights = [0.50, 0.20, 0.30]

rows = []

# ============================
# GÉNÉRATION DES DONNÉES
# ============================
for _ in range(N):

    # Données personnelles
    age = np.random.randint(19, 31)  # pas d'influence
    type_bac = random.choices(type_bac_list, weights=type_bac_weights)[0]
    parcours = random.choices(parcours_list, weights=parcours_weights)[0]

    # Données académiques
    moyenne_bac = round(np.random.uniform(11, 18), 2)
    moyenne_s1 = round(np.clip(np.random.normal(moyenne_bac - 0.5, 1.5), 6, 16), 2)
    moyenne_s2 = round(np.clip(np.random.normal(moyenne_s1, 1.5), 6, 16), 2)
    nb_modules_echoues = np.random.choice([0, 1, 2, 3, 4], p=[0.35,0.30,0.18,0.12,0.05])

    # Ajustement logique : si nb_modules_echoues >= 3, moyenne_s1 et s2 <= 9
    if nb_modules_echoues >= 3:
        moyenne_s1 = min(moyenne_s1, 9)
        moyenne_s2 = min(moyenne_s2, 9)

    # Recalcul de la moyenne générale
    moyenne_generale_s1_s2 = (moyenne_s1 + moyenne_s2) / 2
    reussite_generale = 1 if moyenne_generale_s1_s2 >= 10 else 0

    # Comportement
    heures_travail_semaine = round(np.clip(np.random.normal(8 + (moyenne_s2-10)/2, 4), 0, 30), 1)

    # Discipline & satisfaction
    discipline = int(np.clip(np.random.normal(3.2 + (moyenne_s2-10)/3, 0.8), 1, 5))
    satisfaction_parcours = int(np.clip(np.random.normal(3.0 + discipline/4, 0.8), 1, 5))

    # Travail parallèle
    travail_parallele = random.choices(["Oui", "Non"], weights=[0.35, 0.65])[0]

    # Résultat final dépend de plusieurs paramètres
    score = (
        0.4*moyenne_s2 + 
        0.3*discipline + 
        0.1*satisfaction_parcours + 
        0.1*(4 - nb_modules_echoues) + 
        (0.1 if travail_parallele=="Non" else -0.1)
    )
    # Transformation en binaire
    resultat_final = 1 if score >= 6 else 0

    rows.append({
        "age": age,
        "type_bac": type_bac,
        "parcours": parcours,
        "moyenne_bac": moyenne_bac,
        "moyenne_s1": moyenne_s1,
        "moyenne_s2": moyenne_s2,
        "moyenne_generale_s1_s2": moyenne_generale_s1_s2,
        "nb_modules_echoues": nb_modules_echoues,
        "heures_travail_semaine": heures_travail_semaine,
        "discipline_note_sur_5": discipline,
        "satisfaction_parcours_note_sur_5": satisfaction_parcours,
        "travail_parallele": travail_parallele,
        "reussite_generale": reussite_generale,
        "resultat_final": resultat_final
    })

# Création du dataset
df = pd.DataFrame(rows)
df.to_csv("dataset_reussite_etudiants_ISI.csv", index=False)
