import os
import csv
import pygame

# Returns list of dictionaries from species csv
def load_species_from_csv(path):
    """Load species rows from CSV. Expect x,y and sprite columns.
    Returns list of dicts."""
    species = []
    if not os.path.exists(path):
        print("Species CSV not found:", path)
        return species

    with open(path, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            try:
                sid = int(row["id"])
                sprite = row.get("sprite", "").strip() if row.get("sprite") else ""
                species.append({
                    "id": sid,
                    "common_name": row.get("common_name", "").strip().strip('"') if row.get("common_name") else "",
                    "scientific_name": row.get("scientific_name", "").strip().strip('"') if row.get("scientific_name") else "",
                    "description": row.get("description", "").strip().strip('"') if row.get("description") else "",
                    "habitat_info": row.get("habitat_info", "").strip().strip('"') if row.get("habitat_info") else "",
                    "s_image": row.get("s_image", "").strip().strip('"') if row.get("s_image") else "",
                    "native_status": row.get("native_status", "").strip().strip('"') if row.get("native_status") else "",
                    "fun_fact": row.get("fun_fact", "").strip().strip('"') if row.get("fun_fact") else "",
                    "sprite": sprite.strip('"')
                })
            except Exception as e:
                print("Skipping species row, parse error:", e, row)
    return species

_species_objects = []

def prepare_species_objects(species_csv):
    global _species_objects
    species_list = load_species_from_csv(species_csv)

    # Load sprites and create objects
    _species_objects.clear()
    for sp in species_list:
        sprite_path = sp.get("sprite")
        obj = {
            "id": sp["id"],
            "common_name": sp["common_name"],
            "scientific_name": sp["scientific_name"],
            "description": sp["description"],
            "habitat_info": sp["habitat_info"],
            "s_image": sp.get("s_image", ""),
            "native_status": sp.get("native_status", ""),
            "fun_fact": sp.get("fun_fact", ""),
            "sprite_path": sprite_path,
        }
        _species_objects.append(obj)

    return _species_objects

#test run
