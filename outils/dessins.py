# Génère les dessins à colorier (SVG) de Zoé et Pico : style « kawaii », gros traits arrondis.
# Chaque zone coloriable porte l'attribut data-z ; les détails (yeux, sourires) laissent passer le clic.
# Utilisation : python3 outils/dessins.py   (depuis la racine du site)
import math, os, sys

RACINE = sys.argv[1] if len(sys.argv) > 1 else "."
SORTIE = os.path.join(RACINE, "coloriages", "svg")
ENCRE = "#3b2a1a"

def _a(d):
    return " ".join(f'{k.rstrip("_").replace("_", "-")}="{v}"' for k, v in d.items())

def z(tag, sw=6, **a):
    """zone à colorier"""
    return f'<{tag} {_a(a)} fill="#fff" stroke="{ENCRE}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" data-z=""/>'

def trait(d, w=5):
    return f'<path d="{d}" fill="none" stroke="{ENCRE}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" pointer-events="none"/>'

def oeil(x, y, r=5):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{ENCRE}" pointer-events="none"/>'
            f'<circle cx="{x + r * .38:.1f}" cy="{y - r * .38:.1f}" r="{r * .36:.1f}" fill="#fff" pointer-events="none"/>')

def visage(x, y, s=1.0, joues=True):
    e = 11 * s
    out = oeil(x - e, y, 4.6 * s) + oeil(x + e, y, 4.6 * s)
    out += trait(f"M{x - 6 * s:.1f} {y + 8 * s:.1f} Q{x:.1f} {y + 14 * s:.1f} {x + 6 * s:.1f} {y + 8 * s:.1f}", max(2.5, 3.6 * s))
    if joues:
        out += z("ellipse", sw=max(2, 3 * s), cx=f"{x - 18 * s:.1f}", cy=f"{y + 8 * s:.1f}", rx=f"{5.5 * s:.1f}", ry=f"{3.6 * s:.1f}")
        out += z("ellipse", sw=max(2, 3 * s), cx=f"{x + 18 * s:.1f}", cy=f"{y + 8 * s:.1f}", rx=f"{5.5 * s:.1f}", ry=f"{3.6 * s:.1f}")
    return out

def rayons(cx, cy, r1, r2, n=10, demi=.16):
    d = ""
    for i in range(n):
        a = i / n * 2 * math.pi
        p1 = (cx + r1 * math.cos(a - demi), cy + r1 * math.sin(a - demi))
        p2 = (cx + r2 * math.cos(a), cy + r2 * math.sin(a))
        p3 = (cx + r1 * math.cos(a + demi), cy + r1 * math.sin(a + demi))
        d += f"M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{p3[0]:.1f} {p3[1]:.1f} Z "
    return d.strip()

def nuage(cx, cy, s=1.0):
    p = [(-46, 22), (-62, 20, -60, 0), (-58, -16, -36, -14), (-30, -40, -4, -36), (16, -52, 34, -30), (58, -32, 58, -6), (70, 8, 58, 22)]
    d = f"M{cx + p[0][0] * s:.1f} {cy + p[0][1] * s:.1f} "
    for q in p[1:]:
        if len(q) == 4:
            d += f"Q{cx + q[0] * s:.1f} {cy + q[1] * s:.1f} {cx + q[2] * s:.1f} {cy + q[3] * s:.1f} "
    return d + "Z"

def fleur(cx, cy, r=12, n=5, sw=4, visage_=False):
    out = ""
    for i in range(n):
        a = i / n * 2 * math.pi - math.pi / 2
        out += z("ellipse", sw=sw, cx=f"{cx + r * 1.15 * math.cos(a):.1f}", cy=f"{cy + r * 1.15 * math.sin(a):.1f}", rx=f"{r * .85:.1f}", ry=f"{r * .62:.1f}",
                 transform=f"rotate({math.degrees(a) + 90:.0f} {cx + r * 1.15 * math.cos(a):.1f} {cy + r * 1.15 * math.sin(a):.1f})")
    out += z("circle", sw=sw, cx=cx, cy=cy, r=f"{r * .75:.1f}")
    if visage_:
        out += visage(cx, cy - 2, r / 30, joues=False)
    return out

