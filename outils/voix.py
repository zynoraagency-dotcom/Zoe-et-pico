# Découpe les enregistrements de la voix de Pico (ElevenLabs) en une phrase par fichier,
# puis écrit assets/js/voix.js (table phrase -> fichier).
# Sources : outils/voix-sources/bloc1.mp3, bloc2.mp3, bloc3.mp3 (textes donnés dans l'ordre ci-dessous).
# Les temps de coupe (en secondes) viennent de l'analyse des silences de chaque fichier :
# les pauses entre phrases durent ~0,3 à 0,5 s ; les pauses plus courtes sont à l'intérieur d'une phrase.
# Utilisation (depuis la racine du site) : python3 outils/voix.py .
import json, os, re, subprocess, sys

RACINE = sys.argv[1] if len(sys.argv) > 1 else "."
SRC = os.path.join(RACINE, "outils", "voix-sources")
OUT = os.path.join(RACINE, "assets", "voix")

BLOCS = {
    "bloc1": [
        ("Un.", "un", 0.14, 0.43), ("Deux.", "deux", 0.91, 1.34), ("Trois.", "trois", 1.80, 2.18), ("Quatre.", "quatre", 2.67, 3.12),
        ("Cinq.", "cinq", 3.46, 4.03), ("Six.", "six", 4.37, 4.94), ("Sept.", "sept", 5.29, 5.82), ("Huit.", "huit", 6.15, 6.62),
        ("Neuf.", "neuf", 6.99, 7.45), ("Dix !", "dix", 7.87, 8.48), ("Bravo !", "bravo", 8.69, 9.61), ("Super !", "super", 9.61, 10.47),
        ("Génial !", "genial", 10.62, 11.47), ("Bien joué !", "bien-joue", 11.62, 12.36), ("Oui, c'est ça !", "oui-cest-ca", 12.64, 13.58),
        ("Une paire !", "une-paire", 13.84, 14.58), ("Youpi !", "youpi", 14.87, 15.67), ("Trop fort !", "trop-fort", 15.88, 16.77),
        ("Essaie encore !", "essaie-encore", 17.02, 17.79), ("Oups ! Compte avec moi.", "oups", 18.15, 19.71),
        ("Bravo, tu as gagné !", "tu-as-gagne", 19.98, 21.62),
    ],
    "bloc2": [
        ("Combien de pommes ?", "combien-pommes", 0.13, 1.07), ("Combien de fleurs ?", "combien-fleurs", 1.49, 2.44),
        ("Combien d'étoiles ?", "combien-etoiles", 2.82, 3.91), ("Combien de coccinelles ?", "combien-coccinelles", 4.27, 5.48),
        ("Combien de fraises ?", "combien-fraises", 5.86, 6.85), ("Combien de papillons ?", "combien-papillons", 7.15, 8.26),
        ("Combien de champignons ?", "combien-champignons", 8.58, 9.83), ("Combien de tulipes ?", "combien-tulipes", 10.19, 11.24),
        ("Touche le rouge !", "touche-rouge", 11.71, 12.59), ("Touche le bleu !", "touche-bleu", 12.92, 13.64),
        ("Touche le jaune !", "touche-jaune", 14.03, 14.90), ("Touche le vert !", "touche-vert", 15.24, 16.04),
        ("Touche le orange !", "touche-orange", 16.37, 17.40), ("Touche le violet !", "touche-violet", 17.72, 18.58),
        ("Touche le rose !", "touche-rose", 18.92, 19.82), ("Touche le marron !", "touche-marron", 20.13, 20.98),
        ("Trouve le cercle !", "trouve-cercle", 21.47, 22.49), ("Trouve le carré !", "trouve-carre", 22.81, 23.68),
        ("Trouve le triangle !", "trouve-triangle", 24.03, 25.15), ("Trouve l'étoile !", "trouve-etoile", 25.47, 26.52),
        ("Trouve le cœur !", "trouve-coeur", 26.83, 27.73), ("Trouve le rectangle !", "trouve-rectangle", 28.03, 29.18),
        ("Trouve le losange !", "trouve-losange", 29.47, 30.66),
    ],
    "bloc3": [
        ("Rouge.", "rouge", 0.00, 0.62), ("Orange.", "orange", 1.01, 1.63), ("Jaune.", "jaune", 2.06, 2.59), ("Vert.", "vert", 2.99, 3.49),
        ("Vert d'eau.", "vert-deau", 3.81, 4.41), ("Bleu ciel.", "bleu-ciel", 4.70, 5.47), ("Bleu.", "bleu", 5.82, 6.17),
        ("Violet.", "violet", 6.61, 7.14), ("Rose.", "rose", 7.49, 8.03), ("Rose pâle.", "rose-pale", 8.31, 9.06),
        ("Marron.", "marron", 9.42, 9.87), ("Beige.", "beige", 10.21, 10.77), ("Gris.", "gris", 11.09, 11.47),
        ("Noir.", "noir", 11.82, 12.37), ("Blanc.", "blanc", 12.70, 13.04),
        ("Touche les lumières qui volent, et compte avec moi !", "intro-lucioles", 13.48, 15.94),
        ("Retourne deux cartes et retrouve les paires !", "intro-memo", 16.32, 18.78),
        ("Choisis une couleur, puis touche le dessin pour le colorier !", "intro-coloriage", 19.12, 22.36),
        ("Bzzz ! Compte avec moi !", "compte-avec-moi", 22.73, 24.68),
        ("Bravo ! Tu as attrapé dix lumières !", "gagne-lucioles", 25.02, 27.70),
        ("Bravo ! Tu as trouvé toutes les paires !", "gagne-memo", 28.05, 30.61),
        ("Bravo ! Quel joli dessin !", "gagne-dessin", 30.94, 33.20),
        ("Bravo ! Tu as allumé toutes les lumières !", "gagne-lumieres", 33.56, 36.43),
        ("Bzzz ! Coucou ! Viens jouer avec moi !", "coucou", 36.82, 39.73),
    ],
}

def cle(texte):
    """même normalisation que dans voix.js"""
    t = texte.lower().replace(" ", " ").replace("’", "'")
    t = re.sub(r"[!?.,;:…]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

os.makedirs(OUT, exist_ok=True)
table = {}
for bloc, phrases in BLOCS.items():
    src = os.path.join(SRC, bloc + ".mp3")
    for i, (texte, nom, debut, fin) in enumerate(phrases):
        a = max(0.0, debut - 0.04)
        b = fin + 0.10 if i + 1 == len(phrases) else min(fin + 0.10, phrases[i + 1][2] - 0.02)
        dest = os.path.join(OUT, nom + ".mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src,
                        "-af", "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse",
                        "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-q:a", "5", dest], check=True)
        table[cle(texte)] = nom

modele = open(os.path.join(RACINE, "outils", "voix.modele.js"), encoding="utf-8").read()
open(os.path.join(RACINE, "assets", "js", "voix.js"), "w", encoding="utf-8").write(
    modele.replace("/*TABLE*/{}", json.dumps(table, ensure_ascii=False, indent=0).replace("\n", "")))
print(len(table), "phrases découpées")
