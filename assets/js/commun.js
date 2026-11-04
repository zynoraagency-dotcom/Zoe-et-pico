/* =========================================================
   Zoé et Pico — script commun à toutes les pages
   - lumières de luciole, barre du haut, apparition au défilement
   - voix de Pico et petits sons
   - porte parents : tout lien vers un autre site (Amazon, YouTube…)
     demande d'abord une petite question pour les adultes
   - vidéos YouTube chargées seulement quand on appuie dessus
   ========================================================= */
"use strict";
window.ZP = window.ZP || {};

const calme = matchMedia("(prefers-reduced-motion: reduce)").matches;
ZP.calme = calme;

/* ---------- lumières de luciole ---------- */
(() => {
  const box = document.createElement("div");
  box.className = "lucioles"; box.setAttribute("aria-hidden", "true");
  document.body.prepend(box);
  if (calme) return;
  const n = innerWidth < 700 ? 10 : 18;
  for (let i = 0; i < n; i++) {
    const l = document.createElement("i");
    l.style.left = Math.random() * 100 + "%"; l.style.top = Math.random() * 100 + "%";
    l.style.setProperty("--x", Math.random() * 90 - 45 + "px"); l.style.setProperty("--y", Math.random() * 90 - 45 + "px");
    l.style.setProperty("--d", 6 + Math.random() * 6 + "s"); l.style.setProperty("--r", -Math.random() * 10 + "s");
    box.appendChild(l);
  }
})();

/* ---------- barre du haut plus visible quand on descend ---------- */
(() => {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  const maj = () => nav.classList.toggle("defile", scrollY > 40);
  addEventListener("scroll", maj, { passive: true }); maj();
})();

/* ---------- apparition au défilement ---------- */
(() => {
  const els = document.querySelectorAll(".rev");
  if (!("IntersectionObserver" in window)) { els.forEach(e => e.classList.add("vu")); return; }
  const obs = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("vu"); obs.unobserve(e.target); }
  }), { threshold: .08, rootMargin: "0px 0px -20px 0px" });
  els.forEach((el, i) => { el.style.transitionDelay = (i % 3) * 90 + "ms"; obs.observe(el); });
})();

/* ---------- voix et sons ---------- */
let voixFr = null;
const chargerVoix = () => {
  const v = speechSynthesis.getVoices().filter(v => v.lang && v.lang.startsWith("fr"));
  /* on préfère une voix installée sur l'appareil : le texte n'est alors envoyé à aucun service en ligne */
  const locales = v.filter(x => x.localService);
  voixFr = locales.find(x => /Amélie|Audrey|Marie|Denise|Julie|Aurélie|Google/i.test(x.name)) || locales[0] || v[0] || null;
};
if ("speechSynthesis" in window) { chargerVoix(); speechSynthesis.onvoiceschanged = chargerVoix; }
ZP.derniereParole = "";
ZP.parle = (t, garder = true) => {
  if (garder) ZP.derniereParole = t;
  if (!("speechSynthesis" in window)) return;
  try {
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(t);
    u.lang = "fr-FR"; u.rate = .95; u.pitch = 1.25; if (voixFr) u.voice = voixFr;
    speechSynthesis.speak(u);
  } catch (e) {}
};
ZP.tais = () => { try { speechSynthesis.cancel(); } catch (e) {} };
let ac;
ZP.son = type => {
  try {
    ac = ac || new (window.AudioContext || window.webkitAudioContext)();
    if (ac.state === "suspended") ac.resume();
    const notes = { bien: [660, 880, 1320], faux: [300, 220], clic: [900], ding: [1200, 1600], fin: [523, 659, 784, 1047] }[type];
    notes.forEach((f, i) => {
      const o = ac.createOscillator(), g = ac.createGain(), t = ac.currentTime + i * .1;
      o.type = type === "faux" ? "triangle" : "sine"; o.frequency.value = f;
      g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(.25, t + .02); g.gain.exponentialRampToValueAtTime(.0001, t + .25);
      o.connect(g).connect(ac.destination); o.start(t); o.stop(t + .3);
    });
  } catch (e) {}
};
/* les effets s'affichent dans la fenêtre ouverte (jeu) si elle existe, sinon dans la page */
ZP.couche = () => document.querySelector("dialog[open]") || document.body;
ZP.confettis = () => {
  if (calme) return;
  const cs = ["#ffc83d", "#ff5c9a", "#57d6a4", "#6cc8ff", "#b49cff", "#ff8a65"], ou = ZP.couche();
  for (let i = 0; i < 70; i++) {
    const c = document.createElement("i"); c.className = "confetti";
    c.style.left = Math.random() * 100 + "vw"; c.style.background = cs[i % cs.length];
    c.style.animationDuration = 1.8 + Math.random() * 1.8 + "s"; c.style.animationDelay = Math.random() * .5 + "s";
    c.style.borderRadius = Math.random() > .5 ? "50%" : "3px";
    ou.appendChild(c); setTimeout(() => c.remove(), 4500);
  }
};
ZP.hasard = a => a[Math.floor(Math.random() * a.length)];
ZP.melange = a => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

