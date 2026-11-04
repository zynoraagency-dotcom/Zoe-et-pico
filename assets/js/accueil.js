/* =========================================================
   Zoé et Pico — page d'accueil
   - la vidéo de bannière se charge APRÈS le reste de la page (chargement plus rapide)
   - si elle ne peut pas démarrer (mode économie d'énergie sur iPhone),
     on la remplace par la même animation en image animée
   - sans vidéo (connexion lente, animations réduites) : Zoé et Pico animés en image
   ========================================================= */
"use strict";
(() => {
  /* vidéo plus légère (480p, 400 Ko) sur téléphone et tablette, 720p sur ordinateur */
  const BANNIERE = matchMedia("(min-width: 900px)").matches ? "/img/banniere.mp4" : "/img/banniere-mobile.mp4";
  const BANNIERE_ANIMEE = "/img/banniere.webp";
  const scene = document.getElementById("accueil");
  const v = document.getElementById("fond-video");
  const economie = navigator.connection && (navigator.connection.saveData || /2g/.test(navigator.connection.effectiveType || ""));

  if (v && BANNIERE && !ZP.calme && !economie) {
    scene.classList.add("avec-video");
    const lancer = () => {
      v.muted = true; v.src = BANNIERE;
      let remplacee = false;
      const animation = () => {
        if (remplacee || !v.paused) return; remplacee = true;
        const im = document.createElement("img");
        im.className = "fond-video"; im.alt = ""; im.src = BANNIERE_ANIMEE; im.decoding = "async";
        v.replaceWith(im);
      };
      const p = v.play(); if (p) p.catch(animation);
      setTimeout(animation, 3500);
    };
    if (document.readyState === "complete") lancer(); else addEventListener("load", lancer, { once: true });
  }

  /* générique : Pico traverse l'écran avec sa traînée dorée, Zoé arrive en sautant */
  const pico = document.getElementById("pico"), zoe = document.getElementById("zoe"), titre = document.getElementById("titre");
  if (!pico || !zoe) return;
  function etincelle(x, y, fort) {
    const e = document.createElement("i");
    e.className = "etinc" + (Math.random() < .35 ? " etoile" : "");
    const t = (fort ? 10 : 6) + Math.random() * (fort ? 16 : 12);
    e.style.cssText = `left:${x + (Math.random() - .5) * 20}px;top:${y + (Math.random() - .5) * 20}px;--t:${t}px;--dx:${(Math.random() - .5) * 60}px;--dy:${Math.random() * 50 + 10}px`;
    document.body.appendChild(e); setTimeout(() => e.remove(), 950);
  }
  function trainee(el, duree) {
    const t0 = performance.now();
    (function f(t) {
      if (t - t0 > duree) return;
      const r = el.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) etincelle(r.left + r.width * .45, r.top + r.height * .6);
      requestAnimationFrame(f);
    })(t0);
  }
  function eclat(el, n = 16) {
    const r = el.getBoundingClientRect();
    for (let i = 0; i < n; i++) etincelle(r.left + Math.random() * r.width, r.top + Math.random() * r.height, true);
  }
  /* les mots du titre éclatent en étincelles (avec ou sans vidéo) */
  if (!ZP.calme && titre) titre.querySelectorAll(".mot").forEach((m, i) => setTimeout(() => eclat(m, 5), 1300 + i * 110));
  if (ZP.calme || scene.classList.contains("avec-video")) return;

  pico.animate([
    { transform: "translate(-115vw,26vh) rotate(-18deg) scale(.7)" },
    { transform: "translate(-70vw,-12vh) rotate(14deg) scale(.85)", offset: .4 },
    { transform: "translate(-30vw,12vh) rotate(-10deg) scale(1)", offset: .72 },
    { transform: "translate(0,0) rotate(0) scale(1)" }
  ], { duration: 2100, easing: "ease-in-out", fill: "backwards" });
  trainee(pico, 2100);
  zoe.animate([
    { transform: "translateY(110%)" },
    { transform: "translateY(-10%) scaleY(1.06)", offset: .55 },
    { transform: "translateY(0) scale(1.06,.92)", offset: .78 },
    { transform: "none" }
  ], { duration: 950, delay: 1900, easing: "ease-out", fill: "backwards" });
  const coucou = () => zoe.animate([{ transform: "rotate(0)" }, { transform: "rotate(-5deg)" }, { transform: "rotate(5deg)" }, { transform: "rotate(-4deg)" }, { transform: "rotate(0)" }], { duration: 1000, easing: "ease-in-out" });
  setTimeout(coucou, 3000);
  const looping = () => {
    const pts = [], R = innerWidth < 700 ? .5 : 1;
    for (let k = 0; k <= 16; k++) { const a = k / 16 * Math.PI * 2; pts.push({ transform: `translate(${-Math.sin(a) * 70 * R}px,${(Math.cos(a) - 1) * 55 * R}px) rotate(${-k / 16 * 360}deg)` }); }
    pico.animate(pts, { duration: 1500, easing: "ease-in-out" }); trainee(pico, 1500);
  };
  const saut = () => zoe.animate([
    { transform: "none" }, { transform: "scale(1.06,.9)", offset: .15 }, { transform: "translateY(-16%) scale(.96,1.05)", offset: .45 },
    { transform: "translateY(0) scale(1.07,.9)", offset: .75 }, { transform: "none" }
  ], { duration: 800, easing: "ease-out" });
  let visible = true;
  new IntersectionObserver(e => visible = e[0].isIntersecting).observe(pico);
  let tour = 0;
  setInterval(() => { if (!visible || document.hidden) return; (tour++ % 2 ? saut : looping)(); }, 4500);
  pico.addEventListener("click", () => { looping(); eclat(pico, 20); ZP.parle("Bzzz ! Coucou ! Viens jouer avec moi !"); });
  zoe.addEventListener("click", () => { saut(); setTimeout(coucou, 800); ZP.parle("Coucou ! Moi, c'est Zoé !"); });
})();
