/* =========================================================
   Zoé et Pico — la salle de jeu
   Toute carte avec data-jeu="memo|compter|couleurs|formes|lucioles|coloriage"
   ouvre le jeu en plein écran. Lien direct possible : /jeux/#jeu-couleurs
   Le bouton « retour » du téléphone ferme le jeu au lieu de quitter le site.
   ========================================================= */
"use strict";
(() => {
  const { parle, son, hasard, melange, confettis } = ZP;
  const PICO = "/img/pico-petit.webp", ZOE = "/img/zoe.webp";
  const MOTS = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix"];

  /* ---------- la fenêtre de jeu ---------- */
  const salle = document.createElement("dialog");
  salle.className = "salle"; salle.setAttribute("aria-labelledby", "salle-titre");
  salle.innerHTML = `
    <div class="salle-haut">
      <button class="rond" id="retour" type="button" aria-label="Retour">←</button>
      <h2 id="salle-titre" class="disp">Jeu</h2>
      <div class="lumieres" id="etoiles" role="img" aria-label="Progression"></div>
      <button class="rond miel" id="repeter" type="button" aria-label="Répéter la consigne">🔊</button>
    </div>
    <div class="plateau" id="plateau"></div>
    <div class="fin" id="fin" aria-live="polite">
      <div class="persos"><img class="z" src="${ZOE}" alt="" width="324" height="690"><img class="p" src="${PICO}" alt="" width="160" height="208"></div>
      <h3>Bravo&nbsp;!</h3>
      <div class="boutons">
        <button class="btn btn-miel" id="rejouer" type="button">🔁 Rejouer</button>
        <button class="btn btn-blanc" id="autres" type="button">🎮 Autres jeux</button>
      </div>
      <p class="promo">Parents&nbsp;: retrouvez Zoé et Pico dans <a href="/livres/">leurs cahiers d'activités</a> et sur <a href="/videos/">leur chaîne YouTube</a>.</p>
    </div>`;
  document.body.appendChild(salle);
  const $ = id => salle.querySelector("#" + id);
  const plateau = $("plateau"), fin = $("fin"), etoiles = $("etoiles");
  let jeuActuel = null, minuteurs = [], intervalles = [];
  const plusTard = (f, ms) => minuteurs.push(setTimeout(f, ms));

  function nettoyer() {
    minuteurs.forEach(clearTimeout); minuteurs = [];
    intervalles.forEach(clearInterval); intervalles = [];
    plateau.innerHTML = ""; fin.classList.remove("vue"); ZP.tais();
  }
  function preparerEtoiles(n) { etoiles.innerHTML = "<i></i>".repeat(n); majEtoiles(); }
  function majEtoiles() { const t = etoiles.children.length, on = etoiles.querySelectorAll(".on").length; etoiles.setAttribute("aria-label", `${on} sur ${t}`); }
  function gagneEtoile(i) { const e = etoiles.children[i]; if (e) e.classList.add("on"); majEtoiles(); }
  function bullePico(texte) {
    const z = document.createElement("div"); z.className = "consigne-zone";
    z.innerHTML = `<img src="${PICO}" alt="" width="160" height="208"><div class="consigne" aria-live="polite"></div>`;
    z.querySelector(".consigne").textContent = texte;
    plateau.appendChild(z); return z.querySelector(".consigne");
  }
  function victoire(msg = "Bravo, tu as gagné !") {
    plusTard(() => { son("fin"); confettis(); parle(msg); fin.classList.add("vue"); $("rejouer").focus(); }, 600);
  }

  function ouvrir(nom, sansHistorique) {
    if (!JEUX[nom]) return;
    nettoyer(); jeuActuel = nom;
    $("salle-titre").textContent = JEUX[nom].titre;
    if (!salle.open) { salle.showModal(); document.body.style.overflow = "hidden"; }
    if (!sansHistorique) history.pushState({ jeu: nom }, "", "#jeu-" + nom);
    son("clic"); JEUX[nom].lancer();
  }
  function fermer(depuisHistorique) {
    if (!salle.open) return;
    if (!depuisHistorique && history.state && history.state.jeu) { history.back(); return; }
    nettoyer(); salle.close(); document.body.style.overflow = ""; jeuActuel = null;
  }
  ZP.ouvrirJeu = ouvrir;
  addEventListener("popstate", e => {
    if (e.state && e.state.jeu) return ouvrir(e.state.jeu, true);
    const m = location.hash.match(/^#jeu-(\w+)$/);
    if (m && JEUX[m[1]]) { history.replaceState(null, "", location.pathname + location.search); ouvrir(m[1]); }
    else fermer(true);
  });
  salle.addEventListener("cancel", e => { e.preventDefault(); fermer(); });
  $("retour").addEventListener("click", () => fermer());
  $("rejouer").addEventListener("click", () => ouvrir(jeuActuel, true));
  $("autres").addEventListener("click", () => {
    fermer();
    const liste = document.getElementById("jeux");
    if (liste) setTimeout(() => liste.scrollIntoView({ behavior: ZP.calme ? "auto" : "smooth" }), 120);
    else location.href = "/jeux/";
  });
  $("repeter").addEventListener("click", () => ZP.derniereParole && parle(ZP.derniereParole));
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-jeu]");
    if (b) { e.preventDefault(); ouvrir(b.dataset.jeu); }
  });

  /* ---------- quiz générique ---------- */
  function quiz({ tours = 8, question }) {
    preparerEtoiles(tours);
    let tour = 0;
    const suivant = () => {
      if (tour >= tours) return victoire();
      plateau.innerHTML = "";
      const q = question(tour);
      bullePico(q.texte);
      if (q.avant) plateau.appendChild(q.avant);
      const zone = document.createElement("div"); zone.className = q.classe || "choix";
      let bloque = false;
      q.choix.forEach(ch => {
        const b = ch.el; b.type = "button";
        b.addEventListener("click", () => {
          if (bloque) return;
          if (ch.bon) {
            bloque = true; b.classList.add("vrai"); son("bien"); gagneEtoile(tour);
            parle(hasard(["Bravo !", "Super !", "Génial !", "Bien joué !", "Oui, c'est ça !"]), false);
            tour++; plusTard(suivant, 1300);
          } else { b.classList.remove("faux"); void b.offsetWidth; b.classList.add("faux"); son("faux"); parle("Essaie encore !", false); }
        });
        zone.appendChild(b);
      });
      plateau.appendChild(zone);
      parle(q.texte);
    };
    suivant();
  }

  /* ---------- dessins à colorier ---------- */
  const T = 'stroke="#3b2a1a" stroke-width="5" stroke-linejoin="round" fill="#fff" data-z';
  const DESSINS = [
    { nom: "Le jardin", ico: "🌼", svg: `
      <rect ${T} x="4" y="4" width="392" height="392" rx="22"/>
      <path ${T} d="M4 300 Q120 250 220 290 T396 270 V374 Q396 396 374 396 H26 Q4 396 4 374Z"/>
      <circle ${T} cx="335" cy="70" r="38"/>
      <path ${T} d="M70 90 Q70 60 100 62 Q112 40 140 48 Q165 40 172 66 Q198 70 192 92 Z"/>
      <path ${T} d="M125 300 Q120 230 130 190"/>
      <path ${T} d="M128 260 Q90 240 80 210 Q115 212 128 248Z"/>
      <path ${T} d="M130 235 Q165 215 178 190 Q142 192 130 226Z"/>
      <circle ${T} cx="130" cy="120" r="30"/><circle ${T} cx="168" cy="150" r="30"/><circle ${T} cx="152" cy="196" r="30"/>
      <circle ${T} cx="108" cy="196" r="30"/><circle ${T} cx="92" cy="150" r="30"/>
      <circle ${T} cx="130" cy="160" r="26"/>
      <path ${T} d="M240 300 V200 L290 160 L340 200 V300Z"/>
      <path ${T} d="M228 206 L290 150 L352 206 L340 214 L290 172 L240 214Z"/>
      <rect ${T} x="276" y="248" width="30" height="52" rx="4"/>
      <rect ${T} x="252" y="214" width="24" height="24" rx="3"/><rect ${T} x="306" y="214" width="24" height="24" rx="3"/>
      <ellipse ${T} cx="66" cy="340" rx="16" ry="12"/><ellipse ${T} cx="200" cy="355" rx="18" ry="12"/><ellipse ${T} cx="330" cy="345" rx="16" ry="11"/>` },
    { nom: "Le papillon", ico: "🦋", svg: `
      <rect ${T} x="4" y="4" width="392" height="392" rx="22"/>
      <path ${T} d="M4 340 Q200 300 396 340 V374 Q396 396 374 396 H26 Q4 396 4 374Z"/>
      <path ${T} d="M196 190 C150 90 60 60 50 130 C42 185 120 210 196 205Z"/>
      <path ${T} d="M204 190 C250 90 340 60 350 130 C358 185 280 210 204 205Z"/>
      <path ${T} d="M196 212 C140 215 80 260 110 305 C140 340 185 285 196 228Z"/>
      <path ${T} d="M204 212 C260 215 320 260 290 305 C260 340 215 285 204 228Z"/>
      <circle ${T} cx="112" cy="140" r="20"/><circle ${T} cx="288" cy="140" r="20"/>
      <circle ${T} cx="132" cy="282" r="15"/><circle ${T} cx="268" cy="282" r="15"/>
      <ellipse ${T} cx="200" cy="215" rx="14" ry="70"/>
      <circle ${T} cx="200" cy="135" r="20"/>
      <path d="M193 118 Q182 86 162 78 M207 118 Q218 86 238 78" stroke="#3b2a1a" stroke-width="5" fill="none" stroke-linecap="round"/>` },
    { nom: "L'arc-en-ciel", ico: "🌈", svg: `
      <rect ${T} x="4" y="4" width="392" height="392" rx="22"/>
      <path ${T} d="M4 318 H396 V374 Q396 396 374 396 H26 Q4 396 4 374Z"/>
      <circle ${T} cx="340" cy="62" r="32"/>
      <path ${T} d="M30 300 A170 170 0 0 1 370 300 L345 300 A145 145 0 0 0 55 300Z"/>
      <path ${T} d="M55 300 A145 145 0 0 1 345 300 L320 300 A120 120 0 0 0 80 300Z"/>
      <path ${T} d="M80 300 A120 120 0 0 1 320 300 L295 300 A95 95 0 0 0 105 300Z"/>
      <path ${T} d="M105 300 A95 95 0 0 1 295 300 L270 300 A70 70 0 0 0 130 300Z"/>
      <path ${T} d="M130 300 A70 70 0 0 1 270 300Z"/>
      <path ${T} d="M16 318 Q12 284 46 284 Q56 258 84 268 Q112 258 118 288 Q142 292 136 318Z"/>
      <path ${T} d="M384 318 Q388 284 354 284 Q344 258 316 268 Q288 258 282 288 Q258 292 264 318Z"/>` }
  ];
  let dessinActuel = 0;
  const COULEURS = [["rouge", "#ef233c"], ["orange", "#ff8a00"], ["jaune", "#ffd000"], ["vert", "#22c55e"], ["vert d'eau", "#57d6a4"], ["bleu ciel", "#6cc8ff"],
    ["bleu", "#1e6bff"], ["violet", "#8b3dff"], ["rose", "#ff6fb5"], ["marron", "#8b5a2b"], ["noir", "#3b2a1a"], ["blanc", "#ffffff"]];

  /* ---------- les jeux ---------- */
  const JEUX = {
    lucioles: { titre: "Attrape les lucioles", lancer() {
      preparerEtoiles(10);
      let n = 0; const but = 10;
      bullePico("Touche les lumières !");
      const pot = document.createElement("div"); pot.className = "pot"; pot.textContent = "0 / 10 ✨"; plateau.appendChild(pot);
      parle("Touche les lumières qui volent, et compte avec moi !");
      const apparait = () => {
        if (n >= but) return;
        const b = document.createElement("button"); b.className = "luciole-btn"; b.type = "button"; b.setAttribute("aria-label", "Lumière");
        const r = plateau.getBoundingClientRect();
        const place = () => { b.style.left = 10 + Math.random() * Math.max(10, r.width - 104) + "px"; b.style.top = 120 + Math.random() * Math.max(40, r.height - 280) + "px"; };
        place(); b.style.transition = "left 1.6s ease-in-out, top 1.6s ease-in-out";
        plateau.appendChild(b);
        const bouge = setInterval(place, 1600); intervalles.push(bouge);
        b.addEventListener("click", () => {
          clearInterval(bouge); b.classList.add("prise"); gagneEtoile(n); n++; son("ding");
          pot.textContent = `${n} / 10 ✨`; parle(MOTS[n], false); setTimeout(() => b.remove(), 400);
          if (n >= but) { plateau.querySelectorAll(".luciole-btn").forEach(x => x.remove()); victoire("Bravo ! Tu as attrapé dix lumières !"); }
        });
        plusTard(() => { clearInterval(bouge); if (!b.classList.contains("prise")) b.remove(); }, 6500);
        plusTard(apparait, 900 + Math.random() * 700);
      };
      apparait(); plusTard(apparait, 500);
    }},

    memo: { titre: "Memory", lancer() {
      const symboles = melange(["🌸", "🍓", "🐞", "🌈", "⭐", "🍄", "🦋", "🌻"]).slice(0, 6);
      const cartes = melange([...symboles, ...symboles]);
      preparerEtoiles(6);
      bullePico("Retrouve les paires !");
      parle("Retourne deux cartes et retrouve les paires !");
      const g = document.createElement("div"); g.className = "grille-memo";
      let ouvertes = [], trouvees = 0, bloque = false;
      cartes.forEach((s, i) => {
        const c = document.createElement("button"); c.className = "memo"; c.type = "button"; c.dataset.s = s; c.setAttribute("aria-label", "Carte " + (i + 1));
        c.innerHTML = `<div class="memo-in"><div class="memo-d"><img src="${PICO}" alt="" width="160" height="208"></div><div class="memo-f" aria-hidden="true">${s}</div></div>`;
        c.addEventListener("click", () => {
          if (bloque || c.classList.contains("retournee") || c.classList.contains("trouvee")) return;
          c.classList.add("retournee"); c.setAttribute("aria-label", "Carte " + (i + 1) + " : " + s); son("clic"); ouvertes.push(c);
          if (ouvertes.length === 2) {
            bloque = true;
            const [a, b] = ouvertes;
            if (a.dataset.s === b.dataset.s) {
              plusTard(() => { a.classList.add("trouvee"); b.classList.add("trouvee"); son("bien"); gagneEtoile(trouvees); trouvees++;
                parle(hasard(["Bravo !", "Une paire !", "Super !"]), false); ouvertes = []; bloque = false;
                if (trouvees === 6) victoire("Bravo ! Tu as trouvé toutes les paires !"); }, 450);
            } else plusTard(() => {
              [a, b].forEach(x => { x.classList.remove("retournee"); x.setAttribute("aria-label", "Carte " + (1 + [...g.children].indexOf(x))); });
              ouvertes = []; bloque = false;
            }, 1000);
          }
        });
        g.appendChild(c);
      });
      plateau.appendChild(g);
    }},

    compter: { titre: "Combien ?", lancer() {
      const objets = [["🍎", "pommes"], ["🌸", "fleurs"], ["⭐", "étoiles"], ["🐞", "coccinelles"], ["🍓", "fraises"], ["🦋", "papillons"], ["🍄", "champignons"]];
      let dernier = 0;
      quiz({ tours: 8, question(tour) {
        /* difficulté progressive : jusqu'à 5, puis 7, puis 10 */
        const [min, max] = tour < 3 ? [1, 5] : tour < 6 ? [2, 7] : [3, 10];
        let n; do { n = min + Math.floor(Math.random() * (max - min + 1)); } while (n === dernier); dernier = n;
        const [emo, nom] = hasard(objets);
        const av = document.createElement("div"); av.className = "objets"; av.setAttribute("role", "img"); av.setAttribute("aria-label", `${n} ${nom}`);
        av.innerHTML = Array.from({ length: n }, (_, i) => `<span style="animation-delay:${i * 60}ms" aria-hidden="true">${emo}</span>`).join("");
        const opts = new Set([n]); while (opts.size < 3) { const o = n + hasard([-2, -1, 1, 2, 3]); if (o >= 1 && o <= 10) opts.add(o); }
        return { texte: `Combien de ${nom} ?`, avant: av,
          choix: melange([...opts]).map(o => { const b = document.createElement("button"); b.className = "gros-bouton"; b.textContent = o; b.setAttribute("aria-label", MOTS[o]); return { el: b, bon: o === n }; }) };
      }});
    }},

    couleurs: { titre: "Les couleurs", lancer() {
      const C = [["rouge", "#ef233c"], ["bleu", "#1e6bff"], ["jaune", "#ffd000"], ["vert", "#22c55e"], ["orange", "#ff8a00"], ["violet", "#8b3dff"], ["rose", "#ff6fb5"], ["marron", "#8b5a2b"]];
      let dernier = "";
      quiz({ tours: 8, question() {
        const choix = melange(C).slice(0, 4); let cible; do { cible = hasard(choix); } while (cible[0] === dernier); dernier = cible[0];
        return { texte: `Touche le ${cible[0]} !`, classe: "pastilles",
          choix: choix.map(([nom, coul]) => { const b = document.createElement("button"); b.className = "blob"; b.style.background = coul; b.setAttribute("aria-label", nom); return { el: b, bon: nom === cible[0] }; }) };
      }});
    }},

    formes: { titre: "Les formes", lancer() {
      const F = {
        "le cercle": '<circle cx="50" cy="50" r="42" fill="#ff5c9a"/>',
        "le carré": '<rect x="10" y="10" width="80" height="80" rx="6" fill="#1e6bff"/>',
        "le triangle": '<polygon points="50,6 94,90 6,90" fill="#22c55e"/>',
        "l'étoile": '<polygon points="50,4 62,36 96,38 69,59 79,93 50,74 21,93 31,59 4,38 38,36" fill="#ffc400"/>',
        "le cœur": '<path d="M50 90 C10 62 4 38 18 22 C30 9 46 14 50 28 C54 14 70 9 82 22 C96 38 90 62 50 90Z" fill="#ef233c"/>',
        "le rectangle": '<rect x="4" y="24" width="92" height="52" rx="6" fill="#8b3dff"/>',
        "le losange": '<polygon points="50,4 94,50 50,96 6,50" fill="#ff8a00"/>'
      };
      const noms = Object.keys(F); let dernier = "";
      quiz({ tours: 8, question() {
        const choix = melange(noms).slice(0, 4); let cible; do { cible = hasard(choix); } while (cible === dernier); dernier = cible;
        return { texte: `Trouve ${cible} !`, classe: "pastilles",
          choix: choix.map(n => { const b = document.createElement("button"); b.className = "forme"; b.setAttribute("aria-label", n);
            b.innerHTML = `<svg viewBox="0 0 100 100" aria-hidden="true">${F[n]}</svg>`; return { el: b, bon: n === cible }; }) };
      }});
    }},

    coloriage: { titre: "Coloriage", lancer() {
      preparerEtoiles(0);
      const d = DESSINS[dessinActuel];
      bullePico("Choisis une couleur, puis touche le dessin !");
      parle("Choisis une couleur, puis touche le dessin pour le colorier !");
      const at = document.createElement("div"); at.className = "atelier";
      at.innerHTML = `<div class="dessin"><svg viewBox="0 0 400 400" role="group" aria-label="Dessin à colorier : ${d.nom}">${d.svg}</svg></div>`;
      const outils = document.createElement("div"); outils.className = "outils";
      const pal = document.createElement("div"); pal.className = "palette"; pal.setAttribute("role", "group"); pal.setAttribute("aria-label", "Couleurs");
      let courant = COULEURS[0][1];
      COULEURS.forEach(([nom, c], i) => {
        const b = document.createElement("button"); b.type = "button"; b.style.background = c; b.setAttribute("aria-label", nom); b.setAttribute("aria-pressed", i ? "false" : "true");
        b.addEventListener("click", () => { pal.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); courant = c; son("clic"); parle(nom, false); });
        pal.appendChild(b);
      });
      const choixD = document.createElement("div"); choixD.className = "dessins-choix";
      DESSINS.forEach((x, i) => {
        if (i === dessinActuel) return;
        const b = document.createElement("button"); b.type = "button"; b.className = "btn btn-blanc btn-petit"; b.textContent = `${x.ico} ${x.nom}`;
        b.addEventListener("click", () => { dessinActuel = i; ouvrir("coloriage", true); });
        choixD.appendChild(b);
      });
      const fini = document.createElement("button"); fini.type = "button"; fini.className = "btn btn-miel"; fini.textContent = "✨ J'ai fini !"; fini.disabled = true; fini.style.opacity = ".5";
      fini.addEventListener("click", () => { if (!at.dataset.fini) { at.dataset.fini = 1; dessinActuel = (dessinActuel + 1) % DESSINS.length; victoire("Bravo ! Quel joli dessin !"); } });
      outils.append(pal, fini, choixD); at.appendChild(outils); plateau.appendChild(at);
      const zones = at.querySelectorAll("[data-z]"); const colorie = new Set();
      zones.forEach((z, i) => {
        z.setAttribute("tabindex", "0"); z.setAttribute("role", "button"); z.setAttribute("aria-label", "Zone " + (i + 1));
        const peindre = () => {
          z.setAttribute("fill", courant); son("ding"); colorie.add(i);
          if (colorie.size >= 3) { fini.disabled = false; fini.style.opacity = ""; }
          if (colorie.size === zones.length && !at.dataset.fini) { at.dataset.fini = 1; dessinActuel = (dessinActuel + 1) % DESSINS.length; victoire("Bravo ! Quel joli dessin !"); }
        };
        z.addEventListener("click", peindre);
        z.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); peindre(); } });
      });
    }}
  };

  /* lien direct vers un jeu : /jeux/#jeu-couleurs */
  const m = location.hash.match(/^#jeu-(\w+)$/);
  if (m && JEUX[m[1]]) { history.replaceState(null, "", location.pathname + location.search); ouvrir(m[1]); }
})();
