# ChromaCraft Product Roadmap

> Current focus: finish the Phase 0 baseline, then ship the everyday color tools that run in the browser, before building persistence and the library.
>
> Last reviewed: November 13, 2026

## Product value

ChromaCraft helps a user turn visual or verbal inspiration into an editable, accessible, implementation-ready color system: one that works in any browser, needs no account, and exports into the tools they already use.

The core workflow is:

```text
Image, concept, or harmony rule
    → generate a palette of 2–10 colors
    → edit, lock, vary, and regenerate
    → assign practical color roles
    → check contrast and color-blind legibility
    → share, save, and revisit versions
    → export to code and design tools
```

Generation attracts a user. Checking, varying, sharing, and exporting are what make the product worth returning to.

### Problems ChromaCraft solves

| User problem | ChromaCraft answer |
|---|---|
| "I need colors for this idea or photo." | Generate from an image, a written concept, or a harmony rule. |
| "Keep the colors I like and change the rest." | Lock colors and regenerate with one key press. |
| "Is this text readable?" | Contrast matrix with WCAG AA/AAA results, plus accessible alternatives. |
| "Can people with color blindness tell these apart?" | Color-blindness simulation of the whole palette. |
| "I need lighter and darker versions of one color." | A shades-and-tints scale (50–950) for any color. |
| "How will this look in a real UI?" | A preview that applies the palette's roles to page templates. |
| "Get it into my code or design tool." | CSS, SCSS, Tailwind, design-token JSON, SVG, PNG, and copy-as-code. |
| "Send it to someone, or open it on another device." | A share link that encodes the palette in the URL. No account or server storage. |
| "Don't lose my work." | Local autosave, a palette library, and version history. |

## Benchmark: Coolors Pro

Coolors puts many of its tools behind a paid Pro plan. Most of those tools are pure color math that runs in the browser and costs nothing to serve. ChromaCraft's position: **every tool that runs in the browser is free and needs no account.** Only features with a running cost (AI generation volume, cloud sync, teams) could ever be paid.

Size key: **S** = runs in the browser and reuses existing code. **M** = needs a new UI surface or depends on local storage. **L** = needs a backend, accounts, or a content library.

| Coolors Pro capability | ChromaCraft today | Decision | Size | Phase |
|---|---|---|---|---|
| Palettes beyond 5 colors (up to 10) | Harmony and image fixed at 5; AI concept up to 8 | Adopt, free: 2–10 colors in every generator, add/remove colors | S | 1 |
| AI palette generation | Concept → palette; image + concept transform | Keep; add rate and cost limits | — | 6 |
| Pick colors from an image | Auto-extracts 5 dominant colors | Adopt: choose the extraction count (2–10), then a click-to-pick eyedropper on the uploaded image | S, then M | 1, 3 |
| Contrast checker | Contrast math in `frontend/utils/color-utils.ts`; swatch badge exists but is disabled | Adopt, free: full contrast matrix with AA/AAA | S | 1 |
| Color and palette variations | Brightness/saturation helpers exist | Adopt: shades-and-tints scale per color; whole-palette lighter/darker/muted variants | S | 1 |
| Palette visualizer | None | Adopt, small: one role-based template first, then three (landing page, dashboard, mobile) | M | 3, 7 |
| Save unlimited palettes | None | Adopt: local library in IndexedDB, no account | M | 2, 4 |
| Save individual colors | None | Adopt: favorite colors in the local library | S | 4 |
| Projects and collections | None | Adopt: collections and tags in the local library | M | 7 |
| Advanced export options | Basic PNG endpoint | Adopt: CSS, SCSS, Tailwind (v3 and v4), design-token JSON, SVG, PNG with names, copy-as-code | M | 5 |
| Gradients | None | Adopt: CSS gradient from the palette, copy and export | S | 5 |
| Color libraries | XKCD color names | Adopt open libraries: nearest Tailwind and CSS named color. Skip licensed libraries such as Pantone. | S | 5 |
| Dark mode | Done | — | — | — |
| No ads | No ads | — | — | — |
| Large catalog of ready-made palettes | None | Later: start with a small curated starter set; a catalog needs content and a backend | L | After v1 |
| Public or private profile page | None | After cloud accounts | L | After v1 |
| Collages, saved fonts, PDF export with a custom logo | None | Not pursuing for v1 | L | Deferred |

