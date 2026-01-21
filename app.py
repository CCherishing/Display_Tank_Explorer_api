from flask import Flask, jsonify
from flask_cors import CORS
from species import load_species_from_csv
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Data_Dir = os.path.join(Base_Dir, "data")
species_csv = os.path.join(Data_Dir,"display_tank_species_data.csv")

species = load_species_from_csv(species_csv)
print("Loaded species count:", len(species))

app = Flask(__name__)
CORS(app)

@app.route("/species")
def get_species():
    return jsonify(species)

@app.route("/species/<species_id>")
def get_specie(species_id):
    for c in species:
        if c["id"] == species_id:
            return jsonify(c)
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "api": "Display Tank Explorer"
    })
