/* =========================================================
   Zoé et Pico — la vraie voix de Pico (enregistrements dans /assets/voix/)
   Fichier généré par outils/voix.py à partir de outils/voix.modele.js : ne pas modifier à la main.
   ZPVoix.dire(texte, secours) joue l'enregistrement de la phrase s'il existe et renvoie true ;
   sinon renvoie false (la synthèse vocale du navigateur prend le relais).
   ========================================================= */
"use strict";
window.ZPVoix = (() => {
  const TABLE = {"un": "un","deux": "deux","trois": "trois","quatre": "quatre","cinq": "cinq","six": "six","sept": "sept","huit": "huit","neuf": "neuf","dix": "dix","bravo": "bravo","super": "super","génial": "genial","bien joué": "bien-joue","oui c'est ça": "oui-cest-ca","une paire": "une-paire","youpi": "youpi","trop fort": "trop-fort","essaie encore": "essaie-encore","oups compte avec moi": "oups","bravo tu as gagné": "tu-as-gagne","combien de pommes": "combien-pommes","combien de fleurs": "combien-fleurs","combien d'étoiles": "combien-etoiles","combien de coccinelles": "combien-coccinelles","combien de fraises": "combien-fraises","combien de papillons": "combien-papillons","combien de champignons": "combien-champignons","combien de tulipes": "combien-tulipes","touche le rouge": "touche-rouge","touche le bleu": "touche-bleu","touche le jaune": "touche-jaune","touche le vert": "touche-vert","touche le orange": "touche-orange","touche le violet": "touche-violet","touche le rose": "touche-rose","touche le marron": "touche-marron","trouve le cercle": "trouve-cercle","trouve le carré": "trouve-carre","trouve le triangle": "trouve-triangle","trouve l'étoile": "trouve-etoile","trouve le cœur": "trouve-coeur","trouve le rectangle": "trouve-rectangle","trouve le losange": "trouve-losange","rouge": "rouge","orange": "orange","jaune": "jaune","vert": "vert","vert d'eau": "vert-deau","bleu ciel": "bleu-ciel","bleu": "bleu","violet": "violet","rose": "rose","rose pâle": "rose-pale","marron": "marron","beige": "beige","gris": "gris","noir": "noir","blanc": "blanc","touche les lumières qui volent et compte avec moi": "intro-lucioles","retourne deux cartes et retrouve les paires": "intro-memo","choisis une couleur puis touche le dessin pour le colorier": "intro-coloriage","bzzz compte avec moi": "compte-avec-moi","bravo tu as attrapé dix lumières": "gagne-lucioles","bravo tu as trouvé toutes les paires": "gagne-memo","bravo quel joli dessin": "gagne-dessin","bravo tu as allumé toutes les lumières": "gagne-lumieres","bzzz coucou viens jouer avec moi": "coucou"};
  const cle = t => String(t).toLowerCase().replace(/ /g, " ").replace(/’/g, "'").replace(/[!?.,;:…]/g, " ").replace(/\s+/g, " ").trim();
  let ctx = null, source = null, dernier = null;
  const cache = new Map();
  const audio = () => ctx || (ctx = new (window.AudioContext || window.webkitAudioContext)());
  const charger = f => {
    if (!cache.has(f)) cache.set(f, fetch(`/assets/voix/${f}.mp3`)
      .then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); })
      .then(b => new Promise((ok, ko) => audio().decodeAudioData(b, ok, ko)))
      .catch(e => { cache.delete(f); throw e; }));
    return cache.get(f);
  };
  function arreter() { dernier = null; if (source) { try { source.stop(); } catch (e) {} source = null; } }
  function dire(texte, secours) {
    const f = TABLE[cle(texte)];
    if (!f || !(window.AudioContext || window.webkitAudioContext)) return false;
    arreter();
    const jeton = dernier = {};
    try { if (audio().state === "suspended") ctx.resume(); } catch (e) { return false; }
    charger(f).then(buf => {
      if (dernier !== jeton) return;
      const s = ctx.createBufferSource(); s.buffer = buf; s.connect(ctx.destination); s.start(); source = s;
      s.onended = () => { if (source === s) source = null; };
    }).catch(() => { if (dernier === jeton && secours) secours(); });
    return true;
  }
  /* charge à l'avance les phrases d'un jeu (pendant que l'enfant regarde l'écran) */
  function prechauffer(textes) { textes.forEach(t => { const f = TABLE[cle(t)]; if (f) charger(f).catch(() => {}); }); }
  return { dire, arreter, prechauffer };
})();