Additions beyond the benchmark list that are cheap and solve real problems:

- Share link with the palette encoded in the URL (S, Phase 1)
- Color-blindness simulation (S, Phase 1)
- Spacebar to regenerate and a keyboard-first flow (S, Phase 1)
- Installable, offline-capable app for every non-AI feature (S–M, Phase 6)
- Design-token JSON that opens in Figma token plugins and Style Dictionary (S, Phase 5)

## Definition of Done: useful v1

ChromaCraft v1 is done only when a user can complete the following journey reliably:

1. Create a palette of 2–10 colors from an image, a written concept, or a color-harmony generator.
2. Edit any color, add or remove colors, reorder colors, and lock colors during regeneration (including with the spacebar).
3. Assign practical roles such as primary, secondary, accent, surface, and text.
4. See WCAG contrast results for the whole palette and for role pairs, and preview the palette under common color-blindness types.
5. Open a shades-and-tints scale for any color and add a step to the palette.
6. Undo and redo edits without losing work.
7. Share a palette as a link that opens the same palette on any device.
8. Name and save a palette locally without creating an account.
9. Reload the application and recover the last workspace and saved palettes.
10. Open, rename, duplicate, archive, and delete a saved palette, and see and restore earlier versions.
11. Export the result as PNG, SVG, CSS variables, Tailwind, and design-token JSON, and import a previously exported ChromaCraft JSON file.
12. Complete the core journey on desktop and mobile using keyboard, mouse, or touch.

The release also must meet these quality gates:

- [ ] A fresh clone can be set up using the documented commands.
- [ ] Frontend and backend start together without import or configuration errors.
- [ ] CI runs backend tests and frontend lint, tests, and build on every pull request.
- [ ] A deploy from `main` succeeds on Vercel and Railway, and the API health check (`/`) responds.
- [x] Frontend API declarations match implemented backend endpoints.
- [ ] Core frontend and backend tests pass in a clean environment.
- [ ] Invalid images, unavailable AI, timeouts, and malformed input produce useful errors without destroying existing work.
- [ ] Autosave visibly reports `Saving`, `Saved locally`, or `Save failed`.
- [ ] Stored data has a versioned schema and a tested migration path.
- [ ] No OpenAI key or other secret is exposed to the browser or committed to Git.
- [ ] Uploaded images have documented size/type limits and are not retained without the user's knowledge.
- [ ] The core workflow has no known data-loss or keyboard-blocking defects.

Items outside this Definition of Done are deferred unless they directly unblock it.

## Current reality

### Implemented

- [x] Image-based dominant-color extraction (fixed at 5 colors)
- [x] AI concept-to-palette generation (3–8 colors in the UI)
- [x] Concept-based transformation of an extracted palette
- [x] Random and harmony-based palette generation (fixed at 5 colors)
- [x] Color naming using the XKCD color dataset
- [x] Click-to-copy color values
- [x] Lock/unlock colors during regeneration (locked colors keep their position)
- [x] Basic keyboard interaction for palette swatches
- [x] Light/dark theme support
- [x] Basic PNG generation
- [x] FastAPI route/service/utility separation
- [x] Centralized frontend API client

### Built but not exposed

- Contrast ratio, WCAG level, and pairwise palette contrast functions (`frontend/utils/color-utils.ts`)
- A contrast badge on each swatch (`showAccessibility` is `false` everywhere)
- Brightness, saturation, and hue adjustment helpers that can drive shades, tints, and variants

### Known gaps and inconsistencies

- [x] Restore the missing backend request/response models imported by the routes.
- [ ] Ensure all backend dependencies, including OpenAI, install from `requirements.txt`.
- [ ] Make the documented setup commands work on supported Windows shells.
- [x] Reconcile frontend-only API declarations with real backend endpoints.
- [x] Verify the PNG request format agrees between frontend and backend.
- [x] Remove or update stale README/TODO claims.
- [ ] Resolve text/emoji encoding corruption where it appears. (The Windows `UnicodeEncodeError` crash is fixed; emoji in UI copy and logs remain.)
- [x] Remove or properly ignore temporary development files.
- [ ] The page has three separate palettes (AI concept, harmony, image), and only the harmony one supports locks.
- [ ] Image upload and concept adjustment call `fetch` directly, bypassing the API client, and show nothing to the user when they fail.

