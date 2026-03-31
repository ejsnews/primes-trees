import sqlite3
import json
import math

def generate_primalux_json(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Extraction des 694 arbres
    cursor.execute("SELECT * FROM trees_metadata_3")
    rows = cursor.fetchall()
    
    game_data = []

    for row in rows:
        raw_branches = row['nb_branches']
        nb_branches = int(raw_branches) if raw_branches is not None else 0
        # Sécurité : On ne traite que les arbres qui ont au moins 1 branche
        if nb_branches > 0:
            root = math.isqrt(nb_branches)
            is_stable = (root * root == nb_branches)
            # Logique de tri pour le Panthéon
            is_singularity = (nb_branches in [16, 25, 36, 49, 64]) # le 81 = fin de partie
            is_codex =  (nb_branches in [77, 78, 80, 81]) # 4 codex de victoire 0_4, 0_3, 0_2, 0_1
            # ... le reste de ton calcul ...
        else:
            # Optionnel : loguer l'erreur ou passer à l'arbre suivant
            continue
        # Calcul de la stabilité selon ta récurrence (n^2)
        rootA = math.isqrt(row['A'])
        is_stable_A = (rootA * rootA == row['A'])
        
        root = math.isqrt(nb_branches)
        is_stable_br = (root * root == nb_branches)
        next_stable = (root + 1) ** 2
        #bonus = ((root + 1) ** 2 - (root) ** 2) * nb_branches  # 2 * root + 1
        bonus = round(0.2 * row['mean_density'] * nb_branches, 0)
        missing_to_fusion = next_stable - nb_branches
        
        # Détermination du coût en Neutrinos (formule EJS)
        # Plus il y a de feuilles (premiers), plus le coût de création est élevé
        creation_cost = (nb_branches * 100) + (row['nb_leaves'] * 10)
         
        tree_entry = {
            "coords": {"A": row['A'], "B": row['B']},
            "name": row['name_poetic_fr'],
            "name_scientific": row['name_scientific'],
            "family": row['family_fr'],
            "tree_value_A": row['A'],
            "tree_value_br": int(math.isqrt(nb_branches)),
            "nano_banana_prompt": row['nano_banana_prompt'],
            "stats": {
                "branches": nb_branches,
                "neutrinos": round(row['mean_density'], 0) * nb_branches,  # Les neutrinos de l'arbre relies aux branches
                "nb_leaves": round(row['nb_leaves'], 0),
                "density": round(row['mean_density'], 0)
            },
            "game_logic": {
                "is_stable_A": is_stable_A,
                "is_stable_br": is_stable_br,
                "is_stable": is_stable_br or is_stable_A,
                "missing_to_fusion": missing_to_fusion,
                "neutrino_cost": creation_cost,
                "role": "Singularity" if is_singularity else "Common_Tree",
                "victory": "Codex" if is_codex else "Common_Tree",
                "fusion_bonus": (bonus) if is_singularity else 0, # Le paquet virtuel de neutrinos
                "tax_multiplier": 10 if is_singularity else 1, # Explosion du pouvoir des taxes
                "gravity_tax": round(row['mean_density'] * 5, 0),
                "is_potential_tn": row['nb_leaves'] > 1000 # Seuil pour devenir un TN
            }
        }
        game_data.append(tree_entry)
        
    # Sauvegarde
    with open('prima_lux_logic.json', 'w', encoding='utf-8') as f:
        json.dump(game_data, f, indent=4, ensure_ascii=False)
        
    print(f"Extraction réussie : {len(game_data)} structures prêtes pour le sac.")

generate_primalux_json('formules.db')
