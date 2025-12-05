# pip install streamlit pandas scikit-learn seaborn matplotlib joblib

import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

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

# =============================
# OPTION 1 : IMPORT DATASET
# =============================
if menu == "📂 Importer un Dataset":

    st.header("📊 Analyse Automatique d’un Dataset")
    file = st.file_uploader("Importer votre fichier CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.subheader("✅ Aperçu des données")
        st.dataframe(df.head())

        st.subheader("📈 Statistiques Générales")
        st.write(df.describe())

        # Visualisation taux de réussite
        if "resultat_final" in df.columns:
            st.subheader("📊 Taux de Réussite")
            fig, ax = plt.subplots()
            sns.countplot(x="resultat_final", data=df, ax=ax)
            st.pyplot(fig)

        # Prédictions automatiques
        st.subheader("🔮 Prédictions Automatiques")
        X = df.drop(columns=["resultat_final","reussite_generale"], errors="ignore")
        predictions = model.predict(X)
        df["prediction"] = predictions
        st.dataframe(df.head())

        # Recommandations
        st.subheader("✅ Recommandations Automatiques")
        def recommendation(row):
            if row["prediction"] == 1:
                return "✅ Bon niveau – Continuer les efforts"
            elif row.get("nb_modules_echoues", 0) >= 3:
                return "⚠️ Tutorats intensifs recommandés"
            else:
                return "📘 Renforcement académique conseillé"

        df["recommandation"] = df.apply(recommendation, axis=1)
        st.dataframe(df[["prediction", "recommandation"]].head())

# =============================
# OPTION 2 : FORMULAIRE ÉTUDIANT
# =============================
if menu == "🧑‍🎓 Prédiction Étudiant (Formulaire)":

    st.header("🧑‍🎓 Prédiction en Temps Réel")

    # Champs
    age = st.number_input("Âge", 18, 40)
    m1 = st.number_input("Moyenne S1", 0.0, 20.0)
    m2 = st.number_input("Moyenne S2", 0.0, 20.0)
    modules = st.number_input("Nombre de modules échoués", 0, 10)
    heures = st.number_input("Heures de travail / semaine", 0, 80)
    discipline = st.slider("Discipline /5", 1, 5)
    satisfaction = st.slider("Satisfaction /5", 1, 5)
    travail = st.selectbox("Travail parallèle", ["Oui", "Non"])
    bac = st.selectbox("Type Bac", ["Mathématiques", "Sciences", "Technique", "Informatique"])
    parcours = st.selectbox("Parcours", ["Licence", "Cycle Ingénieur", "Master"])

    if st.button("🔮 Prédire la réussite"):
        moyenne_gen = (m1 + m2) / 2
        data = pd.DataFrame([[age, bac, parcours, m1, m2, moyenne_gen, modules, heures, discipline, satisfaction, travail]],
                            columns=[
                                "age","type_bac","parcours","moyenne_s1","moyenne_s2","moyenne_generale_s1_s2",
                                "nb_modules_echoues","heures_travail_semaine","discipline_note_sur_5",
                                "satisfaction_parcours_note_sur_5","travail_parallele"
                            ])
        prediction = model.predict(data)[0]

        if prediction == 1:
            st.success("✅ L'étudiant a une FORTE chance de réussir")
            st.info("🎯 Recommandation : Continuer les efforts")
        else:
            st.error("❌ Risque d'échec détecté")
            st.warning("📘 Recommandation : Tutorats + accompagnement pédagogique")
