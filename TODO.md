# ChromaCraft Product Roadmap

> Current focus: finish the Phase 0 baseline, then ship the everyday color tools that run in the browser, before building persistence and the library.
>
> Last reviewed: November 13, 2026

## Product value

ChromaCraft helps a user turn visual or verbal inspiration into an editable, accessible, implementation-ready color system: one that works in any browser, needs no account, and exports into the tools they already use.

The core workflow is:

```text
Image, concept, harmony rule, or color wheel
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
| "I need colors for this idea or photo." | Generate from an image (with a mood such as muted or bright), a written concept, or a harmony rule. |
| "Which colors go together, by color theory?" | Pick a base color on a color wheel and apply any of eight harmony rules; drag the colors on the wheel to fine-tune. |
| "Keep the colors I like and change the rest." | Lock colors and regenerate with one key press. |
| "Is this text readable?" | Contrast matrix with WCAG AA/AAA results, plus accessible alternatives. |
| "Can people with color blindness tell these apart?" | Color-blindness simulation, with the pairs that become hard to tell apart flagged. |
| "I need lighter and darker versions of one color." | A shades-and-tints scale (50–950) for any color. |
| "How will this look in a real UI?" | A preview that applies the palette's roles to page templates. |
| "Get it into my code or design tool." | CSS, SCSS, Tailwind, design-token JSON (Figma), ASE (Adobe apps), SVG, PNG, and copy-as-code. |
| "Send it to someone, or open it on another device." | A share link that encodes the palette in the URL. No account or server storage. |
| "Don't lose my work." | Local autosave, a palette library, and version history. |

## Platform

ChromaCraft uses the same stack as the other products: one host per job, no extra services without a measured need.

| Job | Service | ChromaCraft |
|---|---|---|
| Frontend | Vercel | Project `chroma-craft`, `https://chromacraft-app.vercel.app` |
| API (AI, images, palettes) | Railway | Service `ChromaCraft`, `https://chromacraft-production.up.railway.app` |
| Database, sign-in, file storage | Supabase | Not needed until cloud persistence (after v1) |
| Code, CI, dependency updates | GitHub | `IbukunSanni/ChromaCraft`, Actions, Dependabot |

## Benchmark: Coolors and Adobe Color

ChromaCraft is compared against the two tools people most often use for palettes:

- **Coolors:** a fast generator with an AI palette tool. Many of its tools (more than 5 colors, contrast checks, variations, the visualizer, unlimited saving, advanced exports) appear on its paid Pro plan.
- **Adobe Color** (now part of Adobe Express): free and strong on color theory. It has a color wheel with nine harmony rules, image extraction with color moods, gradient extraction, a contrast checker, and a color-blind-safe checker. Saving goes to Adobe Libraries and needs an Adobe sign-in, and its color wheel states that it does not use generative AI.

ChromaCraft's position: **Coolors' speed and AI plus Adobe Color's color theory and accessibility tools, free, with no account, exporting into any tool (code, Figma tokens, and Adobe apps).** Every tool that runs in the browser is free. Only features with a running cost (AI generation volume, cloud sync, teams) could ever be paid.

Size key: **S** = runs in the browser and reuses existing code. **M** = needs a new UI surface or depends on local storage. **L** = needs a backend, accounts, or a content library.

The Coolors column reflects the features listed on its Pro plan page (checked November 13, 2026); some may also be partly free. The Adobe Color column reflects color.adobe.com, checked the same day.

