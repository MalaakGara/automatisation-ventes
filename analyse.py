import pandas as pd

# lire le fichier
try:
    df = pd.read_csv('ventes.csv')
except FileNotFoundError:
    print("❌ fichier ventes.csv introuvable")
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

# produit avec CA max
max_id = df.loc[df['CA_Net'].idxmax(), 'ID']
print("Produit avec CA_Net max :", max_id)
df.to_csv('resultats_final.csv', index=False)
import matplotlib.pyplot as plt

# graphique
colors = ['blue'] * len(df)
max_index = df['CA_Net'].idxmax()
colors[max_index] = 'red'

plt.bar(df['ID'], df['CA_Net'], color=colors)
plt.title("CA Net par produit")
plt.xlabel("ID Produit")
plt.ylabel("CA Net")

plt.savefig("ca_par_produit.png")
plt.show()