## Execution plan

Work in order. Do not begin a later phase while an earlier phase has release-blocking failures.

Phase order changed on November 13, 2026: the browser-only tools (Phase 1) now come before persistence. They are pure functions of a list of colors, so they do not depend on the storage design, and they deliver most of the benchmark's paid value early. The share link gives cross-device access before any storage exists.

### Phase 0 — Establish a reliable baseline

Goal: a contributor can run, test, and deploy the existing application before new product work begins.

- [x] Add or restore backend Pydantic request/response models.
- [x] Merge PR #8 into `main` (November 13, 2026).
- [ ] Name every hosted resource `chromacraft`: the Vercel project, the Railway project and service, and the Railway domain `chromacraft-production.up.railway.app`.
- [ ] Railway: set the config-as-code path to `/backend/railway.json`, remove any manual `PORT` variable, set `OPENAI_API_KEY`, and check that `/` responds (it currently returns 502).
- [ ] Vercel: set `NEXT_PUBLIC_API_URL` to the Railway domain for Production and Preview, redeploy, and confirm that palette generation works on the production site.
- [ ] Add GitHub Actions CI: backend `pytest`, plus frontend lint, tests, and production build, on pull requests to `dev` and `main`.
- [ ] Turn on Dependabot security updates. The vulnerable Next.js release blocked production deploys for months.
- [ ] Install from a clean environment and correct dependency declarations.
- [ ] Decide on `torch`/`sentence-transformers`. `/adjust-concept` uses them only to score a concept against six words, at the cost of a ~15 s first request, ~440 MB of memory, and a multi-GB image. Replace them with OpenAI embeddings or AI-returned adjustment weights, or keep them and document the cost.
- [ ] Start frontend and backend together and exercise every implemented endpoint. (All endpoints except a live `/generate/concept` call were exercised on November 13, 2026.)
- [ ] Align API paths, payload names, response types, and error shapes. (Paths, payloads, and response types now match.)
  - [ ] Return 400/422, not 500, for concept validation errors, and use the codes in `backend/constants/error_codes.py`.
  - [ ] Route image upload and concept adjustment through the API client, and show their errors in the UI.
- [x] Remove client methods for endpoints that are not part of the current scope, or implement the required endpoints.
- [x] Make lint, frontend tests, backend tests, and frontend production build pass.
- [ ] Fix `pnpm run setup:backend` on Windows, and use one virtual-environment folder name (`backend/venv` or `backend/.venv`) everywhere.
- [x] Remove the unused `backend/render.yaml`; Railway is the only backend host.
- [ ] Archive `.kiro/specs` so this file is the single plan.
- [ ] Update README setup, environment, and feature documentation from verified behavior.

**Phase 0 exit criteria:** documented setup succeeds, CI passes, both applications start, and production serves the current `main`.

### Phase 1 — One workspace and everyday color tools

Goal: a user can generate, check, vary, and share a palette of up to 10 colors without an account, on any device.

- [ ] Define the canonical palette model (stable palette and color IDs, value, name, role, lock state, order, source, concept, timestamps) for the in-memory workspace. Storage comes in Phase 2.
- [ ] Merge the AI concept, harmony, and image flows into one workspace palette that every generator writes into. Locks then apply to every source.
- [ ] Replace the client-side lock-position workaround (`frontend/lib/palette-locks.ts`) with ID-based locks, and let the backend accept locked positions.
- [ ] Support 2–10 colors in every generator: add a `color_count` parameter to `/generate/random` and `/extract-colors`, offer up to 10 in the AI flow, and add add/remove-color controls. [S]
- [ ] Spacebar regenerates unlocked colors, and keyboard focus is preserved. [S]
- [ ] Contrast matrix: every color against every other, with ratio and AA/AAA for normal and large text, reusing `color-utils.ts`. Turn on the swatch contrast badge. [S]
- [ ] Shades-and-tints scale (50–950) for any color, with copy and "add to palette". [S]
- [ ] Whole-palette variants: lighter, darker, muted, vivid. [S]
- [ ] Color-blindness simulation (protanopia, deuteranopia, tritanopia, achromatopsia) for the whole palette. [S]
- [ ] Share link that encodes the palette in the URL, and opening that link restores it. [S]
- [ ] Copy-as-code for the current palette: HEX list, CSS variables, and a Tailwind snippet. [S]
- [ ] Tests for each pure function: contrast, scales, variants, simulation, and URL encoding round-trip.

