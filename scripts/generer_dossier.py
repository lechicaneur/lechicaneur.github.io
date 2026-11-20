import datetime
import glob
import os
import re
from google import genai
from google.genai import types

print("1. Initialisation du client GenAI...")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

aujourd_hui = datetime.date.today().strftime("%Y-%m-%d")
timestamp_unique = datetime.datetime.now().strftime("%H%M%S")


def extraire_titre(contenu):
    match = re.search(r"^title:\s*(.+)$", contenu, re.MULTILINE)
    if not match:
        return None
    titre = match.group(1).strip()
    if (titre.startswith('"') and titre.endswith('"')) or (
        titre.startswith("'") and titre.endswith("'")
    ):
        titre = titre[1:-1].strip()
    return titre


def recuperer_titres_recents(posts_dir="_posts", limite=30):
    fichiers = sorted(
        glob.glob(os.path.join(posts_dir, "**", "*.md"), recursive=True),
        reverse=True,
    )[:limite]
    titres = []
    for chemin in fichiers:
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read(1200)
        titre = extraire_titre(contenu)
        if titre:
            titres.append(titre)
    return titres


def nettoyer_markdown(texte):
    texte = texte.strip()
    texte = re.sub(r"^```(?:markdown|md)?\s*\n", "", texte)
    texte = re.sub(r"\n```\s*$", "", texte)
    return texte.strip()


titres_recents = recuperer_titres_recents()
liste_titres = (
    "\n".join(f"- {t}" for t in titres_recents) if titres_recents else "- Aucun"
)

prompt = f"""
Tu es le rédacteur en chef d'un organe clandestin d'investigation, de prospective logistique occulte et d'observation paranoïaque du réel. Ton style mêle la froideur administrative d'un haut fonctionnaire tatillon et la mécanique d'une théorie du complot absurde, absolue et décomplexée.

Reste entièrement libre dans le choix de ton sujet et de ton approche, et veille à varier par rapport aux dossiers déjà publiés :
{liste_titres}

L'article doit impérativement commencer par la structure Front Matter suivante, en remplaçant uniquement les valeurs entre crochets par un titre et une description originaux, percutants et conformes à ce registre (ne recopie pas les instructions et n'utilise pas de guillemets doubles à l'intérieur des chaînes) :
---
layout: post
title: "[TITRE ORIGINAL, ALARMISTE, TECHNIQUE ET CONFIDENTIEL SUR LE SUJET CHOISI]"
description: "[RÉSUMÉ CONCIS, ACCROCHEUR ET BUREAUCRATIQUEMENT INQUIÉTANT DE 140 À 160 CARACTÈRES]"
date: {aujourd_hui}
author: "La Rédaction • Cellule de Veille Occulte"
category: "Prospective & Complots du Réel"
---

Rédige ensuite le corps du texte avec au moins deux sections numérotées, un vocabulaire technocratique hyper-spécialisé mêlé à des hypothèses conspirationnistes délirantes, et une conclusion menaçante ou faussement rassurante. Ne mets aucun texte avant ou après le Markdown.
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
