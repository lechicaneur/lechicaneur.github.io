import datetime
import os
import re
from google import genai
from google.genai import types

print("1. Initialisation du client GenAI...")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

aujourd_hui = datetime.date.today().strftime("%Y-%m-%d")
timestamp_unique = datetime.datetime.now().strftime("%H%M%S")


def nettoyer_markdown(texte):
    texte = texte.strip()
    texte = re.sub(r"^```(?:markdown|md)?\s*\n", "", texte)
    texte = re.sub(r"\n```\s*$", "", texte)
    return texte.strip()


prompt = f"""
Tu diriges une revue secrète qui enquête avec le plus grand sérieux du monde sur des phénomènes absurdes, banals ou invisibles, en les présentant comme des complots métaphysiques ou des manipulations de masse.

Écris un article complet au format Markdown sur un sujet totalement libre, surprenant et décalé. Adopte une langue ultra-sérieuse, érudite ou administrative, en décalage complet avec l'absurdité du sujet.

Commence impérativement par ce Front Matter YAML (sans guillemets doubles à l'intérieur des valeurs) :
---
layout: post
title: "[TITRE ORIGINAL ET PERCUTANT DU DOSSIER]"
description: "[RÉSUMÉ CONCIS DE 140 À 160 CARACTÈRES POUR LE SEO]"
date: {aujourd_hui}
author: "La Rédaction • Cellule de Veille Occulte"
category: "Prospective & Complots du Réel"
---

Structure l'article avec au moins deux sections numérotées et une conclusion mémorable. Ne mets aucun texte avant ou après le Markdown.
"""

print("2. Envoi de la requête à l'API Gemini...")
try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=1.2),
    )
    print("3. Réponse reçue avec succès !")
except Exception as e:
    print(f"ERREUR lors de l'appel API : {e}")
    exit(1)

contenu_article = nettoyer_markdown(response.text)

nom_fichier = f"_posts/{aujourd_hui}-dossier-automatise-{timestamp_unique}.md"

print(f"4. Écriture du fichier : {nom_fichier}")
os.makedirs("_posts", exist_ok=True)
with open(nom_fichier, "w", encoding="utf-8") as f:
    f.write(contenu_article)

print("Terminé avec succès !")
