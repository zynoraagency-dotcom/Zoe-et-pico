# Génère les dessins à colorier (SVG) de Zoé et Pico : style « kawaii » inspiré des coloriages de la marque
# (soleil à rayons arrondis, visages aux yeux fermés, joues rondes, cœurs et étincelles), gros traits arrondis.
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

def f(v):
    return f"{v:.1f}"

def joyeux(x, y, s=1.0, bouche=False, joues=True):
    """visage aux yeux fermés qui sourit (comme sur les coloriages de Zoé et Pico)"""
    w = max(2.5, 4 * s)
    out = trait(f"M{f(x - 17 * s)} {f(y)} Q{f(x - 11 * s)} {f(y - 9 * s)} {f(x - 5 * s)} {f(y)}", w)
    out += trait(f"M{f(x + 5 * s)} {f(y)} Q{f(x + 11 * s)} {f(y - 9 * s)} {f(x + 17 * s)} {f(y)}", w)
    if bouche:
        out += z("path", sw=f(max(2.5, 3.6 * s)), d=f"M{f(x - 8 * s)} {f(y + 7 * s)} Q{f(x)} {f(y + 24 * s)} {f(x + 8 * s)} {f(y + 7 * s)} Z")
    else:
        out += trait(f"M{f(x - 7 * s)} {f(y + 7 * s)} Q{f(x)} {f(y + 15 * s)} {f(x + 7 * s)} {f(y + 7 * s)}", w)
    if joues:
        for dx in (-23, 23):
            out += z("circle", sw=f(max(2, 3 * s)), cx=f(x + dx * s), cy=f(y + 8 * s), r=f(5.5 * s))
    return out

def soleil(cx, cy, r=34):
    s = r / 34
    out = ""
    for i in range(10):
        out += z("rect", sw=5, x=f(cx - 7 * s), y=f(cy - r - 12 * s - 24 * s), width=f(14 * s), height=f(24 * s), rx=f(7 * s), transform=f"rotate({i * 36} {cx} {cy})")
    return out + z("circle", cx=cx, cy=cy, r=r) + joyeux(cx, cy - 2 * s, s, bouche=True)

def nuage_z(cx, cy, s=1.0, visage_=True):
    pts = [(-64, 24), (-84, 22, -80, 2), (-76, -16, -54, -14), (-50, -40, -22, -38), (-8, -62, 18, -50), (40, -60, 52, -36), (78, -36, 78, -10), (92, 4, 80, 18), (76, 26, 64, 24)]
    d = f"M{f(cx + pts[0][0] * s)} {f(cy + pts[0][1] * s)} " + "".join(f"Q{f(cx + a * s)} {f(cy + b * s)} {f(cx + c_ * s)} {f(cy + e * s)} " for a, b, c_, e in pts[1:]) + "Z"
    return z("path", d=d) + (joyeux(cx, cy - 4 * s, s * .9) if visage_ else "")

def eclat(x, y, r=12):
    """étincelle à quatre branches"""
    k = r * .18
    return z("path", sw=3.5, d=f"M{x} {y - r} Q{f(x + k)} {f(y - k)} {x + r} {y} Q{f(x + k)} {f(y + k)} {x} {y + r} Q{f(x - k)} {f(y + k)} {x - r} {y} Q{f(x - k)} {f(y - k)} {x} {y - r}Z")

def flocon(x, y, r=14):
    d = ""
    for a in (0, 60, 120):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        d += f"M{f(x - r * ca)} {f(y - r * sa)} L{f(x + r * ca)} {f(y + r * sa)} "
        for sgn in (-1, 1):
            bx, by = x + sgn * r * .62 * ca, y + sgn * r * .62 * sa
            for t in (-1, 1):
                b = math.radians(a + t * 40)
                d += f"M{f(bx)} {f(by)} L{f(bx + sgn * r * .32 * math.cos(b))} {f(by + sgn * r * .32 * math.sin(b))} "
    return trait(d.strip(), 3.5)

def herbe(x, y):
    return trait(f"M{x - 9} {y} Q{x - 8} {y - 10} {x - 12} {y - 18} M{x} {y} V{y - 20} M{x + 9} {y} Q{x + 8} {y - 10} {x + 12} {y - 18}", 4)

