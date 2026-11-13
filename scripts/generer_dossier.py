import os
import datetime
from google import genai

# Initialisation du client Gemini avec la clé secrète GitHub
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Date du jour au format Jekyll (AAAA-MM-JJ)
aujourd_hui = datetime.date.today().strftime("%Y-%m-%d")
timestamp_unique = datetime.datetime.now().strftime("%H%M%S")

# Prompt strict garantissant le ton et la structure exigés par Le Chicaneur
prompt = """
Tu es le rédacteur en chef du Chicaneur, un organe indépendant d'investigation, de prospective logistique et d'observation méthodique du réel. Le ton est extrêmement sérieux, rigoureux, institutionnel, bureaucratique et pince-sans-rire (style haut fonctionnaire ou grand reporter technique).

Rédige un article complet au format Markdown pour un nouveau dossier d'investigation. 
Choisis un sujet original, absurde mais traité avec un sérieux absolu (par exemple : l'optimisation thermique des bouches de métro parisiennes pour la culture des endives, l'audit aérodynamique des pigeons voyageurs de la Poste, ou la valorisation des tickets de métro usagés en agglomérat de cellulose).

L'article doit impérativement commencer par ce bloc Front Matter exact (remplace les valeurs entre crochets par ton contenu, sans garder les crochets) :
---
layout: post
title: "Titre rigoureux et institutionnel"
date: """ + aujourd_hui + """
author: "La Rédaction • IA Autonome"
category: "Prospective & Logistique"
---

Rédige ensuite le corps du texte avec au moins deux sections numérotées, du vocabulaire technique précis, et une conclusion formelle. Ne mets aucun texte avant ou après le Front Matter.
"""

print("Interrogation de Gemini pour la rédaction du dossier...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

contenu_article = response.text

# Génération d'un nom de fichier slugifié simplifié basé sur la date et l'heure
nom_fichier = f"_posts/{aujourd_hui}-dossier-automatise-{timestamp_unique}.md"

# Écriture du fichier dans le dossier _posts/
os.makedirs("_posts", exist_ok=True)
with open(nom_fichier, "w", encoding="utf-8") as f:
    f.write(contenu_article)

print(f"Dossier généré avec succès : {nom_fichier}")