**Phase 1 exit criteria:** all of the above works for palettes of 2 and 10 colors, on mobile and desktop, and the share link round-trips exactly.

### Phase 2 — Local persistence

Goal: users never lose useful work during ordinary browser use.

- [ ] Introduce a `PaletteRepository` interface so storage is replaceable.
- [ ] Implement a local repository using IndexedDB; use `localStorage` only for small preferences.
- [ ] Autosave after meaningful changes using a short debounce.
- [ ] Restore the last workspace on reload.
- [ ] Add save-state feedback: `Saving`, `Saved locally`, and `Save failed`.
- [ ] Add schema versioning and migrations.
- [ ] Add JSON backup export and import.
- [ ] Test reload recovery, failed writes, corrupt records, migrations, and import validation.

**Phase 2 exit criteria:** a user can close or reload the browser and recover their palette, metadata, locks, roles, and edit state without manual action.

### Phase 3 — Complete the palette workspace

Goal: generated colors can be refined into a practical color system.

- [ ] Edit an individual color using a color picker and HEX input.
- [ ] Validate and normalize manual color input.
- [ ] Reorder colors with mouse, keyboard, and touch controls.
- [ ] Implement bounded undo/redo history.
- [ ] Assign semantic roles: primary, secondary, accent, surface, background, text, success, warning, and danger.
- [ ] Show contrast for role pairs (text on background, text on surface, and so on) alongside the full matrix.
- [ ] Suggest accessible alternatives without silently changing the palette. The shades scale from Phase 1 supplies the candidates.
- [ ] Preserve roles and locked colors when regenerating where possible.
- [ ] Live preview: one responsive template that uses the assigned roles. [M]
- [ ] Eyedropper: click the uploaded image to pick an exact color into the palette. [M]

**Phase 3 exit criteria:** a user can deliberately refine a generated palette, understand its accessibility, and undo mistakes.

### Phase 4 — Palette library and versions

Goal: ChromaCraft becomes a workspace users can return to.

- [ ] Add a `My Palettes` library.
- [ ] Name, search, sort, open, rename, duplicate, archive, and delete palettes.
- [ ] Save individual favorite colors. [S]
- [ ] Confirm destructive deletion and clearly distinguish it from archive.
- [ ] Create version snapshots for generation and significant edits.
- [ ] View, compare, and restore earlier versions.
- [ ] Protect against accidental overwrite when two tabs edit the same palette.
- [ ] Provide a clear empty state and a short first-use explanation.

**Phase 4 exit criteria:** a user can manage several projects and safely explore alternatives without losing an earlier result.

### Phase 5 — Exports for code and design tools

Goal: users can take the palette directly into real design or development work, anywhere.

- [ ] Keep PNG export working and include palette name, color names, and HEX values.
- [ ] Export SVG.
- [ ] Export canonical ChromaCraft JSON.
- [ ] Export CSS custom properties and SCSS variables using semantic role names.
- [ ] Export Tailwind colors: a v3 config object and a v4 `@theme` block, including shade scales.
- [ ] Export design-token JSON in the W3C Design Tokens format, usable in Figma token plugins and Style Dictionary.
- [ ] Export a CSS gradient built from the palette. [S]
- [ ] Show the nearest Tailwind and CSS named color for each swatch. [S]
- [ ] Preview and copy export text before download.
- [ ] Sanitize generated token names and handle duplicate roles/names.
- [ ] Add round-trip tests for ChromaCraft JSON import/export.

**Phase 5 exit criteria:** every export is valid, deterministic, works on mobile, and is usable without manual cleanup.