def coeur(x, y, s=1.0):
    return z("path", sw=4, d=f"M{x:.1f} {y + 6 * s:.1f} C{x:.1f} {y - 4 * s:.1f} {x + 12 * s:.1f} {y - 6 * s:.1f} {x + 14 * s:.1f} {y + 3 * s:.1f} "
             f"C{x + 16 * s:.1f} {y - 6 * s:.1f} {x + 28 * s:.1f} {y - 4 * s:.1f} {x + 28 * s:.1f} {y + 6 * s:.1f} C{x + 28 * s:.1f} {y + 16 * s:.1f} {x + 14 * s:.1f} {y + 26 * s:.1f} {x + 14 * s:.1f} {y + 26 * s:.1f} "
             f"C{x + 14 * s:.1f} {y + 26 * s:.1f} {x:.1f} {y + 16 * s:.1f} {x:.1f} {y + 6 * s:.1f}Z")

def etincelle(x, y, t=8):
    return trait(f"M{x} {y - t} V{y + t} M{x - t} {y} H{x + t}", 4)

def etoile(cx, cy, r1, r2, n=5):
    pts = []
    for i in range(n * 2):
        a = i / (n * 2) * 2 * math.pi - math.pi / 2
        r = r1 if i % 2 == 0 else r2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)

def svg(slug, titre, corps):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="Coloriage : {titre}">'
            f'<title>Coloriage {titre} – Zoé et Pico</title>'
            f'<defs><clipPath id="cadre-{slug}"><rect x="4" y="4" width="392" height="392" rx="26"/></clipPath></defs>'
            f'<g clip-path="url(#cadre-{slug})">'
            + z("rect", x=0, y=0, width=400, height=400) + corps +
            '</g>'
            f'<rect x="4" y="4" width="392" height="392" rx="26" fill="none" stroke="{ENCRE}" stroke-width="7" pointer-events="none"/>'
            '</svg>\n')

DESSINS = {}

# ---------------------------------------------------------------- 1. le jardin ensoleillé
c = ""
c += z("path", d=rayons(320, 82, 48, 70, 10))
c += z("circle", cx=320, cy=82, r=40) + visage(320, 80, 1)
c += z("path", d=nuage(100, 82, 1)) + visage(100, 74, .8)
c += etincelle(200, 50) + etincelle(232, 96, 6)
c += z("path", d="M0 262 Q90 214 200 250 Q300 222 400 244 V400 H0Z")
c += z("rect", x=322, y=146, width=18, height=40, rx=3)
c += z("path", d="M228 200 L290 142 L352 200 Z")
c += z("rect", x=240, y=196, width=100, height=82, rx=8)
c += z("rect", x=252, y=212, width=22, height=22, rx=5) + z("rect", x=306, y=212, width=22, height=22, rx=5)
c += trait("M263 212 V234 M252 223 H274 M317 212 V234 M306 223 H328", 3)
c += z("path", d="M276 278 V250 Q276 234 290 234 Q304 234 304 250 V278 Z")
c += z("path", d="M0 318 Q110 284 220 312 Q312 334 400 302 V400 H0Z")
c += z("path", d="M105 340 Q99 290 107 238 L117 238 Q110 290 115 340 Z")
c += z("path", d="M107 302 Q74 296 66 268 Q98 266 110 292 Z")
c += z("path", d="M114 282 Q144 270 154 244 Q124 244 113 270 Z")
c += fleur(112, 200, 26, 6, 5, visage_=True)
c += z("path", d="M326 352 Q324 322 331 312 L355 312 Q362 322 360 352 Z")
c += z("path", d="M308 316 Q310 274 343 272 Q376 274 378 316 Q343 324 308 316 Z")
c += z("circle", sw=4, cx=330, cy=294, r=7) + z("circle", sw=4, cx=352, cy=287, r=6) + z("circle", sw=4, cx=366, cy=302, r=5)
c += trait("M30 372 l7 -16 l7 16 M190 380 l7 -16 l7 16 M250 360 l6 -14 l6 14", 4)
DESSINS["jardin"] = ("Le jardin ensoleillé", c)

# ---------------------------------------------------------------- 2. le papillon
c = ""
c += etincelle(60, 64) + etincelle(92, 40, 5) + etincelle(340, 40) + etincelle(374, 200, 6) + etincelle(28, 210, 6)
c += coeur(300, 26, .6)
c += z("path", d="M0 334 Q200 292 400 334 V400 H0Z")
c += fleur(66, 352, 13, 5, 4) + fleur(338, 356, 13, 5, 4) + fleur(200, 370, 10, 5, 3)
c += z("path", d="M192 172 C150 70 46 58 50 140 C54 198 132 208 192 198 Z")
c += z("path", d="M208 172 C250 70 354 58 350 140 C346 198 268 208 208 198 Z")
c += z("path", d="M192 208 C140 212 76 252 96 298 C116 338 180 292 192 238 Z")
c += z("path", d="M208 208 C260 212 324 252 304 298 C284 338 220 292 208 238 Z")
c += z("circle", sw=5, cx=110, cy=134, r=24) + z("circle", sw=4, cx=152, cy=106, r=11)
c += z("circle", sw=5, cx=290, cy=134, r=24) + z("circle", sw=4, cx=248, cy=106, r=11)
c += coeur(116, 254, 1) + coeur(256, 254, 1)
c += trait("M188 118 Q176 86 160 76 M212 118 Q224 86 240 76", 5)
c += z("circle", sw=5, cx=157, cy=73, r=9) + z("circle", sw=5, cx=243, cy=73, r=9)
c += z("ellipse", cx=200, cy=228, rx=17, ry=62)
c += trait("M186 206 Q200 212 214 206 M185 232 Q200 238 215 232 M187 258 Q200 264 213 258", 4)
c += z("circle", cx=200, cy=144, r=32) + visage(200, 144, .95)
DESSINS["papillon"] = ("Le papillon", c)

