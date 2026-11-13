import os
import datetime
from google import genai

print("1. Initialisation du client GenAI...")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

aujourd_hui = datetime.date.today().strftime("%Y-%m-%d")
timestamp_unique = datetime.datetime.now().strftime("%H%M%S")

prompt = """
Tu es le rédacteur en chef du Chicaneur, un organe indépendant d'investigation, de prospective logistique et d'observation méthodique du réel. Le ton est extrêmement sérieux, rigoureux, institutionnel, bureaucratique et pince-sans-rire (style haut fonctionnaire ou grand reporter technique).

Rédige un article complet au format Markdown pour un nouveau dossier d'investigation. 
Choisis un sujet original, absurde mais traité avec un sérieux absolu (par exemple : l'optimisation thermique des bouches de métro parisiennes pour la culture des endives, l'audit aérodynamique des pigeons voyageurs de la Poste, ou la valorisation des tickets de métro usagés en agglomérat de cellulose).

L'article doit impérativement commencer par ce bloc Front Matter exact :
---
layout: post
title: "Titre rigoureux et institutionnel"
date: """ + aujourd_hui + """
author: "La Rédaction • IA Autonome"
category: "Prospective & Logistique"
---

Rédige ensuite le corps du texte avec au moins deux sections numérotées, du vocabulaire technique précis, et une conclusion formelle. Ne mets aucun texte avant ou après le Front Matter.
"""

print("2. Envoi de la requête à l'API Gemini (mode synchrone)...")
try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    print("3. Réponse reçue avec succès !")
except Exception as e:
    print(f"ERREUR lors de l'appel API : {e}")
    exit(1)

contenu_article = response.text

nom_fichier = f"_posts/{aujourd_hui}-dossier-automatise-{timestamp_unique}.md"

print(f"4. Écriture du fichier : {nom_fichier}")
os.makedirs("_posts", exist_ok=True)
with open(nom_fichier, "w", encoding="utf-8") as f:
    f.write(contenu_article)

print("Terminé avec succès !")