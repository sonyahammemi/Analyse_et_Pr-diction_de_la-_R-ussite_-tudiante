# Student Success Analysis and Prediction Dashboard

## Overview
This mini-project focuses on *analyzing and predicting student success* at the Institut Supérieur d’Informatique (ISI). Students are enrolled in various programs (Licence, Engineering Cycle, and Master's) with diverse study modes (on-site, hybrid, online). The goal of this project is to:  
- Analyze student profiles, performance, and behaviors  
- Predict the risk of failure or success  
- Provide personalized recommendations and guidance  

The project is implemented in *Python* and uses *Streamlit* for the interactive dashboard.

---

## Project Structure

plaintext

MP_PYTHON/
│
├─ dataset/                               # Contient les données étudiantes générées
│ |─ dataset_reussite_etudiants_ISI.csv   # Dataset final généré pour l'analyse et la modélisation
│ └─ generate_dataset.py                  # Script Python qui génère le dataset simulé
│
├─ modeles_sauvegardes/                   # Dossier pour stocker les modèles ML entraînés
│ └─ xgboost_model.pkl                     # Modèle XGBoost sauvegardé après entraînement
│
├─ modelisation/                          # Notebook pour la modélisation prédictive
│ └─ etape_3_modelisation.ipynb           # Étape 3 : Prétraitement, entraînement et évaluation des modèles
│
├─ analyse/                               # Notebook pour l'analyse exploratoire des données
│ └─ etape_2_analyse.ipynb                # Étape 2 : Analyse descriptive, visualisations et corrélations
│
├─ interfaces/                            # Contient tout ce qui est lié aux interfaces et backend
│ |─ database/                             # Stockage local pour les données utilisateurs
│   |─ etudiants.csv                        # Fichier CSV des étudiants ajoutés via l'application
│   └─ etudiants.db                         # Base de données SQLite pour persistance des données
│ |─ api_server.py                          # API Flask pour la gestion des étudiants et stockage des résultats
│ └─ api_streamlit.py                       # Application Streamlit pour le dashboard interactif et la prédiction
│
└─ README.md                               # Documentation complète du projet : instructions, objectifs, structure, etc.

 
 
---

## 🛠 Steps

1. *Generate Dataset*  
   Run generate_dataset.py to create a simulated student dataset.

2. *Data Analysis*  
   Use etape_2_analyse.ipynb to explore, visualize, and analyze the dataset.

3. *Predictive Modeling*  
   Use etape_3_modelisation.ipynb to train and evaluate machine learning models (XGBoost is used here).

4. *Dashboard & API*  
   - api_streamlit.py provides a web interface to input student data and predict success.  
   - api_server.py stores student data in a CSV or SQLite database.

---

## 📊 Features

- Dataset simulation with personal, academic, and behavioral data
- Data visualization and correlation analysis
- Predictive model for student success
- Real-time prediction dashboard with recommendations

---

## ⚡ Requirements

bash
pip install pandas numpy scikit-learn seaborn matplotlib joblib streamlit xgboost flask


---

⚖ Licence

This project is distributed under the MIT License — you are free to use it for educational or personal purposes, as long as the original author is credited.

---
⭐ Student Success Prediction: An intelligent and interactive tool to analyze and predict student outcomes.