from flask import Flask, request, jsonify
import sqlite3
import joblib
import pandas as pd
import os

app = Flask(__name__)

# -------------------------------
# Charger le modèle ML
# -------------------------------
model_path = "../modeles_sauvegardes/xgboost_model.pkl"
model = joblib.load(model_path)

# -------------------------------
# Créer le dossier et la base SQLite si inexistants
# -------------------------------
db_folder = "database"
db_path = os.path.join(db_folder, "etudiants.db")

if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# -------------------------------
# Créer la table si inexistante
# -------------------------------
conn = sqlite3.connect(db_path)
conn.execute("""
CREATE TABLE IF NOT EXISTS etudiants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    type_bac TEXT,
    parcours TEXT,
    moyenne_bac REAL,
    moyenne_s1 REAL,
    moyenne_s2 REAL,
    moyenne_generale REAL,
    nb_modules_echoues INTEGER,
    heures_travail_semaine REAL,
    discipline_note_sur_5 REAL,
    satisfaction_parcours_note_sur_5 REAL,
    travail_parallele TEXT,
    prediction INTEGER
)
""")
conn.close()

# -------------------------------
# Colonnes attendues par le modèle
# -------------------------------
model_columns = [
    "age", "moyenne_bac", "moyenne_s1", "moyenne_s2", "moyenne_generale",
    "nb_modules_echoues", "heures_travail_semaine", "discipline_note_sur_5",
    "satisfaction_parcours_note_sur_5", "travail_parallele", "type_bac", "parcours"
]

# -------------------------------
# Route pour ajouter un étudiant
# -------------------------------
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()

    # Compléter les colonnes manquantes
    for col in model_columns:
        if col not in data:
            if col in ["travail_parallele", "type_bac", "parcours"]:
                data[col] = "Non spécifié"
            else:
                data[col] = 0

    # Préparer le DataFrame pour le modèle
    df = pd.DataFrame([[data[col] for col in model_columns]], columns=model_columns)
    prediction = int(model.predict(df)[0])
    data["prediction"] = prediction

    # Enregistrer dans la DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO etudiants (
            age, type_bac, parcours, moyenne_bac, moyenne_s1, moyenne_s2, moyenne_generale,
            nb_modules_echoues, heures_travail_semaine, discipline_note_sur_5,
            satisfaction_parcours_note_sur_5, travail_parallele, prediction
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["age"], data["type_bac"], data["parcours"], data["moyenne_bac"],
        data["moyenne_s1"], data["moyenne_s2"], data["moyenne_generale"],
        data["nb_modules_echoues"], data["heures_travail_semaine"],
        data["discipline_note_sur_5"], data["satisfaction_parcours_note_sur_5"],
        data["travail_parallele"], data["prediction"]
    ))
    conn.commit()
    conn.close()

    # -------------------------------
    # Exporter automatiquement en CSV
    # -------------------------------
    conn = sqlite3.connect(db_path)
    df_export = pd.read_sql_query("SELECT * FROM etudiants", conn)
    conn.close()

    csv_path = os.path.join(db_folder, "etudiants.csv")
    df_export.to_csv(csv_path, index=False)

    return jsonify({
        "message": "Étudiant ajouté avec succès",
        "prediction": prediction,
        "csv": csv_path
    })

# -------------------------------
# Route pour récupérer tous les étudiants
# -------------------------------
@app.route("/get_students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM etudiants", conn)
    conn.close()
    return df.to_json(orient="records")

# -------------------------------
# Route pour exporter CSV manuellement
# -------------------------------
@app.route("/export_csv", methods=["GET"])
def export_csv():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM etudiants", conn)
    conn.close()

    csv_path = os.path.join(db_folder, "etudiants.csv")
    df.to_csv(csv_path, index=False)

    return jsonify({"message": f"Fichier CSV créé : {csv_path}"})

# -------------------------------
# Route racine pour test navigateur
# -------------------------------
@app.route("/", methods=["GET"])
def index():
    return "<h2>API Flask pour Dashboard Réussite Étudiante</h2>"

# -------------------------------
# Lancer le serveur
# -------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
