import os
import datetime
from google import genai

print("1. Initialisation du client GenAI...")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

aujourd_hui = datetime.date.today().strftime("%Y-%m-%d")
timestamp_unique = datetime.datetime.now().strftime("%H%M%S")

prompt = f"""
Tu es le rédacteur en chef du Chicaneur, un organe clandestin d'investigation, de prospective logistique occulte et d'observation paranoïaque du réel. Le ton doit être un mélange parfait entre le rapport bureaucratique d'un haut fonctionnaire tatillon et la théorie du complot la plus loufoque, absolue et décomplexée. Traite les sujets du quotidien (le trafic des trottinettes, la composition chimique de la baguette de pain, la synchronisation des feux tricolores, le calibrage des ralentisseurs, ou la météo urbaine) comme des opérations psychologiques mondiales, des conspirations géométriques ou des anomalies quantiques orchestrées par des entités obscures.

Rédige un article complet au format Markdown pour un nouveau dossier d'investigation inédit. 
Invente un sujet du quotidien apparemment banal et révèle sa véritable nature subversive (évite de toujours reprendre les mêmes exemples).

L'article doit impérativement commencer par la structure Front Matter suivante, en remplaçant uniquement les valeurs entre crochets par un titre et une description originaux, percutants et conformes à l'identité du journal (ne recopie surtout pas les instructions, et évite les guillemets doubles non échappés à l'intérieur des chaînes) :
---
layout: post
title: "[INVENTE ICI UN TITRE ORIGINAL, ALARMISTE, TECHNIQUE ET HAUTEMENT CONFIDENTIEL SUR LE SUJET CHOISI]"
description: "[RÉDIGE ICI UN RÉSUMÉ CONCIS, ACCROCHEUR ET BUREAUCRATIQUEMENT INQUIÉTANT DE 140 À 160 CARACTÈRES POUR LE SEO ET LES APERÇUS]"
date: {aujourd_hui}
author: "La Rédaction • Cellule de Veille Occulte"
category: "Prospective & Complots du Réel"
---

Rédige ensuite le corps du texte avec au moins deux sections numérotées, du vocabulaire technocratique ultra-complexe associé à des délires conspirationnistes délirants, et une conclusion menaçante ou faussement rassurante. Ne mets aucun texte avant ou après le Markdown.
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