| Capability | Coolors | Adobe Color | ChromaCraft today | Decision | Size | Phase |
|---|---|---|---|---|---|---|
| Harmony rules | Generator (rules not listed) | 9: analogous, complementary, split complementary, triad, square, compound, shades, monochromatic, custom | 6 in the backend (no compound or shades); only 4 offered in the UI | Offer all rules in the UI and add compound and shades. "Custom" comes from manual editing (Phase 3). | S | 1 |
| Color wheel | — | Create palettes on a wheel and drag color stops | None | Adopt as a creation option: pick a base color on the wheel and see the harmony rule's colors as markers (P1); drag individual stops for a custom palette (P3) | S–M, M | 1, 3 |
| Palette size | Up to 10 (Pro) | Add colors | Harmony and image fixed at 5; AI up to 8 | Free: 2–10 colors in every generator, add/remove colors | S | 1 |
| AI generation | Coolors AI (Pro) | Not on the color wheel ("does not use generative AI") | Concept → palette; image + concept transform | Keep as a differentiator; add rate and cost limits | — | 6 |
| Palette from an image | Pick colors from an image (Pro list) | Extract with moods (colorful, bright, muted, deep, dark); JPEG, PNG, WebP up to 40 MB | Auto-extracts 5 colors; JPG/PNG up to 10 MB | Choose the count 2–10 (P1); moods and a click-to-pick eyedropper (P3); accept WebP (P6) | S–M | 1, 3, 6 |
| Gradients | Save gradients (Pro) | Extract a gradient from an image | None | CSS gradient from the palette (P5); gradient from an image (P7) | S, M | 5, 7 |
| Contrast checker | Check palette contrast (Pro) | Contrast checker (WCAG) | Contrast math exists; swatch badge disabled | Free full matrix with AA/AAA, plus role pairs (P3) | S | 1 |
| Color-blindness | — | Simulator and color-blind-safe check (deuteranopia, protanopia, tritanopia) | None | Simulate 4 types (adds achromatopsia) and flag pairs that become hard to tell apart | S | 1 |
| Shades and variations | Palette variations (Pro) | Shades rule; adjust tints | Brightness/saturation helpers exist | Shades-and-tints scale (50–950) per color; whole-palette variants | S | 1 |
| Undo/redo | — | Yes | None | Bounded undo/redo history | M | 3 |
| UI preview | Palette Visualizer layouts (Pro) | Preview colors together | None | One role-based template, then three | M | 3, 7 |
| Save palettes | Unlimited (Pro) | Adobe Libraries (sign-in) | None | Local library in IndexedDB, no account | M | 2, 4 |
| Save single colors | Unlimited (Pro) | Libraries | None | Local favorite colors | S | 4 |
| Projects and collections | Unlimited (Pro) | Libraries | None | Local collections and tags | M | 7 |
| Ready-made palettes | 10M+ schemes | Explore palettes | None | Curated starter set (P7); a full catalog needs content and a backend | L | 7, after v1 |
| Export | Advanced export options; PDF with custom logo (Pro) | Download HEX/RGB; Libraries for Adobe apps | Basic PNG endpoint | CSS, SCSS, Tailwind (v3 and v4), design-token JSON, SVG, PNG with names, ASE for Adobe apps, copy-as-code | M | 5 |
| Color value formats | — | HEX, RGB | HEX | Copy as HEX, RGB, HSL, and OKLCH | S | 1 |
| Named-color libraries | Color libraries (Pro) | — | XKCD names | Nearest Tailwind and CSS named color; skip licensed libraries such as Pantone | S | 5 |
| Sharing | Profile pages (Pro) | Libraries | None | Share link that encodes the palette in the URL | S | 1 |
| Account | Free account; Pro is paid | Adobe sign-in to save | None needed | No account for any browser tool | — | — |
| Dark mode, no ads | Pro | — | Done | — | — | — |
| Collages, saved fonts, profile pages | Pro | — | None | Not pursuing for v1 | L | Deferred |

Additions beyond both benchmarks that are cheap and solve real problems:

- Spacebar to regenerate and a keyboard-first flow (S, Phase 1)
- Contrast checks on the roles a UI actually uses (text on background, text on surface), not just color pairs (S, Phase 3)
- Installable, offline-capable app for every non-AI feature (S–M, Phase 6)
- Design-token JSON that opens in Figma token plugins and Style Dictionary (S, Phase 5)

## Definition of Done: useful v1

ChromaCraft v1 is done only when a user can complete the following journey reliably:

