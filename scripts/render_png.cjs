// Optional raster exports. Run npm install, then npm run png.
const sharp = require('sharp');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
(async () => {
  for (const start of [1997, 2007]) {
    const base = path.join(root, 'charts', `motherfunctor-days-late-${start}-2026`);
    await sharp(base + '.svg', {density: 144}).png().toFile(base + '.png');
    console.log(base + '.png');
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
