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

The repository is currently in Phase 0 of the roadmap. These commands are the target quality gate, but the backend is not yet expected to pass because the missing request/response model module must be restored.

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

Set:

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
MAX_REQUESTS_PER_MINUTE=60
```

Generate a public Railway domain for the service and use that URL as Vercel's `NEXT_PUBLIC_API_URL`.

The existing `backend/render.yaml` is a Render configuration file. Railway and Vercel do not use it.

### Cross-origin requests

The FastAPI CORS configuration must explicitly allow the production Vercel domain. A string such as `https://*.vercel.app` in `allow_origins` is not a wildcard match. Use an explicit canonical origin and, if preview deployments are required, a constrained `allow_origin_regex`.

## Confirmed deployment status

The latest checked commit, `8f9c4ad`, failed on both providers on July 28, 2026.

### Vercel: confirmed failure

The Vercel build compiled the frontend, passed type checking, and generated all static pages. Vercel then rejected the deployment because the project uses `next@15.2.4`, a version affected by CVE-2025-66478.

Vercel blocks new deployments of affected Next.js versions. The correct fix is to upgrade Next.js and its lockfile to a currently supported patched release, run the frontend tests and production build, and redeploy. Do not bypass the protection with `DANGEROUSLY_DEPLOY_VULNERABLE_CVE_2025_66478`.

### Railway: deployment failure confirmed; application blockers identified

GitHub reports the latest Railway deployment as failed. Provider logs were not available in the current development session, but the repository contains deployment-blocking backend problems:

1. `backend/routes/palettes.py` and `backend/routes/colors.py` import a `models` module that does not exist in the repository.
2. Railway must use `backend` as its root directory; there is no Railway configuration at the repository root to guarantee this automatically.
3. The service must bind to Railway's injected `$PORT`, not the hard-coded port in `backend/render.yaml`.
4. The Python dependency set includes large ML packages such as `torch` and `sentence-transformers`, which significantly increase build time and image size. They should remain only if the current concept-adjustment implementation truly requires them.

Even after a successful dependency installation, the missing `models` module prevents `main:app` from importing, so the API cannot start.

### Deployment recovery order

1. Restore the backend Pydantic request and response models.
2. Confirm `python -c "import main"` succeeds from `backend/`.
3. Configure Railway's root directory, start command, variables, and public domain.
4. Upgrade Next.js from the vulnerable release and update `pnpm-lock.yaml`.
5. Run backend tests, frontend tests, and the frontend production build.
6. Set `NEXT_PUBLIC_API_URL` in Vercel to the Railway domain.
7. Add the Vercel production origin to FastAPI CORS.
8. Deploy Railway first, verify `/`, then deploy Vercel and exercise every user workflow.

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

Some methods declared in `frontend/lib/api-client.ts`, including accessibility validation and JSON/ASE export, do not yet have matching backend routes.

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
