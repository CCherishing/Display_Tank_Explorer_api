from flask import Flask, jsonify
from flask_cors import CORS
from creatures import load_species_from_csv
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Data_Dir = os.path.join(Base_Dir, "data")
species_csv = os.path.join(Data_Dir,"display_tank_species_data.csv")

species = load_species_from_csv(species_csv)


app = Flask(__name__)
CORS(app)

@app.route("/creatures")
def get_creatures():
    return jsonify(species)

@app.route("/creatures/<creature_id>")
def get_creature(creature_id):
    for c in species:
        if c["id"] == creature_id:
            return jsonify(c)
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
