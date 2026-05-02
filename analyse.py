from datetime import date                  #  AJOUT : pour afficher la date du rapport
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
 
# 1. CONFIGURATION DES DOSSIERS DE SORTIE


OUTPUT_DIR = "output"
TOP_N = 20          #  AJOUT : nombre de produits dans les graphiques Top N 
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"📁 Dossier de sortie : {os.path.abspath(OUTPUT_DIR)}/")
 
# 2. CHARGEMENT DU FICHIER CSV
CSV_PATH = "ventes.csv"
 
try:
    df = pd.read_csv(CSV_PATH)
    print(f"✅ Fichier '{CSV_PATH}' chargé — {len(df)} lignes trouvées.")
except FileNotFoundError:
    print(f"❌ Fichier '{CSV_PATH}' introuvable. Lance d'abord generate_data.py")
    sys.exit(1)
 
# 3. VALIDATION DES COLONNES REQUISES
COLONNES_REQUISES = ['ID', 'Prix', 'Quantite', 'Remise']
colonnes_manquantes = [c for c in COLONNES_REQUISES if c not in df.columns]
 
if colonnes_manquantes:
    print(f"❌ Colonnes manquantes dans le CSV : {colonnes_manquantes}")
    sys.exit(1)
 
 
# 4. CALCULS FINANCIERS

# CA Brut = Prix × Quantité (avant remise)
df['CA_Brut'] = df['Prix'] * df['Quantite']
 
# CA Net = CA Brut après application de la remise (%)
df['CA_Net'] = df['CA_Brut'] * (1 - df['Remise'] / 100)
 
# TVA à 20% calculée sur le CA Net
df['TVA'] = df['CA_Net'] * 0.20
 
# 5. STATISTIQUES RÉSUMÉES
total_ca_net   = round(df['CA_Net'].sum(), 2)
moyenne_ca_net = round(df['CA_Net'].mean(), 2)
nb_produits    = len(df)
max_id         = df.loc[df['CA_Net'].idxmax(), 'ID']
aujourd_hui    = date.today().strftime('%d/%m/%Y')   #  AJOUT : date du jour
 
print("\n" + "="*45)
print(f"    RAPPORT DU {aujourd_hui}")          
print("="*45)
print(f"  CA Net Total       : {total_ca_net} €")
print(f"  CA Net Moyen       : {moyenne_ca_net} €")
print(f"  Nombre de produits : {nb_produits}")
print(f"  Produit CA_Net max : {max_id}")
print("\n  🏆 Top 3 produits :")
top3 = df.sort_values(by='CA_Net', ascending=False).head(3)
print(top3[['ID', 'Prix', 'Quantite', 'Remise', 'CA_Net']].to_string(index=False))
print("="*45 + "\n")
 
# 6. EXPORT DES RÉSULTATS
# 6a. CSV complet avec tous les calculs
results_path = os.path.join(OUTPUT_DIR, "resultats_final.csv")
df.to_csv(results_path, index=False)
print(f" Résultats CSV exportés  → {results_path}")
 
# 6b.  AJOUT : résumé lisible en .txt 
summary_path = os.path.join(OUTPUT_DIR, "resume.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"Rapport du          : {aujourd_hui}\n")
    f.write(f"CA Net Total        : {total_ca_net} €\n")
    f.write(f"CA Net Moyen        : {moyenne_ca_net} €\n")
    f.write(f"Nombre de produits  : {nb_produits}\n")
    f.write(f"Top produit (CA max): {max_id}\n")
    f.write("\nTop 3 produits :\n")
    f.write(top3[['ID', 'Prix', 'Quantite', 'Remise', 'CA_Net']].to_string(index=False))
print(f"✅ Résumé texte exporté    → {summary_path}")
 

# 7. VISUALISATIONS AVEC PLOTLY 



 
#7a. TOP N produits — Bar chart horizontal 
# Sur un grand dataset, on affiche les TOP_N meilleurs produits par CA Net.
 
top_n_df = df.sort_values(by='CA_Net', ascending=False).head(TOP_N).copy()   
top_n_df['Couleur'] = top_n_df['CA_Net'].apply(
    lambda x: '🥇 Top produit' if x == top_n_df['CA_Net'].max() else 'Autres produits'
)
 
fig_bar = px.bar(
    top_n_df,
    x='CA_Net',
    y='ID',
    orientation='h',                      # horizontal = labels lisibles
    color='Couleur',
    color_discrete_map={
        '🥇 Top produit': '#e63946',
        'Autres produits': '#457b9d'
    },
    title=f"🏆 Top {TOP_N} Produits par CA Net — Total dataset : {nb_produits} produits",
    labels={'CA_Net': 'CA Net (€)', 'ID': 'ID Produit'},
    text='CA_Net',
    hover_data=['Prix', 'Quantite', 'Remise', 'CA_Brut', 'TVA']
)
fig_bar.update_traces(texttemplate='%{text:.2f} €', textposition='outside')
fig_bar.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=600,
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white'
)
bar_path = os.path.join(OUTPUT_DIR, f"top{TOP_N}_ca_net.html")              
fig_bar.write_html(bar_path)
print(f"✅ Bar chart Top {TOP_N}    → {bar_path}")
 