1. Create a palette of 2–10 colors from an image, a written concept, any of the eight harmony rules, or the color wheel.
2. Edit any color, add or remove colors, reorder colors, and lock colors during regeneration (including with the spacebar).
3. Assign practical roles such as primary, secondary, accent, surface, and text.
4. See WCAG contrast results for the whole palette and for role pairs, preview the palette under common color-blindness types, and see which pairs become hard to tell apart.
5. Open a shades-and-tints scale for any color and add a step to the palette.
6. Undo and redo edits without losing work.
7. Share a palette as a link that opens the same palette on any device.
8. Name and save a palette locally without creating an account.
9. Reload the application and recover the last workspace and saved palettes.
10. Open, rename, duplicate, archive, and delete a saved palette, and see and restore earlier versions.
11. Export the result as PNG, SVG, CSS variables, Tailwind, design-token JSON, and ASE, and import a previously exported ChromaCraft JSON file.
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
- [x] Rename the hosted resources: Vercel and Railway projects `chroma-craft`, production domain `chromacraft-app.vercel.app`, Railway domain `chromacraft-production.up.railway.app`, and `NEXT_PUBLIC_API_URL` pointed at Railway (November 13, 2026).
- [x] Railway: the domain targets port 8000 to match the app, and `/` responds (fixed November 13, 2026; the 502 was an 8080/8000 mismatch).
- [x] Vercel: `NEXT_PUBLIC_API_URL` points at the Railway domain for Production and Preview, and palette generation works on `chromacraft-app.vercel.app` (verified November 13, 2026).
- [ ] Railway: set the config-as-code path to `/backend/railway.json` so deploys use `python server.py` and the `/` health check. Afterwards, check that the deploy log port still matches the domain's port (8000).
- [ ] Decide whether production gets AI text-to-palette: set `OPENAI_API_KEY` on Railway with a dedicated, budget-capped OpenAI project key, or hide the AI card when no key is set.
- [ ] Add GitHub Actions CI: backend `pytest`, plus frontend lint, tests, and production build, on pull requests to `dev` and `main`.
- [ ] Turn on Dependabot security updates. The vulnerable Next.js release blocked production deploys for months.
- [ ] Install from a clean environment and correct dependency declarations.
- [ ] Decide on `torch`/`sentence-transformers`. `/adjust-concept` uses them only to score a concept against six words, at the cost of a ~15 s first request, ~440 MB of memory, and a multi-GB image. Replace them with OpenAI embeddings or AI-returned adjustment weights, or keep them and document the cost.
- [ ] Start frontend and backend together and exercise every implemented endpoint. (Every endpoint was exercised locally and in production on November 13, 2026, except a live OpenAI `/generate/concept` call, which needs `OPENAI_API_KEY`.)
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
- [ ] Offer all harmony rules in the UI (today only 4 of the backend's 6 are shown), and add compound and shades to the backend. [S]
- [ ] Color wheel as a creation option alongside Random and the harmony buttons: pick a base color on the wheel, see the chosen harmony rule's colors as markers, and watch the palette update live. Locked colors stay fixed. Works with keyboard and touch as well as mouse. [S–M]
- [ ] Spacebar regenerates unlocked colors, and keyboard focus is preserved. [S]
- [ ] Contrast matrix: every color against every other, with ratio and AA/AAA for normal and large text, reusing `color-utils.ts`. Turn on the swatch contrast badge. [S]
- [ ] Shades-and-tints scale (50–950) for any color, with copy and "add to palette". [S]
- [ ] Whole-palette variants: lighter, darker, muted, vivid. [S]
- [ ] Color-blindness simulation (protanopia, deuteranopia, tritanopia, achromatopsia) for the whole palette, flagging pairs whose simulated colors become hard to tell apart. [S]
- [ ] Copy any color as HEX, RGB, HSL, or OKLCH. [S]
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
- [ ] Image extraction moods (colorful, bright, muted, deep, dark) that choose different colors from the same image. [S–M]
- [ ] Color wheel editing: drag individual color stops to customize the palette (a "custom" harmony), with brightness and saturation controls, kept in sync with the palette in both directions. [M]

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
- [ ] Export ASE (Adobe Swatch Exchange) so palettes open in Photoshop, Illustrator, and InDesign. [S]
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
- [ ] Validate upload MIME type, decoded image content, dimensions, and file size; accept WebP as well as JPEG and PNG, and make the UI text match the real limits.
- [ ] Add rate limiting and cost controls for AI endpoints.
- [ ] Make the app installable (web app manifest) and keep every non-AI tool working offline. [S–M]
- [ ] Add caching only after measuring repeated requests and defining privacy behavior.
- [ ] Audit keyboard navigation, focus visibility, labels, reduced motion, and touch targets.
- [ ] Test the complete Definition of Done journey on common desktop and mobile viewport sizes.
- [ ] Add privacy copy explaining local storage and image handling.
- [ ] Add error monitoring without recording concepts or image data by default.

**Phase 6 exit criteria:** all Definition of Done items and quality gates are verified in a production-like environment.

### Phase 7 — Benchmark extras (v1.1)

Goal: close the remaining practical gaps with Coolors and Adobe Color using local-only features.

- [ ] Collections and tags for saved palettes and colors. [M]
- [ ] Extract a gradient from an uploaded image. [M]
- [ ] Two more preview templates (dashboard, mobile app). [M]
- [ ] A small curated starter set of palettes, grouped by use (brand, UI, data visualization). [M]

## After useful v1

### Cloud persistence (Supabase)

Cloud persistence is the next milestone, not a prerequisite for validating the local-first product. It uses Supabase Postgres for data and Supabase Auth for sign-in.

How the pieces fit:

- The frontend uses `supabase-js` only to sign in. It sends the user's access token with each request to the API.
- FastAPI on Railway verifies the token against the Supabase project's published signing keys and is the only code that reads or writes the database. Every query is scoped to the signed-in user.
- Row-level security is enabled on every table with no public policies, so the public anon key cannot read data directly.
- Railway connects through Supabase's **session pooler** connection string, which works over IPv4. Railway's outbound IPv6 is off by default, and Supabase's direct database host is IPv6-only.
- The Supabase project lives in the same region as the Railway service.
- The Phase 2 `PaletteRepository` gets a second implementation that calls the API, so local and cloud storage share one interface.

When users need cross-device access beyond share links:

- [ ] Create a `chromacraft` Supabase project in the Railway service's region.
- [ ] Add tables for palettes, palette versions, and optional source-image records, with SQLAlchemy models and Alembic migrations in `backend/` (row-level security policies included in the migrations).
- [ ] Sign in with Supabase Auth (email magic link, plus Google and GitHub); ChromaCraft never stores passwords.
- [ ] Verify Supabase access tokens in FastAPI and reject requests for another user's data.
- [ ] Set the variables: on Railway, `DATABASE_URL` (session pooler) and `SUPABASE_URL`; on Vercel, `NEXT_PUBLIC_SUPABASE_URL` and the public anon (publishable) key. Never expose the service-role key to the browser.
- [ ] Keep anonymous local use available.
- [ ] Offer an explicit local-to-cloud import after sign-in.
- [ ] Create a new version on sync conflict instead of silently overwriting.
- [ ] Add read-only share links with revocation for saved palettes.
- [ ] Add a public or private profile page.
- [ ] Store source images only when a user explicitly keeps them, in a private Supabase Storage bucket.
- [ ] Define account export and deletion behavior before launch, including deleting the Supabase Auth user and their storage files.
- [ ] Plan for Supabase Pro once cloud sync is live: free projects pause after about a week without activity, and the free plan allows two active projects.

Suggested resources:

```text
auth.users          (managed by Supabase Auth)
palettes            (owner = auth.users.id)
palette_versions    (JSON snapshot per version)
source_images       (optional, explicit retention only; files in Supabase Storage)
```

Palette version snapshots may use JSON initially. Normalize color records only when real query requirements justify the added complexity.

### Free and paid boundary (if ChromaCraft is ever monetized)

- Always free: everything that runs in the browser (all generators except AI volume, palette size up to 10, contrast, variations, simulation, preview, exports, the local library, share links).
- Candidates for a paid tier, because they have a running cost: higher AI generation limits, cloud sync across devices, team workspaces. Per-user limits and plans would live in Supabase Postgres.

## Deferred until after useful v1

These ideas may be valuable later but currently dilute the core outcome:

- Large browsable catalog of community or ready-made palettes
- Custom AI model training
- Social feeds, trending palettes, and public showcases
- Collages, saved fonts, and PDF export with custom branding
- Licensed color libraries (for example Pantone)
- Native mobile and desktop applications
- Browser extensions
- Figma or Adobe plugins (design-token JSON and ASE exports cover the first need)
- Team and enterprise collaboration
- Batch processing
- Embed codes
- Advanced analytics and A/B testing
- GPL and other specialist formats (ASE is in Phase 5)
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
4. Ship the Phase 1 tools in this order: 2–10 colors, all harmony rules, color wheel, contrast matrix, shades and tints, share link, color-blindness check, copy-as-code.
5. Continue through Phases 2–6 until every useful v1 Definition of Done item is verified.
