# Contributing to provostlab.polymtl.ca

This file lives in the website's repo. If you have edit access, you can
add publications, news items, and team members directly — every push to
`main` rebuilds and redeploys the site within ~30 seconds.

> **The English and French versions are kept in sync at the data level.**
> Most things you edit only need to be done once and will appear on both
> `/` and `/fr/`. The exceptions (text-heavy pages like the news feed)
> are called out below.

---

## Add a publication

The publications page reads a single file at
[`src/data/publications.yaml`](./src/data/publications.yaml) and serves
the PDFs from [`public/papers/`](./public/papers/). The old Google
Drive folder + Apps Script widget are no longer used.

### Steps

1. **Drop the PDF** into `public/papers/`. A sensible filename helps —
   we usually use lowercase ASCII with hyphens, e.g.:

   ```
   public/papers/2026-xing-tbme-aberration-correction.pdf
   ```

2. **Add a YAML entry** to `src/data/publications.yaml`, in the
   matching year group. If the year doesn't exist yet, add a new
   `- year: '2027'` block at the top.

   ```yaml
   - year: '2026'
     items:
       - title: 3D Transcranial Dynamic Ultrasound Localization Microscopy in the Mouse Brain Using a Row-Column Array
         pdf: papers/2026-wu-tbme-3d-transcranial-dulm.pdf
         citation: |-
           Wu, A., Porée, J., Ramos-Palacios, G., Ghigo, N., Bourquin, C., Leconte, A., Xing, P., Sadikot, A. F., Chassé, M., & Provost, J. (2026). 3D Transcranial Dynamic Ultrasound Localization Microscopy in the Mouse Brain Using a Row-Column Array. <i>IEEE Transactions on Biomedical Engineering, 73</i>(3), 1112–1123. https://doi.org/10.1109/tbme.2025.3598693
   ```

   Notes on the fields:
   - **`title`** — paper title, no formatting.
   - **`pdf`** — relative path under `public/`, almost always `papers/<filename>.pdf`.
   - **`url`** — use instead of `pdf` when the site has no PDF of the paper.
     The title then opens this link, usually `https://doi.org/...` or the arXiv page.
   - **`citation`** — full APA citation. Use `|-` (literal block) so
     it can span multiple lines. `<i>...</i>` italic tags and `&amp;`
     entities are rendered as HTML. Any `https://...` URL in the
     citation auto-links at build time.
   - `drive_id` is a legacy field on older entries; **skip it on new ones**.

3. **(Optional) Refresh the citation from DOI:**
   ```bash
   npm install        # only the first time you clone the repo
   npm run sync-citations
   ```
   This re-fetches the canonical APA from `doi.org` for every entry
   whose citation contains a DOI link. Use it if you only have a DOI
   and want the citation auto-formatted, or to refresh after a journal
   updates volume / pages. It overwrites citations that were corrected
   by hand, so check `git diff` before committing.

4. **Commit and push.**
   ```bash
   git add public/papers/<your-pdf>.pdf src/data/publications.yaml
   git commit -m "Add <short title>"
   git push
   ```

   The page is live on both `/publications` (English) and
   `/fr/publications` (French) within ~30 seconds — they read the same
   YAML.

---

## Other things you can edit

| What | Where |
|---|---|
| Home news feed (English) | [`src/pages/index.astro`](./src/pages/index.astro) |
| Home news feed (French) | [`src/pages/fr/index.astro`](./src/pages/fr/index.astro) — translate each new entry |
| Research page | [`src/pages/research.astro`](./src/pages/research.astro) + [`src/pages/fr/research.astro`](./src/pages/fr/research.astro) |
| People / Membres | [`src/pages/people.astro`](./src/pages/people.astro) + [`src/pages/fr/people.astro`](./src/pages/fr/people.astro) |
| Code repos list | [`src/data/github_repos.json`](./src/data/github_repos.json) — refresh with the curl command in the file's header |
| Videos | [`src/pages/publications/videos.astro`](./src/pages/publications/videos.astro) + the French copy |
| Headshots | [`public/people/<slug>.jpg`](./public/people/) — the page computes the slug from the person's name |
| News images / GIFs | [`public/news/`](./public/news/) |
| Site colors / fonts / layout | [`src/layouts/Base.astro`](./src/layouts/Base.astro) |

---

## Working locally (optional)

You don't need to run anything locally to edit text — pushing a commit
is enough. But if you want to preview before pushing:

```bash
npm install   # first time only
npm run dev   # opens a live-reloading preview at http://localhost:4321
npm run build # production build, useful to catch errors
```

Node 22+ required (the deploy workflow uses Node 22 too).

---

## Need help?

If you're not sure how to format something or you want to make a more
involved change, open an issue or ask Jean.
