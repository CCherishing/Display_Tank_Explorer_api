# Display Tank Explorer API – Adding New Species

This document explains how to add new species to the Display Tank Explorer

## Overview

Species data is stored in a CSV file and loaded by the Flask backend. The frontend calls the API to render sprites and show details.

High-level steps:

1. Prepare sprite image(s) then add to the *images* folder
2. Edit the CSV to add a new row for your species and fill out all the relevant information (including x and y position)
3. Commit everything to github and wait for render to redeploy

---

## 1. Species CSV structure

The CSV file is:

- Located at: `data/display_tank_species_data.csv`
- Loaded by: `species.py` → `load_species_from_csv`

Example column layout (you may have more columns, but these are the important ones):

```text
id,common_name,scientific_name,description,habitat_info,s_image,native_status,fun_fact,sprite,x,y
1,Periwinkle,Littorina littorea,"Small marine snail...", "Rocky intertidal",periwinkle.png,Native,"Fun fact about periwinkles",periwinkle_sprite.png,25,60
```

**Field meanings:**

- `id` (required, integer)  
  Unique numeric identifier for the species. Used in routes like `/species/1`.

- `common_name` (required, string)  
  Human-friendly species name (e.g. `Periwinkle`, `Manila Clam`).

- `scientific_name` (optional, string)  
  Latin binomial name.

- `description` (optional, string)  
  Main description text.

- `habitat_info` (optional, string)  
  Short description of habitat/environment.

- `s_image` (optional, string)  
  Small image filename used in UI or thumbnails (if applicable).

- `native_status` (optional, string)  
  e.g. `Native`, `Introduced`, etc.

- `fun_fact` (optional, string)  
  A fun piece of trivia displayed in the UI.

- `sprite` (optional, string)  
  Filename of the sprite image for rendering in the tank.

- `x` (optional, number)  
  Horizontal position of the sprite in the tank, as a percentage of tank width (0–100). `0` is left, `100` is right.

- `y` (optional, number)  
  Vertical position of the sprite in the tank, as a percentage of tank height (0–100). `0` is top, `100` is bottom.

---

## 2. Adding a new species

1. **Pick a new `id`**

   - Find the highest existing `id` in the CSV.
   - Use the next integer (e.g. if highest is 15, use `16`).
   - `id` **must be unique**.

2. **Choose names**

   - `common_name`: e.g. `Periwinkle`, `Manila Clam`.
   - `scientific_name`: optional but recommended, e.g. `Littorina littorea`.

3. **Write text fields**

   - `description`: 1–3 sentences describing the species.
   - `habitat_info`: e.g. `"Rocky intertidal"`, `"Sandy subtidal flats"`.
   - `fun_fact`: a short, engaging fact.

4. **Prepare sprite and images**

   - Save a sprite image file, e.g. `periwinkle_sprite.png`.
   - Save any popup/thumbnail image as needed, e.g. `periwinkle.png`.
   - Place these in the frontend’s `images/` directory (e.g. `Display_Tank_Explorer_site/images`).
   - Ensure the `sprite` and `s_image` columns exactly match the filenames (case-sensitive).

5. **Set sprite position**

   - Decide where in the tank you want the sprite:
     - `x` between 0 and 100 → left to right
     - `y` between 0 and 100 → top to bottom
   - Example:
     - Near bottom-left: `x = 20`, `y = 80`
     - Near center: `x = 50`, `y = 50`

6. **Add the row to the CSV**

   Example for a new species:

   ```text
   16,Manila Clam,Venerupis philippinarum,"A burrowing clam found in sandy or muddy substrates.","Sandy subtidal flats",manila_clam.png,Introduced,"Often farmed in aquaculture.",manila_clam_sprite.png,60,85
   ```

   - Note: commas within text fields should be quoted: `"A burrowing clam, often farmed..."`.

---

## 3. Redeploying and verifying

After editing the CSV:

1. Commit and push your changes to the GitHub repo.
2. If your Render.com service is connected to the repo:
   - Trigger a deploy by pushing to the branch Render is watching (e.g. `main`).
   - Or use the Render dashboard to manually redeploy.

### 3.2. Verify via API

Once deployed, visit:

- `https://display-tank-explorer-api.onrender.com/species`  
  → Should include the new species in the list.

- `https://display-tank-explorer-api.onrender.com/species/16`  
  → Should return the JSON object for your new species.

If name-based lookup is implemented (see below):

- `https://display-tank-explorer-api.onrender.com/species/periwinkle`
- `https://display-tank-explorer-api.onrender.com/species/manila%20clam`

---

## 4. Name-based lookup behavior

The backend supports both:

- **ID-based:** `/species/1`
- **Name-based:** `/species/periwinkle`, `/species/manila clam` (URL-encoded as `%20`)

Implementation details:

- Routes accept either:
  - An integer path segment (ID), or
  - A string path segment (common name).
- Common names are matched **case-insensitively** and **space-normalized**.
  - For example, `Manila Clam`, `manila clam`, and `MANILA   CLAM` all resolve to the same species.
- Multi-word species are handled by converting:
  - all names to lowercase
  - collapsing multiple spaces to a single space

---

## 5. Troubleshooting

- **Sprite not visible**
  - Check that the `sprite` filename matches a real file in `Display_Tank_Explorer_site/images`.
  - Confirm that `x` and `y` are within 0–100.
  - Open browser dev tools → Network tab → ensure the sprite image is loaded with HTTP 200.

- **Species not on render**
  - Verify the CSV row is syntactically correct (columns aligned, quotes balanced).
  - Check backend logs (on VSCode) for “Skipping species row, parse error” messages.
  - Ensure the service on Render has redeployed successfully. May need to manually redeploy latest commit. (click manually deploy)

- **Name-based lookup not working**
  - Confirm the `common_name` is non-empty in the CSV.
  - Try lowercasing and removing extra spaces in the browser query.

---

## 6. Where to look in the code

- **CSV loading and structure:** `species.py`
- **Flask routes & JSON responses:** `app.py`
- **Frontend rendering and layout:** `Display_Tank_Explorer_site/script.js`, `style.css`

If you add or rename CSV columns, ensure `species.py` is updated accordingly so the new data is available to the API and frontend.