def svg(slug, titre, corps):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="5 5 390 390" role="img" aria-label="Coloriage : {titre}">'
            f'<title>Coloriage {titre} – Zoé et Pico</title>'
            f'<rect x="0" y="0" width="400" height="400" fill="#fff" stroke="none" data-z=""/>' + corps + '</svg>\n')

DESSINS = {}

# ---------------------------------------------------------------- le sapin de Noël
c = nuage_z(82, 62, .72) + coeur(300, 22, .9) + eclat(36, 176, 12) + eclat(366, 196, 11) + coeur(332, 120, .75)
c += z("path", d="M0 356 Q200 336 400 356 V400 H0Z")
c += z("rect", x=182, y=296, width=36, height=36, rx=5)
def etage(ytop, ht, ybot, hb, n):
    d = f"M{200 - ht} {ytop} L{200 - hb} {ybot} "
    pas = 2 * hb / n
    for k in range(n):
        x0 = 200 - hb + k * pas
        d += f"Q{f(x0 + pas / 2)} {ybot + 14} {f(x0 + pas)} {ybot} "
    return z("path", d=d + f"L{200 + ht} {ytop} Z")
c += etage(196, 42, 300, 112, 6) + etage(132, 26, 226, 82, 5) + etage(88, 0, 160, 50, 4)
for (x, y, r) in [(176, 148, 10), (222, 196, 12), (154, 262, 13), (246, 270, 13), (196, 236, 10)]:
    c += z("circle", sw=5, cx=x, cy=y, r=r) + trait(f"M{x - r + 2} {y - 3} H{x + r - 2} M{x - r + 3} {y + 4} H{x + r - 3}", 3)
    c += z("rect", sw=3.5, x=x - 4, y=y - r - 6, width=8, height=7, rx=2)
c += z("polygon", sw=4, points=etoile(226, 150, 10, 4.5)) + z("polygon", sw=4, points=etoile(178, 196, 9, 4)) + z("polygon", sw=4, points=etoile(206, 278, 10, 4.5))
c += trait("M200 40 V28 M172 50 L163 41 M228 50 L237 41", 4.5)
c += z("polygon", sw=6, points=etoile(200, 80, 32, 15)) + joyeux(200, 82, .55)
c += z("rect", x=90, y=304, width=72, height=54, rx=6) + z("rect", x=84, y=292, width=84, height=18, rx=6) + z("rect", sw=4, x=119, y=292, width=14, height=66, rx=2)
c += z("path", sw=5, d="M126 292 Q104 268 98 282 Q96 296 126 294 Z") + z("path", sw=5, d="M126 292 Q148 268 154 282 Q156 296 126 294 Z")
c += z("rect", x=248, y=312, width=64, height=46, rx=6) + z("rect", x=242, y=300, width=76, height=17, rx=6) + z("rect", sw=4, x=273, y=300, width=14, height=58, rx=2)
c += z("path", sw=5, d="M280 300 Q262 280 257 292 Q256 304 280 302 Z") + z("path", sw=5, d="M280 300 Q298 280 303 292 Q304 304 280 302 Z")
c += z("circle", sw=3.5, cx=258, cy=336, r=5) + z("circle", sw=3.5, cx=302, cy=342, r=5)
DESSINS["sapin"] = ("Le sapin de Noël", c)

