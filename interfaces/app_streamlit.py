# app_streamlit.py
# pip install streamlit pandas scikit-learn seaborn matplotlib joblib requests

import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="Dashboard Réussite Étudiante", layout="wide")
st.title("🎓 Dashboard Intelligent - Réussite Étudiante")

# Charger le modèle
model = joblib.load("../modeles_sauvegardes/xgboost_model.pkl")

# =============================
# MENU
# =============================
menu = st.sidebar.radio("MENU", [
    "📂 Importer un Dataset",
    "🧑‍🎓 Prédiction Étudiant (Formulaire)"
])

# Colonnes attendues par le modèle
model_columns = [
    "age",
    "moyenne_bac",
    "moyenne_s1",
    "moyenne_s2",
    "moyenne_generale",
    "nb_modules_echoues",
    "heures_travail_semaine",
    "discipline_note_sur_5",
    "satisfaction_parcours_note_sur_5",
    "travail_parallele",
    "type_bac",
    "parcours"
]

# =============================
# FONCTION PAGINATION
# =============================
def paginated_table(df, page_size=5, key="table"):
    if f"page_{key}" not in st.session_state:
        st.session_state[f"page_{key}"] = 0

    total_pages = (len(df) - 1) // page_size + 1
    start = st.session_state[f"page_{key}"] * page_size
    end = start + page_size

    st.dataframe(df.iloc[start:end], use_container_width=True)

    # Colonnes : Précédent | espace | Texte page | espace | Suivant
    col1, col2, col3, col4, col8 = st.columns([2, 1, 4, 1 ,1,1, 1, 2])

    with col1:
        if st.button("Précédent", key=f"prev_{key}",
                     disabled=st.session_state[f"page_{key}"] == 0):
            st.session_state[f"page_{key}"] -= 1

    with col3:
        st.markdown(
            f"<p style='text-align:center; font-weight:bold;'>Page {st.session_state[f'page_{key}'] + 1} / {total_pages}</p>",
            unsafe_allow_html=True
        )

    with col6:
        if st.button("Suivant", key=f"next_{key}",
                     disabled=st.session_state[f"page_{key}"] >= total_pages - 1):
            st.session_state[f"page_{key}"] += 1


# =============================
# OPTION 1 : IMPORT DATASET
# =============================
if menu == "📂 Importer un Dataset":
    st.header("📊 Analyse Automatique d’un Dataset")
    file = st.file_uploader("Importer votre fichier CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        if "moyenne_generale" not in df.columns:
            if "moyenne_s1" in df.columns and "moyenne_s2" in df.columns:
                df["moyenne_generale"] = (df["moyenne_s1"] + df["moyenne_s2"]) / 2
            else:
                st.warning("⚠️ Impossible de calculer 'moyenne_generale'")
                df["moyenne_generale"] = 0

        if "age" not in df.columns:
            df["age"] = 20

        for col in model_columns:
            if col not in df.columns:
                if col in ["travail_parallele","type_bac","parcours"]:
                    df[col] = "Non spécifié"
                else:
                    df[col] = 0

        st.subheader("✅ Aperçu des données")
        paginated_table(df, page_size=5, key="apercu")

        st.subheader("📈 Statistiques Générales")
        st.write(df.describe())

        if "resultat_final" in df.columns:
            st.subheader("📊 Taux de Réussite")
            fig, ax = plt.subplots()
            sns.countplot(x="resultat_final", data=df, ax=ax)
            st.pyplot(fig)

        st.subheader("🔮 Prédictions Automatiques")
        X = df[model_columns]
        df["prediction"] = model.predict(X)
        paginated_table(df, page_size=5, key="predictions")

        st.subheader("✅ Recommandations Automatiques")
        def recommendation(row):
            if row["prediction"] == 1:
                return "✅ Bon niveau – Continuer les efforts"
            elif row.get("nb_modules_echoues", 0) >= 3:
                return "⚠️ Tutorats intensifs recommandés"
            else:
                return "📘 Renforcement académique conseillé"
        df["recommandation"] = df.apply(recommendation, axis=1)
        paginated_table(df[["prediction","recommandation"]], page_size=5, key="recommandations")

# =============================
# OPTION 2 : FORMULAIRE ÉTUDIANT
# =============================
if menu == "🧑‍🎓 Prédiction Étudiant (Formulaire)":
    st.header("🧑‍🎓 Prédiction en Temps Réel et Sauvegarde")

    age = st.number_input("Âge", 19, 60)
    moyenne_bac = st.number_input("Moyenne Bac", 0.0, 20.0)
    m1 = st.number_input("Moyenne S1", 0.0, 20.0)
    m2 = st.number_input("Moyenne S2", 0.0, 20.0)
    modules = st.number_input("Nombre de modules échoués", 0, 4)
    heures = st.number_input("Heures de travail / semaine", 0, 80)
    discipline = st.slider("Discipline /5", 1, 5)
    satisfaction = st.slider("Satisfaction /5", 1, 5)
    travail = st.selectbox("Travail parallèle", ["Oui", "Non"])
    bac = st.selectbox("Type Bac", ["Mathématiques", "Sciences", "Technique", "Informatique"])

    # Définition dynamique du parcours selon l'âge
    if age >= 21:
        parcours_options = ["Licence", "Cycle Ingénieur", "Master"]
    else:  # age >= 19 et < 21
        parcours_options = ["Licence"]

    parcours = st.selectbox("Parcours", parcours_options)

    if st.button("🔮 Prédire la réussite"):
        moyenne_generale = (m1 + m2) / 2
        data = pd.DataFrame([[age, moyenne_bac, m1, m2, moyenne_generale, modules, heures,
                              discipline, satisfaction, travail, bac, parcours]],
                            columns=model_columns)
        prediction = model.predict(data)[0]

        if prediction == 1:
            st.success("✅ L'étudiant a une FORTE chance de réussir")
            st.info("🎯 Recommandation : Poursuivre vos efforts et consolider vos acquis pour exceller !")
        else:
            st.error("❌ Risque d'échec détecté")
            st.warning("📘 Recommandation : Il est possible de rattraper au contrôle (Tutorats + accompagnement pédagogique)")

        # -------------------------------
        # POST vers API Flask pour sauvegarde
        # -------------------------------
        data_api = {
            "age": age,
            "type_bac": bac,
            "parcours": parcours,
            "moyenne_bac": moyenne_bac,
            "moyenne_s1": m1,
            "moyenne_s2": m2,
            "moyenne_generale": moyenne_generale,
            "nb_modules_echoues": modules,
            "heures_travail_semaine": heures,
            "discipline_note_sur_5": discipline,
            "satisfaction_parcours_note_sur_5": satisfaction,
            "travail_parallele": travail
        }

        try:
            response = requests.post("http://127.0.0.1:5000/add_student", json=data_api)
            if response.status_code == 200:
                st.success("📥 Données sauvegardées dans la base et CSV généré !")
            else:
                st.error(f"❌ Erreur API : {response.status_code}")
        except Exception as e:
            st.error(f"❌ Impossible de contacter l'API : {e}")