# 7b. Pie chart  
# Sur un grand dataset, un pie avec 1000 parts est illisible.

 
top_pie    = df.nlargest(TOP_N // 2, 'CA_Net').copy()                      
ca_autres  = df['CA_Net'].sum() - top_pie['CA_Net'].sum()
autres_row = pd.DataFrame({'ID': ['Autres'], 'CA_Net': [ca_autres]})
pie_df     = pd.concat([top_pie[['ID', 'CA_Net']], autres_row], ignore_index=True)
 
fig_pie = px.pie(
    pie_df,
    values='CA_Net',
    names='ID',
    title=f"📊 Répartition CA Net — Top {TOP_N // 2} + Autres ({nb_produits} produits au total)",
    hole=0.35,              # donut chart 
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
pie_path = os.path.join(OUTPUT_DIR, "ca_pie.html")
fig_pie.write_html(pie_path)
print(f"✅ Pie chart           → {pie_path}")
 
#  7c. Histogramme de distribution du CA Net

 
fig_hist = px.histogram(
    df,
    x='CA_Net',
    nbins=30,               # 30 classes — ajustable selon la densité
    title=f" Distribution du CA Net ({nb_produits} produits)",
    labels={'CA_Net': 'CA Net (€)', 'count': 'Nombre de produits'},
    color_discrete_sequence=['#2a9d8f'],
    marginal='box',         # boxplot en marge pour voir médiane 
    hover_data=df.columns
)
fig_hist.update_layout(
    bargap=0.05,
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white'
)
hist_path = os.path.join(OUTPUT_DIR, "ca_distribution.html")
fig_hist.write_html(hist_path)
print(f" Histogramme         → {hist_path}")
 
#7d. Scatter plot — Prix vs CA_Net 

 
fig_scatter = px.scatter(
    df,
    x='Prix',
    y='CA_Net',
    color='Remise',             
    size='Quantite',             
    hover_name='ID',
    title=f"🔍 Prix vs CA Net — Taille = Quantité, Couleur = Remise ({nb_produits} produits)",
    labels={'Prix': 'Prix unitaire (€)', 'CA_Net': 'CA Net (€)', 'Remise': 'Remise (%)'},
    color_continuous_scale='RdYlGn_r',
    opacity=0.7
)
fig_scatter.update_layout(
    plot_bgcolor='#f8f9fa',
    paper_bgcolor='white'
)
scatter_path = os.path.join(OUTPUT_DIR, "prix_vs_ca_scatter.html")
fig_scatter.write_html(scatter_path)
print(f"✅ Scatter plot        → {scatter_path}")
 
#  7e. Dashboard résumé (4 graphiques combinés en un seul fichier)
 
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        f"Top {TOP_N // 2} CA Net",                                          
        f"Répartition CA Net (Top {TOP_N // 2})",
        "Distribution CA Net",
        "Prix vs CA Net"
    ),
    specs=[
        [{"type": "bar"},        {"type": "pie"}],
        [{"type": "histogram"},  {"type": "scatter"}]
    ]
)
 
# subplot 1 : bar top N/2
top_pie_sorted = top_pie.sort_values('CA_Net', ascending=True)
fig_dashboard.add_trace(
    go.Bar(x=top_pie_sorted['CA_Net'], y=top_pie_sorted['ID'].astype(str),
           orientation='h', marker_color='#457b9d', name='CA Net'),
    row=1, col=1
)
 
# subplot 2 : pie
fig_dashboard.add_trace(
    go.Pie(values=pie_df['CA_Net'], labels=pie_df['ID'].astype(str),
           hole=0.35, showlegend=False),
    row=1, col=2
)
 
# subplot 3 : histogramme
fig_dashboard.add_trace(
    go.Histogram(x=df['CA_Net'], nbinsx=20, marker_color='#2a9d8f', name='Distribution'),
    row=2, col=1
)
 
# subplot 4 : scatter
fig_dashboard.add_trace(
    go.Scatter(x=df['Prix'], y=df['CA_Net'], mode='markers',
               marker=dict(size=5, color=df['Remise'], colorscale='RdYlGn_r',
                           opacity=0.6, showscale=True),
               name='Produits'),
    row=2, col=2
)
 
fig_dashboard.update_layout(
    title_text=f"📊 Dashboard Ventes — {nb_produits} produits | CA Net Total : {total_ca_net:,.2f} € | {aujourd_hui}",
    height=800,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='#f8f9fa'
)
 
dashboard_path = os.path.join(OUTPUT_DIR, "dashboard.html")
fig_dashboard.write_html(dashboard_path)
print(f"✅ Dashboard complet   → {dashboard_path}")
 

# 8. RÉSUMÉ FINAL
print("\n" + "="*45)
print("  ✅ Analyse terminée avec succès !")
print(f"  📂 Tous les fichiers sont dans : {OUTPUT_DIR}/")
print("     ├── resultats_final.csv")
print("     ├── resume.txt")                        # ✅ AJOUT
print(f"    ├── top{TOP_N}_ca_net.html")
print("     ├── ca_pie.html")
print("     ├── ca_distribution.html")
print("     ├── prix_vs_ca_scatter.html")
print("     └── dashboard.html")
print("="*45)
 