# ---------------------------------------------------------------- le bonhomme de neige
c = nuage_z(88, 62, .75) + coeur(300, 36, .9) + coeur(40, 230, .7) + eclat(350, 110, 11)
c += flocon(200, 36, 15) + flocon(46, 156, 14) + flocon(354, 196, 15) + flocon(282, 96, 11)
c += z("path", d="M0 334 Q100 304 200 326 Q300 306 400 330 V400 H0Z")
c += z("ellipse", sw=5, cx=62, cy=362, rx=26, ry=11) + z("ellipse", sw=5, cx=346, cy=366, rx=22, ry=10)
c += trait("M140 270 L96 238 M114 252 L100 232 M260 270 L304 238 M286 252 L300 232", 6)
c += z("circle", cx=200, cy=282, r=72)
c += z("circle", sw=4.5, cx=200, cy=262, r=8) + z("circle", sw=4.5, cx=200, cy=292, r=8) + z("circle", sw=4.5, cx=200, cy=322, r=8)
c += z("circle", cx=200, cy=172, r=54)
c += z("path", d="M148 206 Q200 230 252 206 L256 226 Q200 254 144 226 Z")
c += z("path", d="M222 230 L248 226 L250 290 L222 292 Z") + trait("M223 252 H249 M223 272 H250 M228 292 V302 M236 292 V303 M244 291 V302", 4)
c += z("path", d="M150 150 Q150 92 200 90 Q250 92 250 150 Z") + trait("M158 130 Q200 120 242 130 M166 110 Q200 102 234 110", 4)
c += z("rect", x=140, y=140, width=120, height=26, rx=13) + z("circle", sw=5, cx=200, cy=82, r=17)
c += trait("M171 178 Q177 170 183 178 M217 178 Q223 170 229 178", 4.5)
c += z("circle", sw=3, cx=168, cy=192, r=6) + z("circle", sw=3, cx=232, cy=192, r=6)
c += z("path", sw=4.5, d="M197 184 L238 192 L197 199 Z") + trait("M186 206 Q200 214 214 206", 4)
DESSINS["bonhomme-de-neige"] = ("Le bonhomme de neige", c)

# ---------------------------------------------------------------- le jardin ensoleillé
c = soleil(326, 74, 28) + nuage_z(96, 70, .8) + coeur(194, 36, .9) + eclat(232, 112, 11) + eclat(30, 150, 9)
c += z("path", d="M0 268 Q90 222 200 254 Q300 228 400 248 V400 H0Z")
c += z("rect", x=322, y=150, width=18, height=40, rx=3)
c += z("path", d="M228 204 L290 146 L352 204 Z")
c += z("rect", x=240, y=200, width=100, height=80, rx=8)
c += z("rect", x=252, y=214, width=22, height=22, rx=5) + z("rect", x=306, y=214, width=22, height=22, rx=5)
c += trait("M263 214 V236 M252 225 H274 M317 214 V236 M306 225 H328", 3)
c += z("path", d="M276 280 V252 Q276 236 290 236 Q304 236 304 252 V280 Z")
c += z("path", d="M0 318 Q110 284 220 312 Q312 334 400 302 V400 H0Z")
c += z("path", d="M105 340 Q99 290 107 238 L117 238 Q110 290 115 340 Z")
c += z("path", d="M107 302 Q74 296 66 268 Q98 266 110 292 Z") + z("path", d="M114 282 Q144 270 154 244 Q124 244 113 270 Z")
c += fleur(112, 200, 26, 6, 5) + joyeux(112, 198, .62, joues=False)
c += z("path", d="M326 352 Q324 322 331 312 L355 312 Q362 322 360 352 Z")
c += z("path", d="M308 316 Q310 274 343 272 Q376 274 378 316 Q343 324 308 316 Z")
c += z("circle", sw=4, cx=330, cy=294, r=7) + z("circle", sw=4, cx=352, cy=287, r=6) + z("circle", sw=4, cx=366, cy=302, r=5)
c += herbe(36, 376) + herbe(196, 384) + herbe(256, 362)
DESSINS["jardin"] = ("Le jardin ensoleillé", c)

# ---------------------------------------------------------------- le papillon
c = eclat(60, 64, 12) + eclat(96, 36, 8) + eclat(344, 44, 12) + eclat(374, 204, 9) + eclat(26, 214, 9) + coeur(296, 20, .65)
c += z("path", d="M0 334 Q200 292 400 334 V400 H0Z")
c += fleur(66, 352, 13, 5, 4) + fleur(338, 356, 13, 5, 4) + fleur(200, 370, 10, 5, 3)
c += z("path", d="M192 172 C150 70 46 58 50 140 C54 198 132 208 192 198 Z") + z("path", d="M208 172 C250 70 354 58 350 140 C346 198 268 208 208 198 Z")
c += z("path", d="M192 208 C140 212 76 252 96 298 C116 338 180 292 192 238 Z") + z("path", d="M208 208 C260 212 324 252 304 298 C284 338 220 292 208 238 Z")
c += z("circle", sw=5, cx=110, cy=134, r=24) + z("circle", sw=4, cx=152, cy=106, r=11) + z("circle", sw=5, cx=290, cy=134, r=24) + z("circle", sw=4, cx=248, cy=106, r=11)
c += coeur(116, 254, 1) + coeur(256, 254, 1)
c += trait("M188 118 Q176 86 160 76 M212 118 Q224 86 240 76", 5)
c += z("circle", sw=5, cx=157, cy=73, r=9) + z("circle", sw=5, cx=243, cy=73, r=9)
c += z("ellipse", cx=200, cy=228, rx=17, ry=62) + trait("M186 206 Q200 212 214 206 M185 232 Q200 238 215 232 M187 258 Q200 264 213 258", 4)
c += z("circle", cx=200, cy=144, r=32) + visage(200, 144, .95)
DESSINS["papillon"] = ("Le papillon", c)

