import csv
import random

with open('ventes.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # écrire les colonnes
    writer.writerow(['ID', 'Prix', 'Quantite', 'Remise'])
    
    for i in range(101, 116):
        prix = round(random.uniform(5.0, 100.0), 2)
        quantite = random.randint(1, 10)
        remise = random.choice([0, 5, 10, 15, 20])
        
        writer.writerow([i, prix, quantite, remise])

print("Fichier ventes.csv créé !")