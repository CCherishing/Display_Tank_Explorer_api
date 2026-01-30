import os
import csv

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
                    "sprite": sprite.strip('"'),
                    "x": float(row.get("x", 0)) / 10.0 if row.get("x") else 0.0,
                    "y": float(row.get("y", 0)) /10.0 if row.get("y") else 0.0
                })
            except Exception as e:
                print("Skipping species row, parse error:", e, row)
    return species
