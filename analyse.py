import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Charger le fichier CSV
df = pd.read_csv("data/Mall_Customers.csv")

# Afficher les 5 premières lignes
print(df.head())

# Informations générales sur le DataFrame
print(df.info())

# Statistiques descriptives
print(df.describe())

# Répartition des clients par genre
print(df["Genre"].value_counts())

# Pourcentage des clients par genre
pourcentage_genre = df["Genre"].value_counts(normalize=True) * 100

print(pourcentage_genre)

# Revenu annuel moyen par genre
revenu_moyen_genre = df.groupby("Genre")["Annual Income (k$)"].mean()

print(revenu_moyen_genre)

# Score de dépense moyen par genre
score_moyen_genre = df.groupby("Genre")["Spending Score (1-100)"].mean()

print(score_moyen_genre)

# Créer des tranches d'âge
tranches_age = [17, 25, 35, 45, 55, 70]
labels_age = ["18-25", "26-35", "36-45", "46-55", "56-70"]

df["Tranche_age"] = pd.cut(
    df["Age"],
    bins=tranches_age,
    labels=labels_age
)

# Nombre de clients par tranche d'âge
print(df["Tranche_age"].value_counts().sort_index())

# Revenu et score de dépense moyens par tranche d'âge
analyse_age = df.groupby("Tranche_age", observed=True)[
    ["Annual Income (k$)", "Spending Score (1-100)"]
].mean()

print(analyse_age)

# Corrélation entre le revenu et le score de dépense
correlation = df["Annual Income (k$)"].corr(
    df["Spending Score (1-100)"]
)

print("Corrélation revenu / score de dépense :", correlation)

# Variables utilisées pour la segmentation
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

print(X.head())

# Méthode du coude
inerties = []

for k in range(1, 11):
    modele = KMeans(n_clusters=k, random_state=42, n_init=10)
    modele.fit(X)
    inerties.append(modele.inertia_)

print("Inerties :", inerties)

# Création du modèle K-Means avec 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

# Entraînement du modèle
kmeans.fit(X)

# Ajouter le numéro du cluster à chaque client
df["Cluster"] = kmeans.labels_

print(df[[
    "CustomerID",
    "Annual Income (k$)",
    "Spending Score (1-100)",
    "Cluster"
]].head(10))

# Profil moyen de chaque cluster
profil_clusters = df.groupby("Cluster")[
    ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
].mean()

print("Profil moyen des clusters :")
print(profil_clusters)

# Nom / profil de chaque cluster
noms_clusters = {
    0: "Revenu moyen / dépenses moyennes",
    1: "Revenu élevé / dépenses élevées",
    2: "Revenu faible / dépenses élevées",
    3: "Revenu élevé / dépenses faibles",
    4: "Revenu faible / dépenses faibles"
}

# Nombre de clients par cluster
nombre_clients_cluster = df["Cluster"].value_counts().sort_index()

# Pourcentage de clients par cluster
pourcentage_clusters = (
    nombre_clients_cluster / len(df) * 100
)

# Création du tableau récapitulatif
resume_clusters = profil_clusters.copy()

resume_clusters["Nombre de clients"] = nombre_clients_cluster
resume_clusters["Pourcentage (%)"] = pourcentage_clusters
resume_clusters["Profil"] = resume_clusters.index.map(noms_clusters)

# Arrondir les valeurs numériques
resume_clusters["Age"] = resume_clusters["Age"].round(1)
resume_clusters["Annual Income (k$)"] = resume_clusters["Annual Income (k$)"].round(1)
resume_clusters["Spending Score (1-100)"] = resume_clusters["Spending Score (1-100)"].round(1)
resume_clusters["Pourcentage (%)"] = resume_clusters["Pourcentage (%)"].round(1)

# Réorganiser les colonnes
resume_clusters = resume_clusters[
    [
        "Nombre de clients",
        "Pourcentage (%)",
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)",
        "Profil"
    ]
]

print("Résumé final des clusters :")
print(resume_clusters)













# Visualisation des clusters
plt.scatter(
    X["Annual Income (k$)"],
    X["Spending Score (1-100)"],
    c=df["Cluster"]
)

# Afficher les centres des clusters
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    marker="X",
    s=200,
    edgecolor="black",
    label="Centres"
)

plt.xlabel("Revenu annuel (k$)")
plt.ylabel("Score de dépense")
plt.title("Segmentation des clients par K-Means")

plt.legend()

plt.savefig("images/clusters_clients.png")

plt.show()

# Courbe du coude
plt.plot(range(1, 11), inerties, marker="o")

plt.xlabel("Nombre de clusters (K)")
plt.ylabel("Inertie")
plt.title("Méthode du coude")

plt.savefig("images/methode_du_coude.png")

plt.show()
print("Inerties :", inerties)