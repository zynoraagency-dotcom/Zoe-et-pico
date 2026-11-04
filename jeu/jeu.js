(() => {
  const MOTS = ["zéro","un","deux","trois","quatre","cinq","six","sept","huit","neuf","dix"];
  const NOMS = { fleur: ["fleur","fleurs"], tulipe: ["tulipe","tulipes"], champi: ["champignon","champignons"], etoile: ["étoile","étoiles"], pomme: ["pomme","pommes"] };
  const TOURS = 10;
  const $ = (id) => document.getElementById(id);
  const champ = $("champ"), reponses = $("reponses"), bulle = $("bulle"), pico = $("pico"), lanternes = $("lanternes");

  let etat = { tour: 0, premiersEssais: 0, enCours: false };
  let manche = null;

  // ---------- dessins ----------
  const SVG = {
    fleur: (c) => `<svg viewBox="0 0 100 100"><g transform="translate(50 50)">${[0,45,90,135,180,225,270,315].map(a=>`<ellipse rx="13" ry="24" transform="rotate(${a}) translate(0 -22)" fill="#fff" stroke="#e6d9c2" stroke-width="2"/>`).join("")}<circle r="15" fill="${c}"/><circle r="15" fill="none" stroke="#d99a12" stroke-width="2"/></g></svg>`,
    tulipe: (c) => `<svg viewBox="0 0 100 100"><path d="M50 58 C48 72 50 84 50 96" stroke="#3f9a35" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M50 84 C38 78 30 70 30 62 C40 66 46 72 50 80Z" fill="#5cb84a"/><path d="M26 22 L38 34 L50 14 L62 34 L74 22 L72 48 C70 60 60 66 50 66 C40 66 30 60 28 48Z" fill="${c}" stroke="rgba(0,0,0,.15)" stroke-width="2"/></svg>`,
    champi: () => `<svg viewBox="0 0 100 100"><path d="M38 56 L36 88 C36 92 64 92 64 88 L62 56Z" fill="#fff4e0" stroke="#e2cfae" stroke-width="2"/><path d="M8 58 C8 26 30 10 50 10 C70 10 92 26 92 58 C70 64 30 64 8 58Z" fill="#e8413c" stroke="#b92d29" stroke-width="2"/><circle cx="32" cy="34" r="7" fill="#fff"/><circle cx="56" cy="24" r="6" fill="#fff"/><circle cx="72" cy="42" r="7" fill="#fff"/><circle cx="46" cy="48" r="5" fill="#fff"/></svg>`,
    etoile: () => `<svg viewBox="0 0 100 100"><path d="M50 6 L62 36 L94 38 L69 58 L78 90 L50 72 L22 90 L31 58 L6 38 L38 36Z" fill="#ffd23d" stroke="#e0a400" stroke-width="3" stroke-linejoin="round"/><circle cx="41" cy="48" r="4" fill="#3b2a1a"/><circle cx="59" cy="48" r="4" fill="#3b2a1a"/><path d="M42 59 Q50 66 58 59" stroke="#3b2a1a" stroke-width="3" fill="none" stroke-linecap="round"/></svg>`,
    pomme: () => `<svg viewBox="0 0 100 100"><path d="M50 30 C40 18 14 22 14 50 C14 76 34 94 50 86 C66 94 86 76 86 50 C86 22 60 18 50 30Z" fill="#e8413c" stroke="#b92d29" stroke-width="2"/><path d="M50 30 C50 22 52 14 56 8" stroke="#6b4426" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M56 16 C66 8 76 12 78 16 C70 22 62 22 56 16Z" fill="#5cb84a"/><ellipse cx="34" cy="44" rx="6" ry="10" fill="rgba(255,255,255,.45)"/></svg>`
  };
  const COEURS = ["#ffc83d","#ff9f1c","#ff6fa8"];
  const TULIPES = ["#ff6fa8","#ff8a3d","#b57bff","#ff4d6d"];

  // ---------- sons ----------
  let ctx = null;
  function son(freqs, dur = .12, type = "sine", vol = .18) {
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      let t = ctx.currentTime;
      freqs.forEach((f) => {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type = type; o.frequency.value = f;
        g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(.001, t + dur);
        o.connect(g).connect(ctx.destination); o.start(t); o.stop(t + dur);
        t += dur * .8;
      });
    } catch (e) {}
  }
  const pop = () => son([660, 990], .08, "triangle");
  const youpi = () => son([523, 659, 784, 1047], .14, "triangle", .2);
  const oups = () => son([330, 262], .16, "sine", .15);

  let voixFr = null;
  function chercheVoix() {
    try { const v = speechSynthesis.getVoices().filter(v => v.lang && v.lang.startsWith("fr")); voixFr = v.find(x => x.localService) || v[0] || null; } catch (e) {}
  }
  try { chercheVoix(); speechSynthesis.onvoiceschanged = chercheVoix; } catch (e) {}
  function dire(texte) {
    try {
      speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(texte);
      u.lang = "fr-FR"; u.rate = .9; u.pitch = 1.25;
      if (voixFr) u.voice = voixFr;
      speechSynthesis.speak(u);
    } catch (e) {}
  }

  // ---------- jeu ----------
  function hasard(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function melange(t) { for (let i = t.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [t[i], t[j]] = [t[j], t[i]]; } return t; }

  function dessineLanternes() {
    lanternes.innerHTML = "";
    for (let i = 0; i < TOURS; i++) {
      const s = document.createElement("span");
      s.className = "lanterne" + (i < etat.tour ? " on" : "");
      lanternes.appendChild(s);
    }
    lanternes.setAttribute("aria-label", `${etat.tour} lumières allumées sur ${TOURS}`);
  }

  function nouvelleManche() {
    const max = etat.tour < 4 ? 5 : 10;
    const min = etat.tour < 4 ? 1 : 3;
    const n = hasard(min, max);
    const sorte = melange(Object.keys(SVG))[0];
    manche = { n, sorte, comptes: 0, essais: 0, fini: false };
    // positions sans chevauchement : une grille 4 x 3, cases tirées au sort
    const cases = melange([...Array(12).keys()]).slice(0, n);
    const debout = champ.clientHeight > champ.clientWidth;
    const cols = debout ? 3 : 4, ligs = 12 / cols;
    champ.innerHTML = "";
    cases.forEach((c, i) => {
      const col = c % cols, lig = Math.floor(c / cols);
      const x = (col + .5) * 100 / cols + hasard(-4, 4);
      const y = (lig + .5) * 100 / ligs + hasard(-3, 3);
      const b = document.createElement("button");
      b.className = "objet"; b.type = "button";
      b.style.width = debout ? "27%" : "19%";
      b.style.left = x + "%"; b.style.top = y + "%";
      b.style.animationDelay = (i * 60) + "ms";
      const couleur = sorte === "fleur" ? COEURS[i % 3] : TULIPES[i % TULIPES.length];
      b.innerHTML = SVG[sorte](couleur);
      b.setAttribute("aria-label", NOMS[sorte][0]);
      b.addEventListener("click", () => compte(b));
      champ.appendChild(b);
    });
    // trois choix
    const choix = new Set([n]);
    while (choix.size < 3) {
      const d = n + hasard(-3, 3);
      if (d >= 1 && d <= 10) choix.add(d);
    }
    reponses.innerHTML = "";
    melange([...choix]).forEach((v) => {
      const b = document.createElement("button");
      b.className = "choix"; b.type = "button"; b.textContent = v;
      b.setAttribute("aria-label", MOTS[v]);
      b.addEventListener("click", () => repond(b, v));
      reponses.appendChild(b);
    });
    const nom = NOMS[sorte][1];
    parle(`Combien de ${nom} ? Touche-les pour compter !`, `Combien de ${nom} ?`);
    sauve();
  }

  function parle(texte, aVoix) { bulle.textContent = texte; dire(aVoix || texte); }

  function compte(b) {
    if (!manche || b.dataset.compte) return;
    manche.comptes++;
    b.dataset.compte = manche.comptes;
    const bad = document.createElement("span");
    bad.className = "badge"; bad.textContent = manche.comptes;
    b.appendChild(bad);
    pop(); dire(MOTS[manche.comptes]);
    if (manche.comptes === manche.n) bulle.textContent = `Tu as compté jusqu'à ${manche.n} ! Choisis le bon nombre.`;
  }

  function repond(b, v) {
    if (!manche || manche.fini) return;
    manche.essais++;
    if (v === manche.n) {
      manche.fini = true;
      if (manche.essais === 1) etat.premiersEssais++;
      b.classList.add("juste");
      etat.tour++;
      dessineLanternes();
      youpi(); etincelles(b);
      pico.classList.remove("saute"); void pico.offsetWidth; pico.classList.add("saute");
      const bravo = ["Bravo !", "Super !", "Génial !", "Youpi !", "Trop fort !"][hasard(0, 4)];
      const nom = NOMS[manche.sorte][manche.n > 1 ? 1 : 0];
      parle(`${bravo} Il y a ${manche.n} ${nom} !`, `${bravo} ${MOTS[manche.n]} ${nom} !`);
      sauve();
      setTimeout(() => etat.tour >= TOURS ? finir() : nouvelleManche(), 2200);
    } else {
      b.classList.add("faux");
      oups();
      pico.classList.remove("oups"); void pico.offsetWidth; pico.classList.add("oups");
      parle("Oups ! Touche chaque objet pour compter avec moi.", "Oups ! Compte avec moi.");
    }
  }

  function etincelles(source) {
    const r = source.getBoundingClientRect(), base = document.querySelector(".cadre").getBoundingClientRect();
    for (let i = 0; i < 14; i++) {
      const s = document.createElement("span");
      s.className = "etincelle";
      s.style.left = (r.left - base.left + r.width / 2) + "px";
      s.style.top = (r.top - base.top + r.height / 2) + "px";
      const a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 90;
      s.style.setProperty("--dx", Math.cos(a) * d + "px");
      s.style.setProperty("--dy", Math.sin(a) * d - 40 + "px");
      document.querySelector(".cadre").appendChild(s);
      setTimeout(() => s.remove(), 950);
    }
  }

  function finir() {
    $("bilan").textContent = `Tu as allumé les ${TOURS} lumières de Pico, dont ${etat.premiersEssais} du premier coup !`;
    $("fin").hidden = false;
    parle("Bravo ! Tu sais compter comme un champion !", "Bravo ! Tu as allumé toutes les lumières !");
    etat.enCours = false; sauve();
  }

  function demarrer() {
    etat = { tour: 0, premiersEssais: 0, enCours: true };
    $("debut").hidden = true; $("fin").hidden = true;
    dessineLanternes(); youpi(); nouvelleManche();
  }

  function sauve() {}

  $("jouer").addEventListener("click", demarrer);
  $("rejouer").addEventListener("click", demarrer);

  function start(data) {
    if (data && data.enCours && data.tour < TOURS) {
      etat = { tour: data.tour, premiersEssais: data.premiersEssais || 0, enCours: true };
      $("debut").hidden = true; dessineLanternes(); nouvelleManche();
    } else {
      dessineLanternes();
      // aperçu au repos : une manche d'exemple derrière l'écran d'accueil
      manche = null; const n = 4;
      champ.innerHTML = [[20,30],[45,62],[70,28],[82,70]].map(([x,y],i)=>`<span class="objet" style="left:${x}%;top:${y}%;animation:none">${SVG.fleur(COEURS[i%3])}</span>`).join("");
      reponses.innerHTML = [3,4,5].map(v=>`<button class="choix" type="button" tabindex="-1">${v}</button>`).join("");
    }
  }
  start({});
})();
