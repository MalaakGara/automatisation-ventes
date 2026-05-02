import csv
import random
import sys
import os
 
# -----------------------------------------------------------------------------
# PARAMÈTRES DE GÉNÉRATION
# -----------------------------------------------------------------------------
NB_LIGNES_DEFAULT = 1000
 
# Récupère le nombre de lignes depuis l'argument en ligne de commande
if len(sys.argv) > 1:
    try:
        nb_lignes = int(sys.argv[1])
        if nb_lignes <= 0:
            raise ValueError
    except ValueError:
        print("  Argument invalide. Utilisation du défaut :", NB_LIGNES_DEFAULT)
        nb_lignes = NB_LIGNES_DEFAULT
else:
    nb_lignes = NB_LIGNES_DEFAULT
 
# -----------------------------------------------------------------------------
# GÉNÉRATION DU FICHIER CSV
# -----------------------------------------------------------------------------
CSV_PATH = "ventes.csv"
 
with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
 
    # En-tête du CSV
    writer.writerow(['ID', 'Prix', 'Quantite', 'Remise'])
 
    for i in range(1, nb_lignes + 1):
        produit_id = f"P-{i:05d}"
        prix       = round(random.uniform(5.0, 500.0), 2)
        quantite   = random.randint(1, 50)
        remise     = random.choice([0, 5, 10, 15, 20, 25, 30])
 
        writer.writerow([produit_id, prix, quantite, remise])
 
taille_fichier = os.path.getsize(CSV_PATH)
print(f" Fichier '{CSV_PATH}' généré avec succès !")
print(f"   → {nb_lignes} produits | {taille_fichier / 1024:.1f} Ko")
print(f"\n▶  Lance maintenant : python analyse.py")