/* ---------- porte parents ---------- */
(() => {
  const NOMBRES = { 23: "vingt-trois", 27: "vingt-sept", 34: "trente-quatre", 41: "quarante et un", 48: "quarante-huit", 56: "cinquante-six", 62: "soixante-deux", 75: "soixante-quinze", 83: "quatre-vingt-trois", 96: "quatre-vingt-seize" };
  const porte = document.createElement("dialog");
  porte.className = "porte"; porte.setAttribute("aria-labelledby", "porte-titre");
  porte.innerHTML = `<h2 class="disp" id="porte-titre">🔒 Demande à un adulte</h2><p id="porte-texte"></p><div class="porte-choix" id="porte-choix"></div><small id="porte-note"></small><button class="annuler" type="button">Annuler</button>`;
  document.body.appendChild(porte);
  const texte = porte.querySelector("#porte-texte"), choix = porte.querySelector("#porte-choix"), note = porte.querySelector("#porte-note");
  porte.querySelector(".annuler").addEventListener("click", () => porte.close());
  porte.addEventListener("click", e => { if (e.target === porte) porte.close(); });

  const nomSite = url => /amazon|amzn/.test(url) ? "Amazon" : /youtu/.test(url) ? "YouTube" : new URL(url).hostname.replace(/^www\./, "");
  function demander(url) {
    const cles = Object.keys(NOMBRES).map(Number), bon = ZP.hasard(cles);
    texte.innerHTML = 'Pour quitter le site, touche le nombre&nbsp;:<br><span class="nombre"></span>';
    texte.querySelector(".nombre").textContent = NOMBRES[bon];
    note.textContent = `Ce lien ouvre ${nomSite(url)} dans un nouvel onglet.`;
    choix.innerHTML = "";
    ZP.melange([bon, ...ZP.melange(cles.filter(k => k !== bon)).slice(0, 3)]).forEach(n => {
      const b = document.createElement("button"); b.type = "button"; b.textContent = n;
      b.addEventListener("click", () => {
        if (n !== bon) { porte.close(); return; }
        /* bonne réponse : un vrai lien que l'adulte touche (marche sur tous les téléphones) */
        texte.textContent = "C'est bon ! Touchez le bouton pour ouvrir :";
        choix.innerHTML = "";
        const a = document.createElement("a");
        a.className = "btn " + (/youtu/.test(url) ? "btn-yt" : "btn-amazon");
        a.href = url; a.target = "_blank"; a.rel = "noopener";
        a.textContent = "Ouvrir " + nomSite(url) + " ↗";
        a.addEventListener("click", () => setTimeout(() => porte.close(), 300));
        choix.appendChild(a); a.focus();
      });
      choix.appendChild(b);
    });
    porte.showModal();
  }
  ZP.demanderAdulte = demander;

  /* tous les liens vers un autre site passent par la porte parents */
  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button !== 0) return;
    const a = e.target.closest("a[href]");
    if (!a || porte.contains(a)) return;
    let u; try { u = new URL(a.href, location.href); } catch (_) { return; }
    if (!/^https?:$/.test(u.protocol) || u.host === location.host) return;
    e.preventDefault();
    demander(u.href);
  });
})();

/* ---------- vidéos : l'image s'affiche, YouTube ne se charge qu'au clic ---------- */
document.querySelectorAll("button.video[data-yt]").forEach(b => {
  b.addEventListener("click", () => {
    const f = document.createElement("iframe");
    f.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(b.dataset.yt)}?autoplay=1&rel=0&playsinline=1`;
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen"; f.allowFullscreen = true;
    f.title = b.dataset.titre || "Vidéo de Zoé et Pico";
    const boite = document.createElement("div"); boite.className = "video";
    boite.appendChild(f); b.replaceWith(boite); f.focus();
  }, { once: true });
});

/* ---------- année du pied de page ---------- */
document.querySelectorAll("[data-annee]").forEach(e => e.textContent = new Date().getFullYear());
