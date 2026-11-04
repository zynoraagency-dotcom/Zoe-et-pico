# Prépare les coloriages dessinés de Zoé et Pico (fichiers PNG fournis) :
#  - <slug>-impression.png : 2 x plus grand, traits nettoyés, pour l'impression A4 et les PDF
#  - <slug>.png            : 800 px de large, pour le site et le coloriage en ligne
#  - <slug>-vignette.webp  : 400 px de large, pour les listes
# Utilisation (depuis la racine du site) : python3 outils/images_coloriages.py .
import glob, os, sys
from PIL import Image
RACINE = sys.argv[1] if len(sys.argv) > 1 else "."
D = os.path.join(RACINE, "coloriages", "zoe-et-pico")
def nettoyer(im):
    # noir franc pour les traits, blanc pur pour le papier, dégradé doux entre les deux
    return im.point(lambda v: 0 if v < 100 else 255 if v > 215 else int((v - 100) * 255 / 115))
for src in sorted(glob.glob(os.path.join(D, "originaux", "*.png"))):
    slug = os.path.splitext(os.path.basename(src))[0]
    im = Image.open(src).convert("L")
    w, h = im.size
    nettoyer(im.resize((w * 2, h * 2), Image.LANCZOS)).save(os.path.join(D, f"{slug}-impression.png"), optimize=True)
    web = nettoyer(im.resize((800, round(h * 800 / w)), Image.LANCZOS)); web.save(os.path.join(D, f"{slug}.png"), optimize=True)
    web.resize((400, round(h * 400 / w)), Image.LANCZOS).save(os.path.join(D, f"{slug}-vignette.webp"), "WEBP", quality=82, method=6)
    print(slug, "ok")
