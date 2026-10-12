import os
import pandas as pd
import matplotlib.pyplot as plt

# Cree le dossier pour les graphiques s'il n'existe pas
os.makedirs("graphiques", exist_ok=True)

# CHARGER LES DONNEES
df = pd.read_csv("stats_dvf.csv")
print("Lignes et colonnes :", df.shape)
print("Colonnes :", list(df.columns))

#GARDER UNE SEULE ECHELLE (les departements)
print(df["echelle_geo"].value_counts())
df = df[df["echelle_geo"] == "departement"]

# NETTOYER

# Transformer le texte "2020-05" en vraie date
df["date"] = pd.to_datetime(df["annee_mois"])
df["annee"] = df["date"].dt.year
df["mois"] = df["date"].dt.month

# Enlever les lignes sans prix ou avec un prix impossible
df = df.dropna(subset=["med_prix_m2_apt_maison"])
df = df[df["med_prix_m2_apt_maison"] > 0]
df = df.drop_duplicates()
print("Lignes apres nettoyage :", len(df))

#STATISTIQUES DE BASE
prix = df["med_prix_m2_apt_maison"]
print("\nPrix median au m2 :", round(prix.median()))
print("Prix moyen au m2  :", round(prix.mean()))
print("Prix minimum :", prix.min(), "| Prix maximum :", prix.max())

# TOP 10 DES DEPARTEMENTS LES PLUS CHERS
top10 = df.groupby("libelle_geo")["med_prix_m2_apt_maison"].mean()
top10 = top10.sort_values(ascending=False).head(10)
print("\nTop 10 des plus chers :")
print(top10.round(0))

# EVOLUTION PAR ANNEE
par_annee = df.groupby("annee")["med_prix_m2_apt_maison"].median()
print("\nPrix median par annee :")
print(par_annee.round(0))

premiere = par_annee.iloc[0]
derniere = par_annee.iloc[-1]
evolution = (derniere - premiere) / premiere * 100
print(f"\nEvolution entre {par_annee.index[0]} et {par_annee.index[-1]} : {evolution:.1f} %")

# GRAPHIQUES
# Graphique 1 : evolution du prix
plt.figure(figsize=(8, 4))
plt.plot(par_annee.index, par_annee.values, marker="o")
plt.title("Evolution du prix median au m2")
plt.xlabel("Annee")
plt.ylabel("Prix (EUR/m2)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("graphiques/evolution.png")
plt.close()

# Graphique 2 : top 10 des departements
plt.figure(figsize=(8, 5))
top10.sort_values().plot(kind="barh")
plt.title("Top 10 des departements les plus chers")
plt.xlabel("Prix (EUR/m2)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graphiques/top10.png")
plt.close()

# Graphique 3 : distribution des prix
plt.figure(figsize=(8, 4))
plt.hist(prix, bins=30, edgecolor="white")
plt.title("Distribution du prix au m2")
plt.xlabel("Prix (EUR/m2)")
plt.ylabel("Nombre d'observations")
plt.tight_layout()
plt.savefig("graphiques/distribution.png")
plt.close()



# Quel departement a le prix minimum
dep_prix_min= df.loc[df["med_prix_m2_apt_maison"].idxmin()]
print("Prix minimum: ")
print(dep_prix_min[["libelle_geo", "annee_mois", "med_prix_m2_apt_maison"]])

# Prix de la Creuse sur 5 ans
creuse=df[df["libelle_geo"]=="Creuse"]
print(creuse["med_prix_m2_apt_maison"].describe())

# Les 10 départements les moins chers sur 5 ans
prix_bas10=df.groupby("libelle_geo")["med_prix_m2_apt_maison"].mean()
print("Les 10 departements le moins chers: ")
print(prix_bas10.sort_values().head(10).round(0))

