// Fabrique les aperçus PNG et les PDF des coloriages à partir des pages du site.
// Utilisation (depuis la racine du site, Playwright installé) : node outils/apercus.js .
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const RACINE = path.resolve(process.argv[2] || '.');
// tous les coloriages qui ont une page (/coloriages/<slug>/) ; aperçus PNG pour les dessins vectoriels
const SLUGS = fs.readdirSync(path.join(RACINE, 'coloriages'), { withFileTypes: true })
  .filter(d => d.isDirectory() && fs.existsSync(path.join(RACINE, 'coloriages', d.name, 'index.html'))).map(d => d.name)
  .sort((a, b) => (b.startsWith('zoe-et-pico') - a.startsWith('zoe-et-pico')) || a.localeCompare(b));
const SVG = SLUGS.filter(s => fs.existsSync(path.join(RACINE, `coloriages/svg/${s}.svg`)));
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.json': 'application/json' };

const serveur = http.createServer((req, res) => {
  let f = path.join(RACINE, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!f.startsWith(RACINE) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise(r => serveur.listen(0, '127.0.0.1', r));
  const B = `http://127.0.0.1:${serveur.address().port}`;
  fs.mkdirSync(path.join(RACINE, 'coloriages/img'), { recursive: true });
  fs.mkdirSync(path.join(RACINE, 'coloriages/pdf'), { recursive: true });
  const b = await chromium.launch();

  // aperçus PNG 800 x 800 (fond blanc)
  const p = await b.newPage({ viewport: { width: 800, height: 800 } });
  for (const s of SVG) {
    await p.setContent(`<body style="margin:0;background:#fff"><img src="${B}/coloriages/svg/${s}.svg" style="width:800px;height:800px;display:block"></body>`);
    await p.waitForFunction(() => document.images[0].complete);
    await p.screenshot({ path: path.join(RACINE, `coloriages/img/${s}.png`) });
  }

  // PDF A4 : exactement ce que donne le bouton « Imprimer »
  const prepare = async (page, slugs) => {
    await page.evaluate(async slugs => {
      const zone = document.createElement('div'); zone.id = 'impression';
      for (const [i, s] of slugs.entries()) {
        const html = await (await fetch(`/coloriages/${s}/`)).text();
        const f = new DOMParser().parseFromString(html, 'text/html').getElementById('feuille');
        f.removeAttribute('id'); if (i < slugs.length - 1) f.style.breakAfter = 'page';
        zone.appendChild(document.importNode(f, true));
      }
      document.body.appendChild(zone); document.body.classList.add('imprime');
      await Promise.all([...zone.querySelectorAll('img')].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
      await document.fonts.ready;
    }, slugs);
    await page.emulateMedia({ media: 'print' });
  };
  const pdf = await b.newPage();
  for (const s of SLUGS) {
    await pdf.goto(`${B}/coloriages/${s}/`); await prepare(pdf, [s]);
    await pdf.pdf({ path: path.join(RACINE, `coloriages/pdf/coloriage-${s}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
    await pdf.evaluate(() => { document.getElementById('impression').remove(); document.body.classList.remove('imprime'); });
    await pdf.emulateMedia({ media: 'screen' });
  }
  await pdf.goto(`${B}/coloriages/`); await prepare(pdf, SLUGS);
  await pdf.pdf({ path: path.join(RACINE, 'coloriages/pdf/coloriages-zoe-et-pico.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close(); serveur.close();
  console.log('aperçus et PDF prêts');
})();