### Phase 6 — Product hardening

Goal: the useful v1 workflow is trustworthy outside the developer's machine.

- [ ] Add clear loading, empty, offline, timeout, and retry states.
- [ ] Ensure AI failure leaves current and saved palettes intact.
- [ ] Validate upload MIME type, decoded image content, dimensions, and file size.
- [ ] Add rate limiting and cost controls for AI endpoints.
- [ ] Make the app installable (web app manifest) and keep every non-AI tool working offline. [S–M]
- [ ] Add caching only after measuring repeated requests and defining privacy behavior.
- [ ] Audit keyboard navigation, focus visibility, labels, reduced motion, and touch targets.
- [ ] Test the complete Definition of Done journey on common desktop and mobile viewport sizes.
- [ ] Add privacy copy explaining local storage and image handling.
- [ ] Add error monitoring without recording concepts or image data by default.

**Phase 6 exit criteria:** all Definition of Done items and quality gates are verified in a production-like environment.

### Phase 7 — Benchmark extras (v1.1)

Goal: close the remaining practical gaps with the benchmark using local-only features.

- [ ] Collections and tags for saved palettes and colors. [M]
- [ ] Two more preview templates (dashboard, mobile app). [M]
- [ ] A small curated starter set of palettes, grouped by use (brand, UI, data visualization). [M]

## After useful v1

### Cloud persistence

Cloud persistence is the next milestone, not a prerequisite for validating the local-first product.

When users need cross-device access beyond share links:

- [ ] Add PostgreSQL-backed users, palettes, palette versions, and optional source-image records.
- [ ] Add managed authentication rather than implementing password storage.
- [ ] Keep anonymous local use available.
- [ ] Offer an explicit local-to-cloud import after sign-in.
- [ ] Create a new version on sync conflict instead of silently overwriting.
- [ ] Add read-only share links with revocation for saved palettes.
- [ ] Add a public or private profile page.
- [ ] Define account export and deletion behavior before launch.

Suggested backend resources:

```text
users
palettes
palette_versions
source_images (optional, explicit retention only)
```

Palette version snapshots may use JSON initially. Normalize color records only when real query requirements justify the added complexity.

### Free and paid boundary (if ChromaCraft is ever monetized)

- Always free: everything that runs in the browser (all generators except AI volume, palette size up to 10, contrast, variations, simulation, preview, exports, the local library, share links).
- Candidates for a paid tier, because they have a running cost: higher AI generation limits, cloud sync across devices, team workspaces.

## Deferred until after useful v1

These ideas may be valuable later but currently dilute the core outcome:

- Large browsable catalog of community or ready-made palettes
- Custom AI model training
- Social feeds, trending palettes, and public showcases
- Collages, saved fonts, and PDF export with custom branding
- Licensed color libraries (for example Pantone)
- Native mobile and desktop applications
- Browser extensions
- Figma or Adobe plugins (design-token JSON export covers the first need)
- Team and enterprise collaboration
- Batch processing
- Embed codes
- Advanced analytics and A/B testing
- ASE, GPL, and other specialist formats
- Redis or complex infrastructure without measured need

## Working rules

- Prefer finishing the end-to-end user journey over adding another generator.
- Fix mismatches and broken foundations before building on them.
- Prefer features that run in the browser over ones that need a server; they are free to operate and work offline.
- Every feature must include failure, empty, loading, and recovery behavior.
- Persist user intent—roles, locks, order, concept, and history—not just HEX values.
- Do not mark an item complete because code exists; verify its user-visible acceptance criteria.
- Keep pull requests aligned to one phase outcome where practical.
- Review this roadmap after completing each phase, not on arbitrary calendar dates.

## Immediate next actions

1. Finish the `chromacraft` renames and the Railway and Vercel settings, and confirm production responds.
2. Add CI and Dependabot so `main` cannot silently break again.
3. Build the one-workspace palette model (Phase 1, first two items).
4. Ship the Phase 1 tools in this order: 2–10 colors, contrast matrix, shades and tints, share link, color-blindness simulation, copy-as-code.
5. Continue through Phases 2–6 until every useful v1 Definition of Done item is verified.
