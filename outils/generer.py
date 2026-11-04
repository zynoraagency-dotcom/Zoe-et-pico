# Génère les pages HTML statiques du site Zoé et Pico avec un en-tête et un pied de page communs.
# Utilisation (depuis la racine du site) : python3 outils/images_coloriages.py . && python3 outils/generer.py . && node outils/apercus.js .
import sys, json, os
SORTIE = sys.argv[1]
V = "16"
SITE = "https://zoeetpico.fr"
YT = "https://www.youtube.com/@zoeetpico"
YT_ABO = "https://www.youtube.com/@zoeetpico?sub_confirmation=1"
AMZ_MS = "https://www.amazon.fr/dp/B0HPYPGQWM"  # ASIN du livre broché (bibliothèque KDP)
AMZ_GS = "https://www.amazon.fr/dp/B0HPYWGW65"
MAJ = "4 novembre 2026"
PAGES_SITEMAP = []
A = ("Accueil", "/")
ICONE_YT = '<svg class="icone-yt" viewBox="0 0 28 20" aria-hidden="true"><rect width="28" height="20" rx="6" fill="currentColor" opacity=".25"/><path d="M11 5.5v9l8-4.5z" fill="currentColor"/></svg>'

def fil_ld(fil):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(fil)]}

def tete(titre, desc, chemin, extra="", image=None, fil=None, indexer=True):
    url = SITE + chemin
    if indexer: PAGES_SITEMAP.append(chemin)
    img, iw, ih, ialt = image or (f"{SITE}/img/partage.jpg", 1200, 630, "Zoé et Pico la petite luciole dans le jardin devant la maison")
    if fil: extra = ld(fil_ld(fil)) + extra
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titre}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="max-image-preview:large">
<meta name="theme-color" content="#ffc83d">
<link rel="icon" type="image/png" sizes="64x64" href="/img/icone-64.png">
<link rel="apple-touch-icon" href="/img/icone-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Zoé et Pico">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="{iw}">
<meta property="og:image:height" content="{ih}">
<meta property="og:image:alt" content="{ialt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img}">
<link rel="preload" href="/assets/fonts/sniglet-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/andika-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
{extra}</head>
"""

def nav(actif):
    def l(href, txt, cle):
        cur = ' aria-current="page"' if cle == actif else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    def o(href, ico, txt, cle):
        cur = ' aria-current="page"' if cle == actif else ""
        return f'<a href="{href}"{cur}><span aria-hidden="true">{ico}</span>{txt}</a>'
    return f"""<body>
<a class="aller-contenu" href="#contenu">Aller au contenu</a>
<header class="nav" id="nav">
  <div class="wrap nav-in">
    <a class="logo" href="/" aria-label="Zoé et Pico, accueil">
      <span class="logo-rond"><img src="/img/pico-petit.webp" alt="" width="160" height="208"></span>
      <span class="logo-txt"><span class="logo-nom">Zoé <span class="et">&amp;</span> <span class="pi">Pico</span></span><span class="logo-slogan">Apprendre en s'amusant · 3-6 ans</span></span>
    </a>
    <nav class="liens" aria-label="Menu principal">{l("/jeux/","🎮 Jeux","jeux")}{l("/coloriages/","🖍️ Coloriages","coloriages")}{l("/videos/","▶️ Vidéos","videos")}{l("/livres/","📚 Cahiers","livres")}{l("/#parents","👨‍👩‍👧 Parents","parents")}</nav>
    <a class="btn btn-miel btn-petit btn-jouer" href="/jeux/">🎮 Jouer</a>
  </div>
</header>
<nav class="onglets" aria-label="Menu">{o("/","🏠","Accueil","accueil")}{o("/jeux/","🎮","Jeux","jeux")}{o("/videos/","▶️","Vidéos","videos")}{o("/coloriages/","🖍️","Coloriages","coloriages")}{o("/livres/","📚","Cahiers","livres")}</nav>
"""

PIED = f"""
<footer class="pied">
  <div class="wrap">
    <div class="pied-grille">
      <div class="pied-marque">
        <a class="logo" href="/" aria-label="Zoé et Pico, accueil">
          <span class="logo-rond"><img src="/img/pico-petit.webp" alt="" width="160" height="208" loading="lazy"></span>
          <span class="logo-txt"><span class="logo-nom">Zoé <span class="et">&amp;</span> <span class="pi">Pico</span></span></span>
        </a>
        <p>L'univers magique de Zoé et de Pico la petite luciole&nbsp;: des jeux gratuits, des vidéos et des cahiers d'activités pour apprendre en s'amusant de 3 à 6&nbsp;ans.</p>
      </div>
      <div>
        <h2 class="disp">Jouer</h2>
        <ul>
          <li><a href="/jeu/">Les lumières de Pico</a></li>
          <li><a href="/jeux/compter/">Compter : Combien ?</a></li>
          <li><a href="/jeux/couleurs/">Les couleurs</a></li>
          <li><a href="/jeux/formes/">Les formes</a></li>
          <li><a href="/jeux/memo/">Memory</a></li>
          <li><a href="/jeux/lucioles/">Attrape les lucioles</a></li>
          <li><a href="/jeux/coloriage/">Coloriage en ligne</a></li>
        </ul>
      </div>
      <div>
        <h2 class="disp">Découvrir</h2>
        <ul>
          <li><a href="/coloriages/">Coloriages à imprimer</a></li>
          <li><a href="/videos/">Les vidéos</a></li>
          <li><a href="/livres/">Les cahiers d'activités</a></li>
          <li><a href="{YT}">La chaîne YouTube ↗</a></li>
          <li><a href="{AMZ_GS}">Les cahiers sur Amazon ↗</a></li>
        </ul>
      </div>
      <div>
        <h2 class="disp">Parents</h2>
        <ul>
          <li><a href="/#parents">Un site sûr pour les petits</a></li>
          <li><a href="/confidentialite/">Confidentialité</a></li>
          <li><a href="/mentions-legales/">Mentions légales</a></li>
        </ul>
      </div>
    </div>
    <div class="pied-bas"><span>© <span data-annee>2026</span> Zoé et Pico · Cahiers de Flora Renard</span><span>Sans publicité · Sans inscription · Sans cookie</span></div>
  </div>