# ---------------------------------------------------------------- l'arc-en-ciel
c = soleil(348, 62, 22) + coeur(36, 60, 1.05) + coeur(96, 110, .7) + eclat(162, 50, 11) + eclat(252, 36, 8)
c += z("path", d="M0 316 Q200 296 400 316 V400 H0Z")
for (R, r) in [(178, 152), (152, 126), (126, 100), (100, 74)]:
    c += z("path", d=f"M{200 - R} 304 A{R} {R} 0 0 1 {200 + R} 304 L{200 + r} 304 A{r} {r} 0 0 0 {200 - r} 304 Z")
c += z("path", d="M126 304 A74 74 0 0 1 274 304 Z")
c += nuage_z(58, 292, .78) + nuage_z(342, 292, .78)
c += fleur(150, 360, 12, 5, 4) + fleur(250, 364, 12, 5, 4) + herbe(70, 380) + herbe(330, 382)
DESSINS["arc-en-ciel"] = ("L'arc-en-ciel", c)

# ---------------------------------------------------------------- le poisson
c = z("circle", sw=4, cx=96, cy=104, r=13) + z("circle", sw=4, cx=72, cy=72, r=9) + z("circle", sw=4, cx=104, cy=48, r=6)
c += z("circle", sw=4, cx=318, cy=78, r=11) + z("circle", sw=4, cx=340, cy=52, r=7) + eclat(250, 46, 10)
c += z("path", d="M0 334 Q100 312 200 330 T400 322 V400 H0Z")
c += z("path", d="M54 334 C34 292 78 262 56 222 C46 202 66 186 70 168 C92 200 70 222 82 252 C96 284 72 304 82 334 Z")
c += z("path", d="M340 334 C322 302 354 272 340 238 C364 262 368 304 358 334 Z")
c += z("path", d="M276 192 L346 138 Q330 192 346 246 Z") + z("path", d="M132 142 Q170 62 244 132 Z") + z("path", d="M150 244 Q180 312 230 248 Z")
c += z("ellipse", cx=186, cy=192, rx=98, ry=68)
c += z("path", sw=5, d="M222 130 Q240 192 222 254 L240 252 Q258 192 240 132 Z") + z("path", sw=5, d="M254 142 Q268 192 254 242 L266 236 Q278 192 266 148 Z")
c += z("path", sw=5, d="M186 202 Q214 184 226 214 Q204 226 186 202 Z")
c += z("circle", sw=5, cx=134, cy=176, r=22)
c += f'<circle cx="138" cy="178" r="12" fill="{ENCRE}" pointer-events="none"/><circle cx="143" cy="173" r="4.5" fill="#fff" pointer-events="none"/>'
c += trait("M104 210 Q114 220 124 210", 4) + z("circle", sw=3, cx=152, cy=212, r=6)
c += z("polygon", sw=5, points=etoile(306, 356, 30, 13)) + joyeux(306, 356, .42, joues=False)
c += z("path", sw=4, d="M150 372 Q150 352 170 352 Q190 352 190 372 Z") + trait("M160 372 L165 356 M170 372 V354 M180 372 L175 356", 3)
DESSINS["poisson"] = ("Le poisson", c)

if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    for slug, (titre, corps) in DESSINS.items():
        open(os.path.join(SORTIE, slug + ".svg"), "w", encoding="utf-8").write(svg(slug, titre, corps))
        print(slug, corps.count("data-z") + 1, "zones")