# ---------------------------------------------------------------- 3. l'arc-en-ciel
c = ""
c += z("path", d=rayons(346, 64, 34, 50, 9))
c += z("circle", cx=346, cy=64, r=27) + visage(346, 62, .65, joues=False)
c += coeur(42, 64, 1.05) + coeur(98, 112, .7) + etincelle(160, 52) + etincelle(256, 40, 6)
c += z("path", d="M0 316 Q200 296 400 316 V400 H0Z")
for i, (R, r) in enumerate([(178, 152), (152, 126), (126, 100), (100, 74)]):
    c += z("path", d=f"M{200 - R} 304 A{R} {R} 0 0 1 {200 + R} 304 L{200 + r} 304 A{r} {r} 0 0 0 {200 - r} 304 Z")
c += z("path", d="M126 304 A74 74 0 0 1 274 304 Z")
c += z("path", d=nuage(56, 292, .95)) + visage(56, 286, .75)
c += z("path", d=nuage(344, 292, .95)) + visage(344, 286, .75)
c += fleur(150, 358, 12, 5, 4) + fleur(250, 362, 12, 5, 4)
c += trait("M70 370 l7 -15 l7 15 M318 376 l7 -15 l7 15", 4)
DESSINS["arc-en-ciel"] = ("L'arc-en-ciel", c)

# ---------------------------------------------------------------- 4. le poisson
c = ""
c += z("circle", sw=4, cx=96, cy=104, r=13) + z("circle", sw=4, cx=72, cy=72, r=9) + z("circle", sw=4, cx=104, cy=48, r=6)
c += z("circle", sw=4, cx=318, cy=78, r=11) + z("circle", sw=4, cx=340, cy=52, r=7)
c += z("path", d="M0 334 Q100 312 200 330 T400 322 V400 H0Z")
c += z("path", d="M54 334 C34 292 78 262 56 222 C46 202 66 186 70 168 C92 200 70 222 82 252 C96 284 72 304 82 334 Z")
c += z("path", d="M340 334 C322 302 354 272 340 238 C364 262 368 304 358 334 Z")
c += z("path", d="M276 192 L346 138 Q330 192 346 246 Z")
c += z("path", d="M132 142 Q170 62 244 132 Z")
c += z("path", d="M150 244 Q180 312 230 248 Z")
c += z("ellipse", cx=186, cy=192, rx=98, ry=68)
c += z("path", sw=5, d="M222 130 Q240 192 222 254 L240 252 Q258 192 240 132 Z")
c += z("path", sw=5, d="M254 142 Q268 192 254 242 L266 236 Q278 192 266 148 Z")
c += z("path", sw=5, d="M186 202 Q214 184 226 214 Q204 226 186 202 Z")
c += z("circle", sw=5, cx=134, cy=176, r=22)
c += f'<circle cx="138" cy="178" r="12" fill="{ENCRE}" pointer-events="none"/><circle cx="143" cy="173" r="4.5" fill="#fff" pointer-events="none"/>'
c += trait("M104 210 Q114 220 124 210", 4) + z("ellipse", sw=3, cx=150, cy=212, rx=8, ry=5)
c += z("polygon", sw=5, points=etoile(306, 356, 30, 13)) + visage(306, 356, .45, joues=False)
c += z("path", sw=4, d="M150 372 Q150 352 170 352 Q190 352 190 372 Z")
c += trait("M160 372 L165 356 M170 372 V354 M180 372 L175 356", 3)
DESSINS["poisson"] = ("Le poisson", c)

if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    for slug, (titre, corps) in DESSINS.items():
        open(os.path.join(SORTIE, slug + ".svg"), "w", encoding="utf-8").write(svg(slug, titre, corps))
        print(slug, corps.count("data-z") + 1, "zones")
