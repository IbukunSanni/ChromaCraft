# ChromaCraft

ChromaCraft turns visual or written inspiration into editable color palettes. A user can generate a palette from an image, a natural-language concept, or a color-harmony rule, then copy colors and lock selected colors while exploring alternatives.

The product direction is to grow this into a persistent color-system workspace where palettes can be refined, checked for accessibility, saved, versioned, and exported as implementation-ready design tokens. See [TODO.md](./TODO.md) for the Definition of Done and ordered execution plan.

## Current capabilities

- Extract dominant colors from an uploaded image
- Generate a palette from a text concept using OpenAI
- Transform an extracted palette toward another concept
- Generate random, complementary, triadic, and analogous palettes
- Lock colors during regeneration
- Display human-friendly color names
- Copy HEX values
- Switch between light and dark themes
- Generate a basic PNG palette

Features described in the roadmap—including durable palette storage, manual color editing, reordering, undo/redo, semantic roles, contrast validation, and additional exports—are not complete yet.

## Architecture

```text
Browser
   │
   ▼
Next.js frontend
frontend/
   │ HTTPS
   ▼
FastAPI backend
backend/
   │
   └── OpenAI API
```

The frontend is a Next.js 15 application using React 19, TypeScript, and Tailwind CSS. The backend is a FastAPI application that contains the image-processing, harmony-generation, color-naming, concept-adjustment, and OpenAI integration.

The intended production arrangement is:

- **Vercel:** `frontend/`
- **Railway:** `backend/`
- **PostgreSQL:** add later when cloud accounts and cross-device synchronization are implemented
- **IndexedDB:** planned first persistence layer for anonymous, local-first use

## Repository structure

```text
ChromaCraft/
├── frontend/
│   ├── app/                # Next.js App Router
│   ├── components/         # Palette, upload, concept, and theme UI
│   ├── contexts/           # Shared React context
│   ├── lib/                # API client, types, constants, and errors
│   ├── utils/              # Frontend color utilities
│   └── __tests__/          # Jest and Testing Library tests
├── backend/
│   ├── routes/             # FastAPI HTTP routes
│   ├── services/           # Application-level palette operations
│   ├── utils/              # Image, AI, naming, export, and harmony utilities
│   ├── constants/          # Backend constants and error definitions
│   └── tests/              # Pytest suites
├── package.json            # Workspace scripts
├── pnpm-workspace.yaml
├── .env.example
└── TODO.md
```

## Local development

### Requirements

- Node.js 18 or newer
- pnpm 8 or newer
- Python 3.12 recommended
- An OpenAI API key for AI generation

### Install the frontend

```bash
corepack enable
pnpm install
```

### Install the backend

Create and activate a virtual environment, then install the Python dependencies.

PowerShell:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

macOS/Linux:

```bash
python -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

### Configure the environment

Copy `.env.example` to `.env` and set:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
MAX_REQUESTS_PER_MINUTE=60
```

`OPENAI_API_KEY` is only needed for `/generate/concept`. Without it the API still starts; that endpoint returns `503` and every other feature keeps working.

Optional CORS settings (defaults shown):

```env
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://color-palette-extractor.vercel.app
ALLOWED_ORIGIN_REGEX=https://color-palette-extractor(-[a-z0-9-]+)?\.vercel\.app
```

Never commit `.env` or expose `OPENAI_API_KEY` through a `NEXT_PUBLIC_*` variable.

### Run both applications

```bash
pnpm run dev
```

Or run them separately:

```bash
pnpm run dev:frontend
pnpm run dev:backend
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- FastAPI documentation: `http://localhost:8000/docs`

## Validation commands

```bash
pnpm run build
pnpm run test:frontend
pnpm run test:backend
```

Run the backend tests with the backend virtual environment active. Verified on November 13, 2026 (Windows 11, Python 3.12, Node 22):

- `pnpm run build` (Next.js 15.5.29 production build): passes
- `pnpm run test:frontend`: 5 suites, 63 tests pass
- `pnpm run test:backend`: 59 tests pass in about 2 seconds
- `pnpm run lint:frontend`: no warnings or errors (the backend has no linter configured yet)

