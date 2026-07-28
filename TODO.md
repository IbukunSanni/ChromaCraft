# ChromaCraft Product Roadmap

> Current focus: turn palette generation into a reliable, persistent color-system workspace.
>
> Last reviewed: July 28, 2026

## Product value

ChromaCraft helps a user turn visual or verbal inspiration into an editable, reusable, implementation-ready color system.

The core workflow is:

```text
Image or concept
    → generate a palette
    → edit, lock, and regenerate
    → assign practical color roles
    → check contrast
    → save and revisit versions
    → export usable design tokens
```

Generation attracts a user; continuity, validation, and useful exports make the product worth returning to.

## Definition of Done: useful v1

ChromaCraft v1 is done only when a user can complete the following journey reliably:

1. Create a palette from an image, a written concept, or a color-harmony generator.
2. Edit any color, reorder colors, and lock colors during regeneration.
3. Assign practical roles such as primary, secondary, accent, surface, and text.
4. See clear WCAG contrast results for relevant text/background combinations.
5. Undo and redo edits without losing work.
6. Name and save a palette locally without creating an account.
7. Reload the application and recover the last workspace and saved palettes.
8. Open, rename, duplicate, archive, and delete a saved palette.
9. See and restore earlier versions of a palette.
10. Export the result as PNG, JSON design tokens, and CSS variables.
11. Import a previously exported ChromaCraft JSON file.
12. Complete the core journey on desktop and mobile using keyboard, mouse, or touch.

The release also must meet these quality gates:

- [ ] A fresh clone can be set up using the documented commands.
- [ ] Frontend and backend start together without import or configuration errors.
- [ ] Frontend API declarations match implemented backend endpoints.
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

- [x] Image-based dominant-color extraction
- [x] AI concept-to-palette generation
- [x] Concept-based transformation of an extracted palette
- [x] Random and harmony-based palette generation
- [x] Color naming using the XKCD color dataset
- [x] Click-to-copy color values
- [x] Lock/unlock colors during regeneration
- [x] Basic keyboard interaction for palette swatches
- [x] Light/dark theme support
- [x] Basic PNG generation
- [x] FastAPI route/service/utility separation
- [x] Centralized frontend API client

### Known gaps and inconsistencies

- [ ] Restore the missing backend request/response models imported by the routes.
- [ ] Ensure all backend dependencies, including OpenAI, install from `requirements.txt`.
- [ ] Make the documented setup commands work on supported Windows shells.
- [ ] Reconcile frontend-only API declarations with real backend endpoints.
- [ ] Verify the PNG request format agrees between frontend and backend.
- [ ] Remove or update stale README/TODO claims.
- [ ] Resolve text/emoji encoding corruption where it appears.
- [ ] Remove or properly ignore temporary development files.

## Execution plan

Work in order. Do not begin a later phase while an earlier phase has release-blocking failures.

### Phase 0 — Establish a reliable baseline

Goal: a contributor can run and test the existing application before new product work begins.

- [ ] Add or restore backend Pydantic request/response models.
- [ ] Install from a clean environment and correct dependency declarations.
- [ ] Start frontend and backend together and exercise every implemented endpoint.
- [ ] Align API paths, payload names, response types, and error shapes.
- [ ] Remove client methods for endpoints that are not part of the current scope, or implement the required endpoints.
- [ ] Make lint, frontend tests, backend tests, and frontend production build pass.
- [ ] Update README setup, environment, and feature documentation from verified behavior.

**Phase 0 exit criteria:** documented setup succeeds, both applications start, production frontend build passes, and the test suites run without collection or import errors.

### Phase 1 — Canonical palette model and local persistence

Goal: users never lose useful work during ordinary browser use.

- [ ] Define one canonical, versioned palette model shared conceptually by frontend and backend.
- [ ] Give palettes and individual colors stable IDs.
- [ ] Store color value, name, role, lock state, order, source, concept, timestamps, and generation metadata.
- [ ] Introduce a `PaletteRepository` interface so storage is replaceable.
- [ ] Implement a local repository using IndexedDB; use `localStorage` only for small preferences.
- [ ] Autosave after meaningful changes using a short debounce.
- [ ] Restore the last workspace on reload.
- [ ] Add save-state feedback: `Saving`, `Saved locally`, and `Save failed`.
- [ ] Add schema versioning and migrations.
- [ ] Add JSON backup export and import.
- [ ] Test reload recovery, failed writes, corrupt records, migrations, and import validation.

**Phase 1 exit criteria:** a user can close/reload the browser and recover their palette, metadata, locks, roles, and edit state without manual action.

### Phase 2 — Complete the palette workspace

Goal: generated colors can be refined into a practical color system.