</footer>
"""

def fin(scripts):
    s = "".join(f'<script src="/assets/js/{x}.js?v={V}" defer></script>\n' for x in scripts)
    return PIED + s + "</body>\n</html>\n"

def ecrire(chemin, html):
    p = os.path.join(SORTIE, chemin)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

# ---------------------------------------------------------------- blocs réutilisés
CARTES_JEUX = """
        <a class="carte-jeu vedette rev" href="/jeu/" style="--g:linear-gradient(135deg,#fff1a8,#ffc83d);--o:#d99a12;--b:#c27c00">
          <div class="vignette"><img class="v-pico" src="/img/pico.webp" alt="" width="360" height="469" loading="lazy"><span class="lanternes" aria-hidden="true"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i></i><i></i><i></i></span></div>
          <div class="texte-jeu"><span class="age">⭐ Le jeu de Pico · 3-6 ans</span><h3>Les lumières de Pico</h3><p>Compte les fleurs avec Pico et allume ses 10 lumières&nbsp;!</p>{a_lum}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/memo/" data-jeu="memo" style="--g:linear-gradient(135deg,#ffd3e4,#ff8fbd);--o:#d9578c;--b:#d13a74">
          <div class="vignette"><div class="v-cartes"><span class="mc dos"><img src="/img/pico-petit.webp" alt="" width="160" height="208" loading="lazy"></span><span class="mc">🍓</span><span class="mc">🍓</span></div></div>
          <div class="texte-jeu"><span class="age">4-6 ans</span><h3>Memory</h3><p>Retourne les cartes et trouve les paires.</p>{a_memo}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/compter/" data-jeu="compter" style="--g:linear-gradient(135deg,#c9f7e2,#6ddcb0);--o:#2e9e74;--b:#1f8a63">
          <div class="vignette"><div class="v-compte" aria-hidden="true"><span class="fruits">🍓🍓🍓</span><span class="chiffre">3</span></div></div>
          <div class="texte-jeu"><span class="age">3-6 ans</span><h3>Combien&nbsp;?</h3><p>Compte les fruits et touche le bon nombre.</p>{a_compter}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/couleurs/" data-jeu="couleurs" style="--g:linear-gradient(135deg,#d6efff,#7fcfff);--o:#2f86c0;--b:#1f74b8">
          <div class="vignette"><div class="v-blobs" aria-hidden="true"><i style="background:#ef233c"></i><i style="background:#ffd000"></i><i style="background:#22c55e"></i><i style="background:#1e6bff"></i></div></div>
          <div class="texte-jeu"><span class="age">3-5 ans</span><h3>Les couleurs</h3><p>Pico dit une couleur, touche la bonne.</p>{a_couleurs}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/formes/" data-jeu="formes" style="--g:linear-gradient(135deg,#e6ddff,#b49cff);--o:#7558d1;--b:#6a4fd8">
          <div class="vignette"><div class="v-formes" aria-hidden="true">
            <span><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="#ff5c9a"/></svg></span>
            <span><svg viewBox="0 0 100 100"><polygon points="50,6 94,90 6,90" fill="#22c55e"/></svg></span>
            <span><svg viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="6" fill="#1e6bff"/></svg></span>
            <span><svg viewBox="0 0 100 100"><polygon points="50,4 62,36 96,38 69,59 79,93 50,74 21,93 31,59 4,38 38,36" fill="#ffc400"/></svg></span>
          </div></div>
          <div class="texte-jeu"><span class="age">3-5 ans</span><h3>Les formes</h3><p>Trouve le cercle, le carré, l'étoile…</p>{a_formes}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/lucioles/" data-jeu="lucioles" style="--g:linear-gradient(135deg,#ffe0d0,#ff9a74);--o:#d9643f;--b:#c8532a">
          <div class="vignette"><span class="v-lum" aria-hidden="true"><i style="left:14%;top:20%"></i><i style="left:76%;top:16%;animation-delay:.3s"></i><i style="left:20%;top:62%;animation-delay:.6s"></i><i style="left:80%;top:58%;animation-delay:.2s"></i></span><img class="v-zoe" src="/img/zoe.webp" alt="" width="324" height="690" loading="lazy"></div>
          <div class="texte-jeu"><span class="age">3-6 ans</span><h3>Attrape les lucioles</h3><p>Aide Zoé à attraper 10 lumières qui volent.</p>{a_lucioles}<span class="jouer">Jouer ▶</span></div>
        </a>
        <a class="carte-jeu rev" href="/jeux/coloriage/" data-jeu="coloriage" style="--g:linear-gradient(135deg,#fff6c2,#c4f0d4);--o:#7fb08f;--b:#2f8f58">
          <div class="vignette"><div class="v-dessin" aria-hidden="true"><svg viewBox="0 0 120 120">
            <path d="M58 118 Q56 90 60 70" stroke="#3b2a1a" stroke-width="4" fill="none"/>
            <path d="M59 100 Q40 92 36 80 Q52 80 59 96Z" fill="#22c55e" stroke="#3b2a1a" stroke-width="3"/>
            <circle cx="60" cy="26" r="15" fill="#ff6fb5" stroke="#3b2a1a" stroke-width="3"/><circle cx="80" cy="42" r="15" fill="#ff6fb5" stroke="#3b2a1a" stroke-width="3"/>
            <circle cx="73" cy="64" r="15" fill="#fff" stroke="#3b2a1a" stroke-width="3"/><circle cx="47" cy="64" r="15" fill="#fff" stroke="#3b2a1a" stroke-width="3"/>
            <circle cx="40" cy="42" r="15" fill="#ff6fb5" stroke="#3b2a1a" stroke-width="3"/><circle cx="60" cy="47" r="13" fill="#ffd000" stroke="#3b2a1a" stroke-width="3"/>
          </svg></div></div>
          <div class="texte-jeu"><span class="age">3-6 ans</span><h3>Coloriage</h3><p>Colorie Zoé et Pico à Noël, dans la neige, à la plage et au jardin.</p>{a_coloriage}<span class="jouer">Colorier ▶</span></div>
        </a>"""
APPRENDS = {
    "a_lum": "Compter jusqu'à 10, associer une quantité à un nombre",
    "a_memo": "Mémoire, attention, observation",
    "a_compter": "Dénombrer de 1 à 10, avec une difficulté qui augmente doucement",
    "a_couleurs": "Reconnaître et nommer 8 couleurs",
    "a_formes": "Reconnaître et nommer 7 formes",
    "a_lucioles": "Rapidité, précision du geste, compter jusqu'à 10",
    "a_coloriage": "Motricité fine, noms des couleurs, créativité",
}
def cartes(details):
    d = {k: (f'<p class="apprend"><b>On apprend :</b> {v}.</p>' if details else "") for k, v in APPRENDS.items()}
    return CARTES_JEUX.format(**d)

VIDEO_PICO = f"""<button class="video" type="button" data-yt="57Ozwm16M1A" data-titre="Coucou ! Voici Zoé et Pico" aria-label="Regarder la vidéo : Coucou ! Voici Zoé et Pico">
            <img src="/img/video-message-de-pico.webp" alt="" width="540" height="960" loading="lazy"><span class="etiquette">Coucou ! Voici Zoé et Pico</span><span class="play" aria-hidden="true"></span>
          </button>"""
VIDEO_2 = f"""<button class="video video-sans-image" type="button" data-yt="gxy63tFRIhM" data-titre="Brosse-toi les dents avec Zoé et Pico !" aria-label="Regarder la vidéo : Brosse-toi les dents avec Zoé et Pico !">
            <span class="video-illus" aria-hidden="true"><img src="/img/zoe.webp" alt="" width="324" height="690" loading="lazy"><img src="/img/pico.webp" alt="" width="360" height="469" loading="lazy"></span><span class="etiquette">Brosse-toi les dents&nbsp;! 🪥</span><span class="play" aria-hidden="true"></span>
          </button>"""
CARTE_CHAINE = f"""<a class="video-chaine" href="{YT}">
            <img src="/img/pico.webp" alt="" width="360" height="469" loading="lazy"><b>Toutes les vidéos de Zoé et Pico</b><span class="btn btn-yt btn-petit">{ICONE_YT} Voir la chaîne</span>
          </a>"""

LIVRES = [
    dict(cle="ms", titre="Mon cahier d'activités avec Zoé et Pico – Moyenne Section", niveau="Moyenne Section", age="4-5 ans", img="cahier-moyenne-section", w=500, h=750, lien=AMZ_MS,
         complet="Mon cahier d'activités avec Zoé et Pico : Moyenne Section 4-5 ans : graphisme, nombres jusqu'à 10, labyrinthes, points à relier, logique et coloriages",
         alt="Zoé et Pico dans le jardin, illustration du cahier Moyenne Section",
         court="Graphisme, nombres jusqu'à 10, labyrinthes, points à relier, logique et coloriages.",
         long="Un cahier d'activités pour la Moyenne Section de maternelle, avec Zoé et Pico la petite luciole.",
         programme=["Graphisme", "Nombres jusqu'à 10", "Labyrinthes", "Points à relier", "Logique", "Coloriages"],
         puces=["4-5 ans", "Moyenne Section", "Livre broché"]),
    dict(cle="gs", titre="Mon cahier d'activités avec Zoé et Pico – Grande Section", niveau="Grande Section", age="5-6 ans", img="cahier-grande-section", w=647, h=844, lien=AMZ_GS,
         complet="Mon cahier d'activités avec Zoé et Pico : Grande Section 5-6 ans : lettres de A à Z, nombres jusqu'à 20, premières additions, labyrinthes et coloriages magiques – Prêt pour le CP !",
         alt="Couverture du cahier d'activités Grande Section de Zoé et Pico",
         court="Lettres de A à Z, nombres jusqu'à 20, premières additions, labyrinthes et coloriages magiques.",
         long="Un cahier d'activités pour la Grande Section de maternelle, avec Zoé et Pico la petite luciole : tout pour être « Prêt pour le CP ! ».",
         programme=["Lettres de A à Z", "Nombres jusqu'à 20", "Premières additions", "Labyrinthes", "Coloriages magiques"],
         puces=["5-6 ans", "Grande Section", "Prêt pour le CP !"]),
]
def carte_livre(l):
    p = "".join(f'<span class="puce{(" rose", "", " menthe")[i % 3]}">{x}</span>' for i, x in enumerate(l["puces"]))
    return f"""<article class="livre rev">
          <a class="couv" href="/livres/#{l['cle']}" tabindex="-1" aria-hidden="true"><img src="/img/{l['img']}.webp" alt="" width="{l['w']}" height="{l['h']}" loading="lazy"></a>
          <h3>{l['titre']}</h3>
          <div class="puces">{p}</div>
          <p>{l['court']}</p>
          <a class="btn btn-amazon" href="{l['lien']}">🛒 Voir sur Amazon</a>
        </article>"""
CARTE_BIENTOT = """<article class="livre rev">
          <span class="couv bientot" aria-hidden="true"><b>Bientôt&nbsp;!<br>🎄</b></span>
          <h3>Cahier de coloriage</h3>
          <div class="puces"><span class="puce">3-6 ans</span><span class="puce menthe">En préparation</span></div>
          <p>Un nouveau cahier de coloriages avec Zoé et Pico est en préparation.</p>
        </article>"""

PROMO = f"""<div class="promo-bandeau">
        <a class="promo-carte rev" href="/livres/" style="--g:linear-gradient(135deg,#fff1a8,#ffd27a);--o:#d99a12"><img src="/img/cahier-grande-section.webp" alt="" width="647" height="844" loading="lazy"><span><b>Les cahiers de Zoé et Pico</b><span>Pour continuer à apprendre à la maison, de la Moyenne à la Grande Section.</span></span></a>
        <a class="promo-carte rev" href="/videos/" style="--g:linear-gradient(135deg,#ffd3e4,#ffb3cf);--o:#d9578c"><img src="/img/video-message-de-pico.webp" alt="" width="540" height="960" loading="lazy"><span><b>Les vidéos de Zoé et Pico</b><span>De petites vidéos à regarder ensemble, sur la chaîne YouTube.</span></span></a>
      </div>"""

ORGA = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Zoé et Pico", "inLanguage": "fr-FR",
     "description": "Jeux éducatifs gratuits, vidéos et cahiers d'activités pour les enfants de 3 à 6 ans."},
    {"@type": "Organization", "@id": SITE + "/#marque", "name": "Zoé et Pico", "url": SITE + "/", "logo": SITE + "/img/icone-512.png", "sameAs": [YT]}]}

COLORIAGES = [
    dict(slug="zoe-et-pico-noel", image=True, nom="Zoé et Pico décorent le sapin", titre="Zoé et Pico décorent le sapin", court="Sapin, boules, étoile et cadeaux",
         phrase="Colorie Zoé et Pico qui décorent le sapin&nbsp;!",
         desc="Zoé accroche une boule au sapin pendant que Pico apporte une étoile : un coloriage de Noël avec les cadeaux, les cœurs et un nuage souriant."),
    dict(slug="zoe-et-pico-bonhomme-de-neige", image=True, nom="Zoé et Pico font un bonhomme de neige", titre="Le bonhomme de neige de Zoé et Pico", court="Bonnet, écharpe, flocons et soleil",
         phrase="Colorie Zoé, Pico et leur bonhomme de neige&nbsp;!",
         desc="Zoé et Pico construisent un bonhomme de neige avec son bonnet à pompon et son écharpe, sous les flocons et le soleil d'hiver."),
    dict(slug="zoe-et-pico-plage", image=True, nom="Zoé et Pico à la plage", titre="Zoé et Pico à la plage", court="Château de sable, palmier, ballon",
         phrase="Colorie Zoé et Pico à la plage&nbsp;!",
         desc="Zoé et Pico construisent un château de sable, avec le palmier, le ballon, le coquillage et l'étoile de mer : un coloriage d'été plein de soleil."),
    dict(slug="zoe-et-pico-jardin", image=True, nom="Zoé arrose les fleurs avec Pico", titre="Zoé arrose les fleurs", court="Arrosoir, fleurs, soleil et cœurs",
         phrase="Colorie Zoé et Pico au jardin&nbsp;!",
         desc="Zoé arrose les fleurs du jardin avec son arrosoir, et Pico la petite luciole vole à ses côtés sous le soleil."),
    dict(slug="zoe-et-pico-lecture", image=True, nom="Zoé et Pico lisent une histoire", titre="Zoé et Pico lisent une histoire", court="Un livre, des nuages et des étoiles",
         phrase="Colorie Zoé et Pico qui lisent une histoire&nbsp;!",
         desc="Zoé et Pico, assis dans l'herbe, lisent un livre ensemble sous un soleil souriant, entourés de nuages, de cœurs et d'étoiles."),
]
def img_vignette(c):
    return (f"/coloriages/zoe-et-pico/{c['slug']}-vignette.webp", 400, 565) if c.get("image") else (f"/coloriages/svg/{c['slug']}.svg", 400, 400)
def img_feuille(c):
    return (f"/coloriages/zoe-et-pico/{c['slug']}-impression.png", 2110, 2982) if c.get("image") else (f"/coloriages/svg/{c['slug']}.svg", 400, 400)
def img_partage(c):
    return (f"/coloriages/zoe-et-pico/{c['slug']}.png", 800, 1131) if c.get("image") else (f"/coloriages/img/{c['slug']}.png", 800, 800)

def vignette_coloriage(c, details=False):
    btns = (f'<div class="btns-mini"><a class="btn btn-miel btn-petit" href="/coloriages/{c["slug"]}/">🖨️ Imprimer</a>'
            f'<a class="btn btn-blanc btn-petit" href="/coloriages/pdf/coloriage-{c["slug"]}.pdf" download>📄 PDF</a>'
            f'<a class="btn btn-blanc btn-petit" href="/jeux/coloriage/#jeu-coloriage-{c["slug"]}" data-jeu="coloriage" data-dessin="{c["slug"]}">🎨 En ligne</a></div>') if details else ""
    return f"""<article class="coloriage-carte rev">
          <a class="coloriage-image" href="/coloriages/{c['slug']}/"><img src="{img_vignette(c)[0]}" alt="Coloriage {c['nom']} à imprimer" width="{img_vignette(c)[1]}" height="{img_vignette(c)[2]}" loading="lazy"></a>
          <h3>{c['titre']}</h3>
          <p>{c['court']}</p>{btns}
        </article>"""
VIGNETTES_COLORIAGES = "".join(vignette_coloriage(c) for c in COLORIAGES[:4])

# ================================================================ ACCUEIL
accueil = tete("Zoé et Pico – Jeux éducatifs gratuits, vidéos et cahiers pour les 3-6 ans",
    "Joue avec Zoé et Pico, la petite luciole : jeux gratuits pour compter, apprendre les couleurs, les formes et colorier, vidéos et cahiers d'activités pour la maternelle (3-6 ans).",
    "/", ld(ORGA) + '<link rel="preload" as="image" href="/img/accueil-affiche.webp" fetchpriority="high">\n') + nav("accueil") + f"""
<div class="scene" id="accueil">
  <video class="fond-video" id="fond-video" muted loop playsinline preload="none" poster="/img/accueil-affiche.webp" aria-hidden="true" tabindex="-1"></video>
  <div class="wrap heros">
    <div class="heros-txt">
      <h1 id="titre"><span class="mot" style="--i:0">Joue</span> <span class="mot" style="--i:1">et</span> <span class="mot" style="--i:2">apprends</span><br><span class="mot" style="--i:3">avec</span> <span class="mot jaune" style="--i:4">Zoé</span><br><span class="mot" style="--i:5">et</span> <span class="mot jaune" style="--i:6">Pico</span>&nbsp;<span class="mot" style="--i:7">!</span></h1>
      <p class="apparait" style="--d:2s">Compter, les couleurs, les formes, la mémoire et le coloriage, dans le jardin de Zoé. Pico lit les consignes à voix haute&nbsp;: pas besoin de savoir lire&nbsp;!</p>
      <div class="btns apparait" style="--d:2.2s">
        <a class="btn btn-miel btn-jouer" href="#jeux">🎮 Jouer</a>
        <a class="btn btn-rose" href="#videos">▶ Regarder les vidéos</a>
      </div>
    </div>
    <div class="duo">
      <div class="zoe-saut" id="zoe"><img src="/img/zoe.webp" alt="Zoé" width="324" height="690"></div>
      <div class="pico-vol" id="pico"><img src="/img/pico.webp" alt="Pico, la petite luciole" width="360" height="469"></div>
      <div class="bulle" aria-hidden="true">Coucou&nbsp;! On joue&nbsp;? 💛</div>
    </div>
  </div>
</div>

<main id="contenu">
  <section id="activites" aria-labelledby="t-activites">
    <div class="wrap">
      <div class="titre rev"><span class="badge">✨ Apprendre en s'amusant</span><h2 id="t-activites">Que veux-tu apprendre&nbsp;?</h2></div>
      <div class="activites">
        <a class="activite rev" href="/jeux/compter/" data-jeu="compter" style="--g:#c9f7e2;--o:#9fdcc0"><span class="ico" aria-hidden="true">🔢</span><span><b>Les nombres</b><small>Compter jusqu'à 10 avec Pico</small></span></a>
        <a class="activite rev" href="/jeux/couleurs/" data-jeu="couleurs" style="--g:#d6efff;--o:#a8d6f5"><span class="ico" aria-hidden="true">🎨</span><span><b>Les couleurs</b><small>Reconnaître et nommer les couleurs</small></span></a>
        <a class="activite rev" href="/jeux/formes/" data-jeu="formes" style="--g:#e6ddff;--o:#cbbcf5"><span class="ico" aria-hidden="true">🔺</span><span><b>Les formes</b><small>Cercle, carré, triangle, étoile…</small></span></a>
        <a class="activite rev" href="/jeux/memo/" data-jeu="memo" style="--g:#ffd3e4;--o:#f5b3cc"><span class="ico" aria-hidden="true">🧠</span><span><b>La mémoire</b><small>Retrouver les paires de cartes</small></span></a>
        <a class="activite rev" href="/coloriages/" style="--g:#fff6c2;--o:#eedc8a"><span class="ico" aria-hidden="true">🖍️</span><span><b>Le coloriage</b><small>En ligne ou à imprimer</small></span></a>
        <a class="activite rev" href="/videos/" style="--g:#ffe0d0;--o:#f5c0a6"><span class="ico" aria-hidden="true">▶️</span><span><b>Les vidéos</b><small>Regarder Zoé et Pico</small></span></a>
      </div>
    </div>
  </section>

  <section id="jeux" aria-labelledby="t-jeux">
    <div class="wrap">
      <div class="titre rev"><span class="badge">🎮 7 jeux gratuits</span><h2 id="t-jeux">Choisis ton jeu&nbsp;!</h2><p>Touche une carte pour commencer.</p></div>
      <div class="jeux">{cartes(False)}
      </div>
    </div>
  </section>

  <section id="coloriages" aria-labelledby="t-coloriages">
    <div class="wrap">
      <div class="titre rev"><span class="badge">🖨️ Gratuit, à imprimer</span><h2 id="t-coloriages">Les coloriages de Zoé et Pico</h2><p>À imprimer en A4 ou à colorier en ligne.</p></div>
      <div class="grille-coloriages">{VIGNETTES_COLORIAGES}</div>
      <div class="suite rev"><a class="btn btn-miel" href="/coloriages/">🖍️ Tous les coloriages à imprimer</a></div>
    </div>
  </section>

  <section id="videos" aria-labelledby="t-videos">
    <div class="wrap">
      <div class="videos-zone rev">
        <div class="videos-liste">
          {VIDEO_2}
          {VIDEO_PICO}
          {CARTE_CHAINE}
        </div>
        <div class="videos-txt">
          <div class="mini"><img src="/img/pico-petit.webp" alt="" width="160" height="208" loading="lazy"><span class="badge">▶️ Les vidéos</span></div>
          <h2 id="t-videos">Les vidéos de Zoé et Pico</h2>
          <p>Appuie sur une vidéo pour la regarder. D'autres petites vidéos arrivent pour compter, apprendre les couleurs et s'amuser dans le jardin de Zoé&nbsp;!</p>
          <div class="btns">
            <a class="btn btn-rose" href="/videos/">▶ Toutes les vidéos</a>
            <a class="btn btn-yt" href="{YT_ABO}">{ICONE_YT} S'abonner</a>
          </div>
          <p class="note">La vidéo se charge depuis YouTube seulement quand vous appuyez dessus.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="cahiers" aria-labelledby="t-cahiers">
    <div class="wrap">
      <div class="titre rev"><span class="badge">📚 Pour continuer à la maison</span><h2 id="t-cahiers">Les cahiers de Zoé et Pico</h2><p>Des cahiers d'activités et de coloriage pour la maternelle, vendus sur Amazon.</p></div>
      <div class="livres">
        {carte_livre(LIVRES[0])}
        {carte_livre(LIVRES[1])}
        {CARTE_BIENTOT}
      </div>
      <div class="suite rev"><a class="btn btn-blanc" href="/livres/">📚 Découvrir les cahiers</a></div>
    </div>
  </section>

  <section id="parents" aria-labelledby="t-parents">
    <div class="wrap">
      <div class="titre rev"><span class="badge">👨‍👩‍👧 Pour les parents</span><h2 id="t-parents">Un coin sûr pour les petits</h2></div>
      <div class="parents">
        <div class="atout rev"><span aria-hidden="true">🔒</span><h3>Sans inscription</h3><p>Aucun compte, aucun formulaire, aucun cookie, aucune mesure d'audience. <a href="/confidentialite/">En savoir plus</a></p></div>
        <div class="atout rev"><span aria-hidden="true">🚫</span><h3>Sans publicité</h3><p>Les liens vers Amazon et YouTube sont protégés par une petite question pour les adultes.</p></div>
        <div class="atout rev"><span aria-hidden="true">🔊</span><h3>Pico parle</h3><p>Chaque consigne est lue à voix haute, pour jouer avant de savoir lire.</p></div>
        <div class="atout rev"><span aria-hidden="true">🧠</span><h3>Comme à l'école</h3><p>Nombres, couleurs, formes, mémoire&nbsp;: les jeux accompagnent les cahiers.</p></div>
      </div>
    </div>
  </section>
</main>
""" + fin(["commun", "jeux", "accueil"])
ecrire("index.html", accueil)

# ================================================================ JEUX
jeux = tete("Jeux éducatifs gratuits pour les 3-6 ans – Zoé et Pico",
    "7 jeux éducatifs gratuits pour la maternelle : compter jusqu'à 10, les couleurs, les formes, memory, coloriage. Sans inscription, sans publicité, consignes lues à voix haute.",
    "/jeux/", fil=[A, ("Jeux", "/jeux/")]) + nav("jeux") + f"""
<main id="contenu">
  <div class="page-tete">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › Jeux</p>
        <h1>Les jeux de Zoé et Pico</h1>
        <p>Des jeux éducatifs gratuits pour les 3-6 ans&nbsp;: compter, reconnaître les couleurs et les formes, exercer sa mémoire et colorier. Pico lit chaque consigne à voix haute.</p>
      </div>
      <img src="/img/pico.webp" alt="" width="360" height="469">
    </div>
  </div>

  <section id="jeux" aria-labelledby="t-jeux" style="padding-top:10px">
    <div class="wrap">
      <h2 id="t-jeux" class="visuel-masque">Choisis ton jeu</h2>
      <div class="jeux">{cartes(True)}
      </div>
    </div>
  </section>

  <section aria-labelledby="t-conseils">
    <div class="wrap">
      <div class="titre rev"><span class="badge">👨‍👩‍👧 Pour les parents</span><h2 id="t-conseils">Jouer ensemble, c'est encore mieux</h2></div>
      <div class="parents">
        <div class="atout rev"><span aria-hidden="true">⏱️</span><h3>Des parties courtes</h3><p>Chaque jeu dure quelques minutes&nbsp;: idéal pour une petite pause.</p></div>
        <div class="atout rev"><span aria-hidden="true">🔊</span><h3>Le son allumé</h3><p>Pico lit les consignes et compte avec votre enfant. Le bouton 🔊 répète la consigne.</p></div>
        <div class="atout rev"><span aria-hidden="true">💬</span><h3>On en parle</h3><p>Nommez les couleurs et les formes autour de vous&nbsp;: c'est le meilleur prolongement du jeu.</p></div>
        <div class="atout rev"><span aria-hidden="true">📚</span><h3>Et sur papier</h3><p>Les <a href="/livres/">cahiers d'activités</a> prolongent les jeux loin des écrans.</p></div>
      </div>
    </div>
  </section>

  <section aria-label="À découvrir aussi">
    <div class="wrap">{PROMO}</div>
  </section>
</main>
""" + fin(["commun", "jeux"])
ecrire("jeux/index.html", jeux)

# ================================================================ VIDÉOS
videos = tete("Vidéos éducatives pour enfants – Zoé et Pico",
    "Les vidéos de Zoé et Pico la petite luciole : de petites vidéos pour les enfants de 3 à 6 ans, à regarder ensemble sur la chaîne YouTube Zoé et Pico.",
    "/videos/", fil=[A, ("Vidéos", "/videos/")]) + nav("videos") + f"""
<main id="contenu">
  <div class="page-tete">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › Vidéos</p>
        <h1>Les vidéos de Zoé et Pico</h1>
        <p>Retrouve Zoé et Pico la petite luciole en vidéo&nbsp;! De nouvelles vidéos arrivent régulièrement sur la chaîne YouTube.</p>
        <div class="btns"><a class="btn btn-yt" href="{YT_ABO}">{ICONE_YT} S'abonner à la chaîne</a></div>
      </div>
      <img src="/img/pico.webp" alt="" width="360" height="469">
    </div>
  </div>

  <section aria-labelledby="t-dernieres" style="padding-top:10px">
    <div class="wrap">
      <div class="theme">
        <h2 id="t-dernieres">✨ Les dernières vidéos</h2>
        <div class="grille-videos">
          <!-- POUR AJOUTER UNE VIDÉO : copier le bloc <button class="video" …> … </button> ci-dessous,
               remplacer 57Ozwm16M1A par l'identifiant de la vidéo (la fin de son adresse YouTube),
               changer le titre (2 fois) et l'image (une capture de la vidéo, placée dans le dossier img). -->
          {VIDEO_2}
          {VIDEO_PICO}
          {CARTE_CHAINE}
        </div>
        <p class="note">Pour protéger votre vie privée, YouTube n'est contacté que lorsque vous appuyez sur une vidéo (mode «&nbsp;confidentialité renforcée&nbsp;»). <a href="/confidentialite/">En savoir plus</a></p>
      </div>
    </div>
  </section>

  <section aria-label="À découvrir aussi">
    <div class="wrap">{PROMO}</div>
  </section>
</main>
""" + fin(["commun"])
ecrire("videos/index.html", videos)

# ================================================================ LIVRES
def detail_livre(l):
    p = "".join(f'<span class="puce{(" rose", "", " menthe")[i % 3]}">{x}</span>' for i, x in enumerate(l["puces"]))
    return f"""<article class="livre-detail rev" id="{l['cle']}">
        <span class="couv"><img src="/img/{l['img']}.webp" alt="{l['alt']}" width="{l['w']}" height="{l['h']}"{' loading="lazy"' if l['cle'] != 'ms' else ''}></span>
        <div>
          <h2>{l['titre']}</h2>
          <div class="puces">{p}</div>
          <p>{l['long']}</p>
          <h3 class="disp" style="font-size:1.15rem;margin-top:6px">Au programme</h3>
          <ul>{"".join(f"<li>{x}</li>" for x in l['programme'])}</ul>
          <p style="font-size:.98rem">Âge conseillé&nbsp;: {l['age']} · {l['niveau']} de maternelle · Livre broché vendu sur Amazon</p>
          <div class="btns"><a class="btn btn-amazon" href="{l['lien']}">🛒 Voir le cahier sur Amazon</a></div>
        </div>
      </article>"""
livres_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Book", "name": l["complet"], "image": SITE + f"/img/{l['img']}.jpg", "url": l["lien"], "inLanguage": "fr", "bookFormat": "https://schema.org/Paperback",
     "author": {"@type": "Person", "name": "Flora Renard"}, "typicalAgeRange": l["age"].replace(" ans", ""),
     "about": l["programme"], "educationalLevel": l["niveau"]} for l in LIVRES]}
livres = tete("Cahiers d'activités et de coloriage pour la maternelle – Zoé et Pico",
    "Les cahiers d'activités de Zoé et Pico pour la Moyenne Section (4-5 ans) et la Grande Section (5-6 ans) : activités et coloriages pour apprendre en s'amusant. Disponibles sur Amazon.",
    "/livres/", ld(livres_ld), fil=[A, ("Cahiers", "/livres/")]) + nav("livres") + f"""
<main id="contenu">
  <div class="page-tete">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › Cahiers</p>
        <h1>Les cahiers de Zoé et Pico</h1>
        <p>Pour continuer l'aventure loin des écrans&nbsp;: des cahiers d'activités et de coloriage pour la maternelle, avec Zoé et Pico.</p>
      </div>
      <img src="/img/pico.webp" alt="" width="360" height="469">
    </div>
  </div>

  <section aria-label="Les cahiers" style="padding-top:10px">
    <div class="wrap">
      {detail_livre(LIVRES[0])}
      {detail_livre(LIVRES[1])}
      <div class="livres" style="max-width:420px">{CARTE_BIENTOT}</div>
    </div>
  </section>

  <section aria-labelledby="t-questions">
    <div class="wrap">
      <div class="texte rev">
        <h2 id="t-questions">Questions des parents</h2>
        <h3 class="disp" style="font-size:1.2rem;margin-top:14px">Où acheter les cahiers&nbsp;?</h3>
        <p>Les cahiers sont vendus sur Amazon. Les boutons «&nbsp;Voir sur Amazon&nbsp;» ouvrent la page du cahier après une petite question réservée aux adultes.</p>
        <h3 class="disp" style="font-size:1.2rem;margin-top:14px">Quel cahier choisir&nbsp;?</h3>
        <p>Le cahier Moyenne Section (4-5 ans) travaille le graphisme, les nombres jusqu'à 10, la logique et l'attention. Le cahier Grande Section (5-6 ans) aborde les lettres de A à Z, les nombres jusqu'à 20 et les premières additions, pour préparer l'entrée au CP.</p>
        <h3 class="disp" style="font-size:1.2rem;margin-top:14px">Et sur le site&nbsp;?</h3>
        <p>Les <a href="/jeux/">jeux gratuits</a> complètent les cahiers&nbsp;: compter, les couleurs, les formes, la mémoire et le coloriage.</p>
      </div>
    </div>
  </section>
</main>
""" + fin(["commun"])
ecrire("livres/index.html", livres)

# ================================================================ MENTIONS LÉGALES
mentions = tete("Mentions légales – Zoé et Pico", "Mentions légales du site Zoé et Pico : éditeur, hébergeur, propriété intellectuelle.",
    "/mentions-legales/", fil=[A, ("Mentions légales", "/mentions-legales/")]) + nav("") + f"""
<main id="contenu">
  <div class="page-tete"><div class="wrap"><div><p class="fil"><a href="/">Accueil</a> › Mentions légales</p><h1>Mentions légales</h1></div></div></div>
  <section style="padding-top:10px">
    <div class="wrap">
      <div class="texte">
        <h2>Éditeur du site</h2>
        <p>Le site <strong>zoeetpico.fr</strong> est édité par un particulier, à titre non professionnel.</p>
        <p>Conformément à la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique (LCEN), l'éditeur a choisi de ne pas rendre publique son identité. Ses coordonnées ont été communiquées à l'hébergeur du site.</p>
        <h2>Hébergeur</h2>
        <p>Netlify, Inc.<br>San Francisco, Californie, États-Unis<br>Site&nbsp;: <a href="https://www.netlify.com">www.netlify.com</a></p>
        <h2>Propriété intellectuelle</h2>
        <p>Les personnages de Zoé et Pico, les illustrations, les textes, les jeux et les vidéos présents sur ce site sont protégés par le droit d'auteur. Toute reproduction ou réutilisation, totale ou partielle, sans autorisation est interdite.</p>
        <p>Les polices Andika et Sniglet sont utilisées sous licence SIL Open Font License 1.1.</p>
        <h2>Liens vers d'autres sites</h2>
        <p>Le site propose des liens vers Amazon (pour acheter les cahiers) et vers YouTube (pour regarder les vidéos). Pour protéger les enfants, ces liens s'ouvrent seulement après une question réservée aux adultes. Ces sites ont leurs propres conditions d'utilisation et politiques de confidentialité.</p>
        <h2>Données personnelles</h2>
        <p>Le site ne collecte aucune donnée personnelle. Tous les détails sont dans la page <a href="/confidentialite/">Confidentialité</a>.</p>
        <h2>Accessibilité</h2>
        <p>Le site est conçu pour être utilisable au doigt, à la souris et au clavier, avec de grands boutons, des textes lisibles et des consignes lues à voix haute. Il respecte le réglage «&nbsp;réduire les animations&nbsp;» de votre appareil.</p>
        <p class="maj">Dernière mise à jour&nbsp;: {MAJ}.</p>
      </div>
    </div>
  </section>
</main>
""" + fin(["commun"])
ecrire("mentions-legales/index.html", mentions)

# ================================================================ CONFIDENTIALITÉ
conf = tete("Confidentialité – Zoé et Pico", "Politique de confidentialité de Zoé et Pico : aucun compte, aucun cookie, aucune publicité, aucune mesure d'audience.",
    "/confidentialite/", fil=[A, ("Confidentialité", "/confidentialite/")]) + nav("") + f"""
<main id="contenu">
  <div class="page-tete"><div class="wrap"><div><p class="fil"><a href="/">Accueil</a> › Confidentialité</p><h1>Confidentialité</h1><p>Zoé et Pico est un site pour les jeunes enfants&nbsp;: il est conçu pour ne collecter aucune donnée personnelle.</p></div><img src="/img/pico.webp" alt="" width="360" height="469"></div></div>
  <section style="padding-top:10px">
    <div class="wrap">
      <div class="texte">
        <h2>En bref</h2>
        <ul>
          <li>Aucun compte, aucune inscription, aucun formulaire.</li>
          <li>Aucun cookie, aucune publicité, aucune mesure d'audience, aucun suivi.</li>
          <li>Rien n'est enregistré dans votre navigateur&nbsp;: les parties ne sont pas sauvegardées.</li>
          <li>Les polices de caractères sont hébergées sur le site&nbsp;: aucune demande n'est envoyée à Google pour les afficher.</li>
        </ul>
        <h2>Hébergement</h2>
        <p>Le site est hébergé par Netlify, Inc. Comme tout hébergeur, Netlify reçoit techniquement les informations nécessaires pour afficher les pages (adresse IP, type de navigateur, page demandée) et peut les conserver dans des journaux de sécurité. Netlify étant situé aux États-Unis, ces données peuvent y être traitées&nbsp;; Netlify indique encadrer ces transferts conformément au RGPD. Voir la <a href="https://www.netlify.com/privacy/">politique de confidentialité de Netlify</a>.</p>
        <h2>Vidéos YouTube</h2>
        <p>Les vidéos ne sont pas chargées à l'ouverture de la page&nbsp;: seule une image est affichée. Quand vous appuyez sur une vidéo, elle est lue depuis YouTube en mode «&nbsp;confidentialité renforcée&nbsp;» (youtube-nocookie.com). À ce moment, YouTube (Google) reçoit des informations de connexion et peut utiliser ses propres traceurs. Voir les <a href="https://policies.google.com/privacy?hl=fr">règles de confidentialité de Google</a>.</p>
        <h2>Liens vers Amazon et YouTube</h2>
        <p>Les boutons qui mènent à Amazon ou à YouTube demandent d'abord de toucher un nombre écrit en lettres, pour qu'un adulte valide la sortie du site. Une fois sur ces sites, leurs propres règles de confidentialité s'appliquent.</p>
        <h2>Voix de Pico</h2>
        <p>Les consignes sont lues par la synthèse vocale de votre appareil. Le site choisit en priorité une voix installée sur l'appareil. Si aucune n'est disponible, certains navigateurs peuvent utiliser une voix en ligne fournie par l'éditeur du navigateur&nbsp;: seules les consignes du jeu sont alors transmises, jamais de donnée personnelle.</p>
        <h2>Enfants</h2>
        <p>Le site s'adresse aux enfants de 3 à 6 ans accompagnés de leurs parents. Il ne demande jamais de nom, de photo, d'âge ou d'adresse, et ne propose ni achat intégré, ni discussion, ni publicité.</p>
        <h2>Vos droits</h2>
        <p>Le site ne détenant aucune donnée vous concernant, il n'y a rien à consulter, corriger ou supprimer. Pour toute question sur vos données personnelles en général, vous pouvez consulter le site de la <a href="https://www.cnil.fr">CNIL</a>.</p>
        <p class="maj">Dernière mise à jour&nbsp;: {MAJ}.</p>
      </div>
    </div>
  </section>
</main>
""" + fin(["commun"])
ecrire("confidentialite/index.html", conf)

# ================================================================ 404
p404 = tete("Page introuvable – Zoé et Pico", "Cette page n'existe pas. Retourne jouer avec Zoé et Pico !", "/404.html", indexer=False, extra=
    '<meta name="robots" content="noindex">\n') + nav("") + """
<main id="contenu">
  <div class="page-tete" style="min-height:70vh"><div class="wrap"><div>
    <h1>Oups&nbsp;! Pico s'est perdu…</h1>
    <p>Cette page n'existe pas (ou plus). Pas grave&nbsp;: on retourne jouer&nbsp;!</p>
    <div class="btns"><a class="btn btn-miel" href="/jeux/">🎮 Les jeux</a><a class="btn btn-blanc" href="/">🏠 L'accueil</a></div>
  </div><img src="/img/pico.webp" alt="" width="360" height="469"></div></div>
</main>
""" + fin(["commun"])
ecrire("404.html", p404)

# ================================================================ UNE PAGE PAR JEU (pour Google)
A = ("Accueil", "/")
JEUX_PAGES = [
    dict(slug="compter", h1="Combien ? Le jeu pour apprendre à compter", titre="Jeu pour apprendre à compter jusqu'à 10 (3-6 ans) – Zoé et Pico",
         desc="Jeu gratuit pour apprendre à compter jusqu'à 10 en maternelle : compte les fruits avec Pico et touche le bon nombre. Consignes lues à voix haute, sans inscription.",
         intro="Des pommes, des fraises, des étoiles… Ton enfant compte les objets et touche le bon nombre. Pico lit la question à voix haute et la difficulté augmente doucement, de 5 à 10.",
         age="3-6 ans", ico="🔢", g="#c9f7e2",
         apprend=["Dénombrer une petite quantité d'objets", "Associer une quantité à l'écriture du nombre", "Reconnaître les chiffres de 1 à 10"],
         comment=["Écoute la question de Pico : « Combien de pommes ? »", "Compte les objets, en les montrant du doigt", "Touche le bon nombre parmi les trois propositions", "Allume les 8 lumières pour gagner !"],
         conseil="Comptez à voix haute avec votre enfant en pointant chaque objet du doigt : c'est la meilleure façon d'apprendre à ne pas en oublier."),
    dict(slug="couleurs", h1="Le jeu des couleurs", titre="Jeu pour apprendre les couleurs en maternelle (3-5 ans) – Zoé et Pico",
         desc="Jeu gratuit pour apprendre les couleurs : Pico dit une couleur, l'enfant touche la bonne. Rouge, bleu, jaune, vert, orange, violet, rose, marron. Pour les 3-5 ans.",
         intro="Pico dit une couleur à voix haute, ton enfant touche la bonne tache de peinture. Huit couleurs à reconnaître : rouge, bleu, jaune, vert, orange, violet, rose et marron.",
         age="3-5 ans", ico="🎨", g="#d6efff",
         apprend=["Reconnaître 8 couleurs", "Associer le nom d'une couleur à la couleur", "Écouter une consigne et y répondre"],
         comment=["Écoute Pico : « Touche le rouge ! »", "Regarde bien les quatre taches de couleur", "Touche la bonne couleur", "Allume les 8 lumières pour gagner !"],
         conseil="Après la partie, jouez à « je vois quelque chose de rouge… » dans la maison : votre enfant réutilise tout de suite ce qu'il vient d'apprendre."),
    dict(slug="formes", h1="Le jeu des formes", titre="Jeu pour reconnaître les formes : cercle, carré, triangle (3-5 ans) – Zoé et Pico",
         desc="Jeu gratuit pour reconnaître les formes en maternelle : cercle, carré, triangle, rectangle, étoile, cœur et losange. Consignes lues à voix haute, pour les 3-5 ans.",
         intro="Cercle, carré, triangle, rectangle, étoile, cœur, losange : Pico nomme une forme, ton enfant la retrouve parmi quatre propositions.",
         age="3-5 ans", ico="🔺", g="#e6ddff",
         apprend=["Reconnaître et nommer 7 formes", "Observer et comparer des formes", "Enrichir son vocabulaire"],
         comment=["Écoute Pico : « Trouve le triangle ! »", "Observe les quatre formes", "Touche la bonne forme", "Allume les 8 lumières pour gagner !"],
         conseil="Cherchez ensemble les formes autour de vous : une assiette ronde, une fenêtre carrée, un toit en triangle…"),
    dict(slug="memo", h1="Le Memory de Zoé et Pico", titre="Jeu de memory pour enfants (4-6 ans) – Zoé et Pico",
         desc="Jeu de memory gratuit pour les enfants de 4 à 6 ans : retourne les cartes et retrouve les 6 paires. Exerce la mémoire et l'attention. Sans inscription, sans publicité.",
         intro="Douze cartes, six paires à retrouver : fraises, fleurs, coccinelles, arcs-en-ciel… Ton enfant retourne deux cartes à la fois et doit se souvenir de leur place.",
         age="4-6 ans", ico="🧠", g="#ffd3e4",
         apprend=["Exercer la mémoire visuelle", "Se concentrer et rester attentif", "Observer et associer des images identiques"],
         comment=["Touche une carte pour la retourner", "Touche une deuxième carte", "Si les deux images sont pareilles, c'est une paire !", "Retrouve les 6 paires pour gagner"],
         conseil="Jouez à tour de rôle avec votre enfant : il adore battre les grands, et il apprend à attendre son tour."),
    dict(slug="lucioles", h1="Attrape les lucioles", titre="Jeu d'adresse : attrape les lucioles (3-6 ans) – Zoé et Pico",
         desc="Jeu d'adresse gratuit pour les 3-6 ans : aide Zoé à attraper 10 lumières de luciole qui volent, et compte avec Pico. Idéal sur tablette et téléphone.",
         intro="Des lumières de luciole volent dans le jardin : ton enfant les touche pour les attraper et compte avec Pico jusqu'à 10.",
         age="3-6 ans", ico="✨", g="#ffe0d0",
         apprend=["Précision du geste et rapidité", "Compter jusqu'à 10", "Coordination œil-main"],
         comment=["Regarde les lumières qui volent", "Touche une lumière pour l'attraper", "Pico compte avec toi à chaque lumière", "Attrape 10 lumières pour gagner !"],
         conseil="Un jeu parfait pour les plus petits qui découvrent l'écran tactile : il suffit de toucher, sans rien lire."),
    dict(slug="coloriage", h1="Le coloriage en ligne", titre="Coloriage en ligne gratuit pour enfants (3-6 ans) – Zoé et Pico",
         desc="Coloriage en ligne gratuit pour les 3-6 ans : colorie Zoé et Pico à Noël, dans la neige, à la plage, au jardin ou en lisant une histoire. Les coloriages sont aussi à imprimer.",
         intro="Cinq coloriages de Zoé et Pico à colorier sur l'écran : Noël, le bonhomme de neige, la plage, le jardin et l'heure de l'histoire. Touche une zone, elle se remplit de la couleur choisie, et Pico dit le nom de chaque couleur.",
         age="3-6 ans", ico="🖍️", g="#fff6c2",
         apprend=["Nommer 15 couleurs", "Créativité et choix des couleurs", "Précision du geste"],
         comment=["Choisis un pot de peinture", "Touche une partie du dessin pour la colorier", "Le bouton ↩️ annule la dernière couleur", "Touche « J'ai fini ! » ou imprime ton dessin 🖨️"],
         conseil="Les mêmes dessins existent en version à imprimer : idéal pour continuer avec de vrais crayons, loin des écrans.", extra_lien=("/coloriages/", "🖨️ Les coloriages à imprimer")),
]
def page_jeu(j):
    autres = "".join(f'<a class="activite" href="/jeux/{x["slug"]}/" data-jeu="{x["slug"]}" style="--g:{x["g"]}"><span class="ico" aria-hidden="true">{x["ico"]}</span><span><b>{x["h1"]}</b><small>{x["age"]}</small></span></a>' for x in JEUX_PAGES if x is not j)
    autres += '<a class="activite" href="/jeu/" style="--g:#fff1a8"><span class="ico" aria-hidden="true">⭐</span><span><b>Les lumières de Pico</b><small>3-6 ans</small></span></a>'
    plus = f'<a class="btn btn-blanc" href="{j["extra_lien"][0]}">{j["extra_lien"][1]}</a>' if j.get("extra_lien") else ""
    jeu_ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": j["h1"], "description": j["desc"], "url": f"{SITE}/jeux/{j['slug']}/",
              "inLanguage": "fr", "isAccessibleForFree": True, "learningResourceType": "Jeu éducatif", "educationalLevel": "Maternelle",
              "typicalAgeRange": j["age"].replace(" ans", ""), "teaches": j["apprend"], "publisher": {"@id": SITE + "/#marque"}}
    html = tete(j["titre"], j["desc"], f"/jeux/{j['slug']}/", ld(jeu_ld), fil=[A, ("Jeux", "/jeux/"), (j["h1"], f"/jeux/{j['slug']}/")]) + nav("jeux") + f"""
<main id="contenu">
  <div class="page-tete">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › <a href="/jeux/">Jeux</a> › {j['h1']}</p>
        <h1>{j['h1']}</h1>
        <p>{j['intro']}</p>
        <div class="btns"><a class="btn btn-miel btn-jouer btn-grand" href="#jeu-{j['slug']}" data-jeu="{j['slug']}">▶ Jouer maintenant</a>{plus}</div>
        <div class="puces" style="justify-content:flex-start;margin-top:16px"><span class="puce">{j['age']}</span><span class="puce menthe">Gratuit</span><span class="puce rose">Sans inscription</span><span class="puce">🔊 Lu à voix haute</span></div>
      </div>
      <img src="/img/pico.webp" alt="" width="360" height="469">
    </div>
  </div>
  <section aria-label="Le jeu en détail" style="padding-top:10px">
    <div class="wrap">
      <div class="infos-jeu">
        <div class="atout rev"><span aria-hidden="true">🧠</span><h2 class="disp">Ce que ton enfant apprend</h2><ul>{"".join(f"<li>{x}</li>" for x in j['apprend'])}</ul></div>
        <div class="atout rev"><span aria-hidden="true">👆</span><h2 class="disp">Comment jouer</h2><ol>{"".join(f"<li>{x}</li>" for x in j['comment'])}</ol></div>
        <div class="atout rev"><span aria-hidden="true">💡</span><h2 class="disp">Le conseil pour les parents</h2><p>{j['conseil']}</p></div>
      </div>
    </div>
  </section>
  <section aria-labelledby="t-autres">
    <div class="wrap">
      <div class="titre rev"><span class="badge">🎮 Encore plus de jeux</span><h2 id="t-autres">D'autres jeux gratuits</h2></div>
      <div class="activites">{autres}</div>
    </div>
  </section>
  <section aria-label="À découvrir aussi"><div class="wrap">{PROMO}</div></section>
</main>
""" + fin(["commun", "jeux"])
    ecrire(f"jeux/{j['slug']}/index.html", html)
for j in JEUX_PAGES: page_jeu(j)

# ================================================================ COLORIAGES À IMPRIMER
LIENS_PDF_TOUS = "/coloriages/pdf/coloriages-zoe-et-pico.pdf"
PROMO_CAHIERS_COLORIAGE = f"""<div class="livre-detail rev" style="margin-top:10px">
        <span class="couv"><img src="/img/cahier-grande-section.webp" alt="" width="647" height="844" loading="lazy"></span>
        <div>
          <span class="badge">📚 Pour les parents</span>
          <h2>Encore plus de coloriages dans les cahiers</h2>
          <p>Les cahiers d'activités de Zoé et Pico contiennent aussi des coloriages, avec des labyrinthes, des nombres, des lettres et des jeux de logique, pour la Moyenne Section (4-5 ans) et la Grande Section (5-6 ans).</p>
          <div class="btns"><a class="btn btn-miel" href="/livres/">📚 Découvrir les cahiers</a></div>
        </div>
      </div>"""
coll_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Coloriages à imprimer de Zoé et Pico", "url": SITE + "/coloriages/", "inLanguage": "fr",
           "isAccessibleForFree": True, "hasPart": [{"@type": "ImageObject", "name": f"Coloriage {c['nom']}", "contentUrl": SITE + img_partage(c)[0],
           "url": f"{SITE}/coloriages/{c['slug']}/"} for c in COLORIAGES]}
hub = tete("Coloriages à imprimer gratuits pour enfants (3-6 ans) – Zoé et Pico",
    "Coloriages gratuits à imprimer pour les 3-6 ans : Zoé et Pico à Noël, avec le bonhomme de neige, à la plage, au jardin et en lisant une histoire. Format A4 et PDF, ou à colorier en ligne.",
    "/coloriages/", ld(coll_ld), image=(SITE + img_partage(COLORIAGES[0])[0], 800, 1131, "Coloriage de Zoé et Pico qui décorent le sapin de Noël"),
    fil=[A, ("Coloriages", "/coloriages/")]) + nav("coloriages") + f"""
<main id="contenu">
  <div class="page-tete">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › Coloriages</p>
        <h1>Coloriages à imprimer</h1>
        <p>Des coloriages de Zoé et Pico, gratuits, à imprimer en A4 ou à télécharger en PDF. Ils se colorient aussi en ligne, directement sur la tablette&nbsp;!</p>
        <div class="btns"><a class="btn btn-miel" href="{LIENS_PDF_TOUS}" download>📄 Tous les coloriages (PDF, {len(COLORIAGES)} pages)</a></div>
      </div>
      <img src="/img/pico.webp" alt="" width="360" height="469">
    </div>
  </div>
  <section aria-label="Les coloriages" style="padding-top:10px">
    <div class="wrap"><div class="grille-coloriages grands">{"".join(vignette_coloriage(c, True) for c in COLORIAGES)}</div></div>
  </section>
  <section aria-labelledby="t-astuces">
    <div class="wrap">
      <div class="titre rev"><span class="badge">👨‍👩‍👧 Pour les parents</span><h2 id="t-astuces">Bien imprimer les coloriages</h2></div>
      <div class="parents">
        <div class="atout rev"><span aria-hidden="true">🖨️</span><h3>Imprimer</h3><p>Ouvrez un coloriage et touchez «&nbsp;Imprimer&nbsp;»&nbsp;: seule la feuille A4 s'imprime, sans le reste de la page.</p></div>
        <div class="atout rev"><span aria-hidden="true">📄</span><h3>Le PDF</h3><p>Pratique sur tablette ou pour imprimer plus tard&nbsp;: chaque coloriage existe en PDF, et tous réunis dans un seul fichier.</p></div>
        <div class="atout rev"><span aria-hidden="true">🖍️</span><h3>Gros traits</h3><p>Des contours épais et de grandes zones, adaptés aux petites mains de 3 à 6&nbsp;ans.</p></div>
        <div class="atout rev" id="conditions"><span aria-hidden="true">🏫</span><h3>À la maison et en classe</h3><p>Gratuits pour un usage personnel ou en classe. Merci de ne pas les revendre ni les republier ailleurs.</p></div>
      </div>
    </div>
  </section>
  <section aria-label="Les cahiers"><div class="wrap">{PROMO_CAHIERS_COLORIAGE}</div></section>
</main>
""" + fin(["commun", "jeux"])
ecrire("coloriages/index.html", hub)

def page_coloriage(c):
    autres = "".join(vignette_coloriage(x) for x in COLORIAGES if x is not c)
    img_ld = {"@context": "https://schema.org", "@type": "ImageObject", "name": f"Coloriage {c['nom']} à imprimer", "description": c["desc"],
              "contentUrl": SITE + img_partage(c)[0], "thumbnailUrl": SITE + img_vignette(c)[0],
              "creator": {"@type": "Organization", "name": "Zoé et Pico", "url": SITE + "/"}, "creditText": "Zoé et Pico",
              "copyrightNotice": "© Zoé et Pico", "license": SITE + "/coloriages/#conditions", "acquireLicensePage": SITE + "/coloriages/#conditions"}
    html = tete(f"Coloriage {c['nom']} à imprimer gratuit – Zoé et Pico",
        f"Coloriage gratuit à imprimer : {c['nom']}. {c['desc']} Format A4 ou PDF, ou à colorier en ligne.",
        f"/coloriages/{c['slug']}/", ld(img_ld), image=(SITE + img_partage(c)[0], img_partage(c)[1], img_partage(c)[2], f"Coloriage {c['nom']}"),
        fil=[A, ("Coloriages", "/coloriages/"), (c["titre"], f"/coloriages/{c['slug']}/")]) + nav("coloriages") + f"""
<main id="contenu">
  <div class="page-tete ne-pas-imprimer">
    <div class="wrap">
      <div>
        <p class="fil"><a href="/">Accueil</a> › <a href="/coloriages/">Coloriages</a> › {c['titre']}</p>
        <h1>Coloriage&nbsp;: {c['nom']}</h1>
        <p>{c['desc']}</p>
        <div class="btns">
          <button class="btn btn-miel" type="button" data-imprimer="#feuille">🖨️ Imprimer</button>
          <a class="btn btn-blanc" href="/coloriages/pdf/coloriage-{c['slug']}.pdf" download>📄 PDF</a>
          <a class="btn btn-blanc" href="/jeux/coloriage/#jeu-coloriage-{c['slug']}" data-jeu="coloriage" data-dessin="{c['slug']}">🎨 Colorier en ligne</a>
        </div>
      </div>
    </div>
  </div>
  <section aria-label="La feuille à imprimer" style="padding-top:10px">
    <div class="wrap">
      <div class="feuille" id="feuille">
        <div class="feuille-entete">
          <img src="/img/zoe.webp" alt="" width="324" height="690">
          <p class="feuille-titre">{c.get('phrase') or f"Colorie {c['nom']} avec Zoé et Pico&nbsp;!"}</p>
          <img src="/img/pico-petit.webp" alt="" width="160" height="208">
        </div>
        <p class="feuille-prenom">Mon prénom&nbsp;: ............................................</p>
        <img class="feuille-dessin" src="{img_feuille(c)[0]}" alt="Coloriage {c['nom']} à imprimer, avec de gros contours pour les 3-6 ans" width="{img_feuille(c)[1]}" height="{img_feuille(c)[2]}">
        <p class="feuille-pied">zoeetpico.fr · d'autres coloriages, des jeux gratuits et les cahiers d'activités de Zoé et Pico</p>
      </div>
    </div>
  </section>
  <section class="ne-pas-imprimer" aria-labelledby="t-autres">
    <div class="wrap">
      <div class="titre rev"><span class="badge">🖍️ Encore plus</span><h2 id="t-autres">D'autres coloriages</h2></div>
      <div class="grille-coloriages">{autres}</div>
      {PROMO_CAHIERS_COLORIAGE}
    </div>
  </section>
</main>
""" + fin(["commun", "jeux"])
    ecrire(f"coloriages/{c['slug']}/index.html", html)
for c in COLORIAGES: page_coloriage(c)

# ================================================================ SITEMAP
PAGES_SITEMAP.append("/jeu/")
prio = lambda u: "1.0" if u == "/" else "0.8" if u.count("/") == 2 else "0.6"
ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-11-04</lastmod></url>\n" for u in PAGES_SITEMAP) + "</urlset>\n")
print("ok", len(PAGES_SITEMAP), "pages dans le sitemap")
