import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



# Configuration de la page
st.set_page_config(
    page_title="Segmentation des clients",
    page_icon="📊",
    layout="wide"
)

# Titre du dashboard
st.title("📊 Segmentation des clients")

st.write(
    "Analyse des profils clients à l'aide de la méthode K-Means."
)

# Charger les données
df = pd.read_csv("data/Mall_Customers.csv")


# Sélectionner les données utilisées pour la segmentation
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

# Créer 5 groupes de clients
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

# Ajouter le groupe de chaque client
df["Cluster"] = kmeans.fit_predict(X)



# ==============================
# INDICATEURS KPI
# ==============================

st.subheader("📊 Indicateurs clés")

# Calcul des indicateurs

clusters = sorted(df["Cluster"].unique())

cluster_choisi = st.selectbox(
    "Choisis un groupe de clients :",
    ["Tous les clients"] + clusters
)

if cluster_choisi == "Tous les clients":
    df_filtre = df
else:
    df_filtre = df[df["Cluster"] == cluster_choisi]
nombre_clients = len(df_filtre)
revenu_moyen = df_filtre["Annual Income (k$)"].mean()
score_moyen = df_filtre["Spending Score (1-100)"].mean()
nombre_clusters = df_filtre["Cluster"].nunique()

# Création des 4 colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Nombre de clients", nombre_clients)

with col2:
    st.metric("💰 Revenu moyen", f"{revenu_moyen:.2f} k$")

with col3:
    st.metric("🛍️ Score moyen", f"{score_moyen:.2f}/100")

with col4:
    st.metric("🔵 Nombre de clusters", nombre_clusters)


# Afficher les données filtrées
st.subheader("📋 Données des clients")
st.dataframe(df_filtre)


# Interprétation du groupe sélectionné
st.subheader("🗣️ Comprendre le profil des clients")

if cluster_choisi == "Tous les clients":
    st.info(
        "Vue générale : les clients sont répartis en cinq groupes "
        "selon leur revenu annuel et leur score de dépense. "
        "Cette segmentation permet de comparer différents profils."
    )
else:
    revenu = df_filtre["Annual Income (k$)"].mean()
    score = df_filtre["Spending Score (1-100)"].mean()

    if revenu >= 70:
        profil_revenu = "un revenu annuel moyen élevé"
    elif revenu < 40:
        profil_revenu = "un revenu annuel moyen faible"
    else:
        profil_revenu = "un revenu annuel moyen intermédiaire"

    if score >= 60:
        profil_depense = "un score de dépense élevé"
    elif score < 40:
        profil_depense = "un score de dépense faible"
    else:
        profil_depense = "un score de dépense intermédiaire"

    st.info(
        f"Le cluster {cluster_choisi} comprend {nombre_clients} clients. "
        f"Son profil se caractérise par {profil_revenu} "
        f"et {profil_depense}. "
        f"Le revenu annuel moyen est de {revenu:.2f} k$ "
        f"et le score de dépense moyen est de {score:.2f}/100."
    )

    
# Discours pour la présentation
st.subheader("🎤 Mon discours de présentation")

if cluster_choisi == "Tous les clients":
    discours = (
        "Dans ce projet, mon objectif est de segmenter les clients "
        "selon leur revenu annuel et leur score de dépense. "
        "J'ai utilisé l'algorithme K-Means pour répartir les "
        "200 clients en cinq groupes. "
        "Cette segmentation permet de comparer les profils "
        "et d'identifier des pistes d'analyse marketing."
    )
else:
    discours = (
        f"Dans ce projet, j'ai utilisé l'algorithme K-Means "
        f"pour segmenter les clients selon leur revenu annuel "
        f"et leur score de dépense. "
        f"Le cluster {cluster_choisi} comprend {nombre_clients} clients. "
        f"Le revenu annuel moyen de ce groupe est de {revenu:.2f} k$ "
        f"et son score de dépense moyen est de {score:.2f} sur 100. "
        f"Ce groupe présente {profil_revenu} et {profil_depense}. "
        f"Ces résultats peuvent aider une entreprise à mieux "
        f"comprendre ses clients et à étudier des actions marketing "
        f"adaptées. D'autres données seraient nécessaires pour "
        f"évaluer l'efficacité de ces actions."
    )

st.write(discours)

st.download_button(
    label="📄 Télécharger mon discours",
    data=discours,
    file_name="discours_presentation.txt",
    mime="text/plain"
)


# Préparer les données filtrées pour le téléchargement
csv = df_filtre.to_csv(index=False).encode("utf-8")

# Créer le bouton de téléchargement
st.download_button(
    label="📥 Télécharger les données filtrées",
    data=csv,
    file_name="clients_filtres.csv",
    mime="text/csv"
)


#graphique de visualisation
st.subheader("📈 Visualisation des clusters")

fig, ax = plt.subplots()

for cluster in sorted(df_filtre["Cluster"].unique()):
    clients = df_filtre[df_filtre["Cluster"] == cluster]

    ax.scatter(
        clients["Annual Income (k$)"],
        clients["Spending Score (1-100)"],
        label=f"Cluster {cluster}"
    )

ax.set_xlabel("Revenu annuel (k$)")
ax.set_ylabel("Score de dépense")
ax.legend()
st.pyplot(fig)

plt.close(fig)


# Profil de chaque cluster
st.subheader("📊 Profil de chaque cluster")


profil_clusters = df_filtre.groupby("Cluster").agg(
    Nombre_clients=("CustomerID", "count"),
    Revenu_moyen=("Annual Income (k$)", "mean"),
    Score_moyen=("Spending Score (1-100)", "mean")
).round(2)

st.dataframe(profil_clusters)

st.write("Nombre total de clients :", len(df))
st.write("Nombre de clients par cluster :")
st.write(df["Cluster"].value_counts().sort_index())