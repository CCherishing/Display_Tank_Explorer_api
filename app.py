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

# Make species_id an integer converter and compare numerically
@app.route("/species/<int:species_id>")
def get_specie(species_id):
    for c in species:
        # c["id"] should be an int from CSV parsing; compare numerically
        if c.get("id") == species_id:
            return jsonify(c)
    return jsonify({"error": "Not found"}), 404
#Makes species name usable on render
@app.route("/species/<path:species_name>")
def get_specie_by_name(species_name):
    """
    Lookup species by common_name (case-insensitive, space-normalized).

    Examples:
      /species/periwinkle
      /species/Periwinkle
      /species/manila%20clam
    """
    # Normalize the URL segment: lowercase and collapse multiple spaces
    normalized_query = " ".join(species_name.lower().split())

    for c in species:
        common = (c.get("common_name") or "").strip().lower()
        normalized_common = " ".join(common.split())
        if normalized_common == normalized_query:
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