The first `/adjust-concept` request loads the sentence-transformer model, so it takes about 15 seconds; later requests are fast. `backend/demos/api_smoke_check.py` is a manual script that calls a running server on port 8000; it is not part of the pytest suite.

## Deployment

### Vercel frontend

Create a Vercel project from this repository with:

| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Framework Preset | Next.js |
| Install Command | `pnpm install` |
| Build Command | `pnpm build` |
| Production Branch | `main` |

Set this Vercel environment variable after Railway provides the public backend URL:

```env
NEXT_PUBLIC_API_URL=https://your-api.up.railway.app
```

Apply the variable to Production and Preview as appropriate, then redeploy. Without it, the production browser falls back to `http://localhost:8000` and cannot reach the deployed API.

### Railway backend

Create a Railway service from the same repository with:

| Setting | Value |
|---|---|
| Root Directory | `backend` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health-check Path | `/` |

`backend/Procfile` declares the same start command and `backend/.python-version` pins Python 3.12, so the builder can detect both from the `backend` root directory.

Set:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
MAX_REQUESTS_PER_MINUTE=60
```

Generate a public Railway domain for the service and use that URL as Vercel's `NEXT_PUBLIC_API_URL`.

The existing `backend/render.yaml` is a Render configuration file. Railway and Vercel do not use it.

### Cross-origin requests

CORS origins come from `ALLOWED_ORIGINS` (exact origins) and `ALLOWED_ORIGIN_REGEX` (default: this project's Vercel production and preview domains, `color-palette-extractor[-…].vercel.app`). If the production frontend uses a custom domain, add it to `ALLOWED_ORIGINS` in Railway.

## Deployment status

On July 28, 2026, commit `8f9c4ad` failed on both providers:

- **Vercel** rejected the build because `next@15.2.4` is affected by CVE-2025-66478.
- **Railway** could not start the API, because `main:app` failed to import.

Fixed in the repository on November 13, 2026:

1. `backend/models/` (the Pydantic request/response models) had been excluded by a broad `models/` rule in `.gitignore`. It is now tracked.
2. The color-name loader now reads the XKCD dataset's current JSON shape. Before this, it crashed on import.
3. The OpenAI client and the sentence-transformer model now load on first use. The API starts in about a second, without an OpenAI key and without loading `torch`.
4. Next.js is upgraded to the patched `15.5.29`, and the stale npm `frontend/package-lock.json` is removed. `pnpm-lock.yaml` is the only lockfile.
5. The CORS wildcard is replaced by an origin list and regex set through environment variables.
6. Console output no longer crashes on Windows when stdout is redirected (for example under `pnpm run dev`).

Still to confirm in the provider dashboards:

- Railway: Root Directory `backend`, `OPENAI_API_KEY` set, a public domain generated, and `/` reachable.
- Vercel: `NEXT_PUBLIC_API_URL` set to the Railway domain for Production (and Preview if wanted), then redeploy.
- The `torch` and `sentence-transformers` dependencies make the Railway image large. See the roadmap for the plan to remove them.

## API surface currently implemented

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/mem` | Development memory information |
| `POST` | `/generate/random` | Generate a harmony-based palette |
| `POST` | `/generate/concept` | Generate a concept-based AI palette |
| `POST` | `/extract-colors` | Extract colors from an image |
| `POST` | `/adjust-concept` | Transform a palette toward a concept |
| `POST` | `/export-png` | Generate a PNG palette |

Request and response field names are snake_case and match `backend/models/`. `frontend/lib/api-client.ts` only declares methods for the routes above. `/generate/random` returns locked colors first, and the frontend puts them back at the positions where they were locked (`frontend/lib/palette-locks.ts`).

## Product direction

The useful-v1 goal is not simply to produce five colors. It is to let a user create, refine, validate, save, recover, version, manage, and export an implementation-ready color system without requiring an account.

The complete scope, acceptance criteria, deferred features, and working rules are maintained in [TODO.md](./TODO.md).

## Contributing

1. Create a focused branch from `main`.
2. Keep changes aligned to one roadmap phase outcome.
3. Add or update tests for changed behavior.
4. Run the relevant validation commands.
5. Open a pull request that explains the user impact and verification performed.

## Acknowledgements

- OpenAI
- FastAPI
- Next.js
- Pillow and ColorThief
- XKCD Color Survey
