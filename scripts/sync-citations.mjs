#!/usr/bin/env node
// Refresh APA citations in src/data/publications.yaml by re-fetching from doi.org.
// For each entry whose citation contains a https://doi.org/... URL, ask doi.org
// for "text/x-bibliography; style=apa" and write it back to the YAML.
//
// Usage:   npm run sync-citations
import fs from 'node:fs';
import yaml from 'js-yaml';

const path = 'src/data/publications.yaml';
const data = yaml.load(fs.readFileSync(path, 'utf8'));

const extractDoi = (cite) => {
  const m = cite.match(/https?:\/\/doi\.org\/(\S+)/i);
  return m ? m[1].replace(/[.,;)\]>"]+$/, '') : null;
};

async function apa(doi) {
  const r = await fetch('https://doi.org/' + encodeURIComponent(doi), {
    headers: { Accept: 'text/x-bibliography; style=apa' },
  });
  if (!r.ok) return null;
  // doi.org title-cases journal names into "&Amp;", which browsers show as-is.
  return (await r.text()).trim().replace(/&Amp;/g, '&amp;');
}

let updated = 0, skipped = 0, missing = 0;
for (const g of data) {
  for (const it of g.items) {
    const doi = extractDoi(it.citation || '');
    if (!doi) { missing++; continue; }
    process.stdout.write(`  ${doi}... `);
    try {
      const fresh = await apa(doi);
      if (!fresh) { console.log('not available'); skipped++; continue; }
      if (fresh.replace(/\s+/g, ' ') === (it.citation || '').replace(/\s+/g, ' ').trim()) {
        console.log('unchanged');
        skipped++;
      } else {
        it.citation = fresh;
        console.log('UPDATED');
        updated++;
      }
    } catch (e) {
      console.log('error:', e.message);
      skipped++;
    }
    await new Promise((r) => setTimeout(r, 250)); // be polite to doi.org
  }
}

fs.writeFileSync(path, yaml.dump(data, { sortKeys: false, lineWidth: -1 }));
console.log(`\nDone. updated=${updated}  unchanged/skipped=${skipped}  no-doi=${missing}`);