- [ ] Edit an individual color using a color picker and HEX input.
- [ ] Validate and normalize manual color input.
- [ ] Reorder colors with mouse, keyboard, and touch controls.
- [ ] Implement bounded undo/redo history.
- [ ] Assign semantic roles: primary, secondary, accent, surface, background, text, success, warning, and danger.
- [ ] Display WCAG contrast ratios and AA/AAA results for selected foreground/background pairs.
- [ ] Suggest accessible alternatives without silently changing the palette.
- [ ] Preserve roles and locked colors when regenerating where possible.
- [ ] Provide a responsive live preview using the assigned roles.

**Phase 2 exit criteria:** a user can deliberately refine a generated palette, understand its accessibility, and undo mistakes.

### Phase 3 — Palette library and versions

Goal: ChromaCraft becomes a workspace users can return to.

- [ ] Add a `My Palettes` library.
- [ ] Name, search, sort, open, rename, duplicate, archive, and delete palettes.
- [ ] Confirm destructive deletion and clearly distinguish it from archive.
- [ ] Create version snapshots for generation and significant edits.
- [ ] View, compare, and restore earlier versions.
- [ ] Protect against accidental overwrite when two tabs edit the same palette.
- [ ] Provide a clear empty state and a short first-use explanation.

**Phase 3 exit criteria:** a user can manage several projects and safely explore alternatives without losing an earlier result.

### Phase 4 — Implementation-ready exports

Goal: users can take the palette directly into real design or development work.

- [ ] Keep PNG export working and include palette name and optional metadata.
- [ ] Export canonical ChromaCraft JSON.
- [ ] Export CSS custom properties using semantic role names.
- [ ] Export a Tailwind-compatible color object.
- [ ] Preview and copy export text before download.
- [ ] Sanitize generated token names and handle duplicate roles/names.
- [ ] Add round-trip tests for ChromaCraft JSON import/export.

**Phase 4 exit criteria:** the exported CSS and JSON are valid, deterministic, accessible from mobile, and usable without manual cleanup.

### Phase 5 — Product hardening

Goal: the useful v1 workflow is trustworthy outside the developer's machine.

- [ ] Add clear loading, empty, offline, timeout, and retry states.
- [ ] Ensure AI failure leaves current and saved palettes intact.
- [ ] Validate upload MIME type, decoded image content, dimensions, and file size.
- [ ] Add rate limiting and cost controls for AI endpoints.
- [ ] Add caching only after measuring repeated requests and defining privacy behavior.
- [ ] Audit keyboard navigation, focus visibility, labels, reduced motion, and touch targets.
- [ ] Test the complete Definition of Done journey on common desktop and mobile viewport sizes.
- [ ] Add privacy copy explaining local storage and image handling.
- [ ] Add error monitoring without recording concepts or image data by default.

**Phase 5 exit criteria:** all Definition of Done items and quality gates are verified in a production-like environment.

## Persistence after useful v1

Cloud persistence is the next milestone, not a prerequisite for validating the local-first product.

When users need cross-device access:

- [ ] Add PostgreSQL-backed users, palettes, palette versions, and optional source-image records.
- [ ] Add managed authentication rather than implementing password storage.
- [ ] Keep anonymous local use available.
- [ ] Offer an explicit local-to-cloud import after sign-in.
- [ ] Create a new version on sync conflict instead of silently overwriting.
- [ ] Add read-only share links with revocation.
- [ ] Define account export and deletion behavior before launch.

Suggested backend resources:

```text
users
palettes
palette_versions
source_images (optional, explicit retention only)
```

Palette version snapshots may use JSON initially. Normalize color records only when real query requirements justify the added complexity.

## Deferred until after useful v1

These ideas may be valuable later but currently dilute the core outcome:

- Custom AI model training
- Social feeds, trending palettes, and public showcases
- Native mobile and desktop applications
- Browser extensions
- Figma or Adobe plugins
- Team and enterprise collaboration
- Batch processing
- Embed codes
- Advanced analytics and A/B testing
- ASE, GPL, and other specialist formats
- Redis or complex infrastructure without measured need

## Working rules

- Prefer finishing the end-to-end user journey over adding another generator.
- Fix mismatches and broken foundations before building on them.
- Every feature must include failure, empty, loading, and recovery behavior.
- Persist user intent—roles, locks, order, concept, and history—not just HEX values.
- Do not mark an item complete because code exists; verify its user-visible acceptance criteria.
- Keep pull requests aligned to one phase outcome where practical.
- Review this roadmap after completing each phase, not on arbitrary calendar dates.

## Immediate next actions

1. Complete Phase 0 and record exact verification commands in the README.
2. Define the canonical `SavedPalette` schema and repository interface.
3. Implement local autosave and reload recovery.
4. Add the palette library before cloud accounts.
5. Continue through the phases until every useful v1 Definition of Done item is verified.
