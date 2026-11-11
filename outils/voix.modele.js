/* =========================================================
   Zoé et Pico — la vraie voix de Pico (enregistrements dans /assets/voix/)
   Fichier généré par outils/voix.py à partir de outils/voix.modele.js : ne pas modifier à la main.
   ZPVoix.dire(texte, secours) joue l'enregistrement de la phrase s'il existe et renvoie true ;
   sinon renvoie false (la synthèse vocale du navigateur prend le relais).
   ========================================================= */
"use strict";
window.ZPVoix = (() => {
  const TABLE = /*TABLE*/{};
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
