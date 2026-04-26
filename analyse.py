import pandas as pd

# lire le fichier
try:
    df = pd.read_csv('ventes.csv')
except FileNotFoundError:
    print("❌ fichier ventes.csv introuvable")
    exit()

colonnes = ['ID', 'Prix', 'Quantite', 'Remise']
if not all(col in df.columns for col in colonnes):
    print("❌ colonnes manquantes")
    exit() 
    
# calculs
df['CA_Brut'] = df['Prix'] * df['Quantite']
df['CA_Net'] = df['CA_Brut'] * (1 - df['Remise'] / 100)
df['TVA'] = df['CA_Net'] * 0.20

# afficher
print(df.head())
# CA Net total
total = round(df['CA_Net'].sum(), 2)
print("CA Net Total :", total)
print("CA moyen :", round(df['CA_Net'].mean(), 2))
print("Nombre de produits :", len(df))
print("Top 3 produits :")
print(df.sort_values(by='CA_Net', ascending=False).head(3))

# produit avec CA max
max_id = df.loc[df['CA_Net'].idxmax(), 'ID']
print("Produit avec CA_Net max :", max_id)
df.to_csv('resultats_final.csv', index=False)
print("✅ Fichier resultats_final.csv créé") 

import matplotlib.pyplot as plt

# graphique
colors = ['blue'] * len(df)
max_index = df['CA_Net'].idxmax()
colors[max_index] = 'red'

plt.figure(figsize=(10,5))
plt.xticks(rotation=45)
plt.bar(df['ID'], df['CA_Net'], color=colors)

plt.title("CA Net par produit")
plt.xlabel("ID Produit")
plt.ylabel("CA Net")

plt.savefig("ca_par_produit.png")
plt.show()
print("✅ Graphique enregistré")