# Deploy to the Cloud via CI/CD (Railway + GitHub Actions)

This project was originally written for **Azure** (`deploy-azure.sh` + `azure-pipelines.yml`).
That path works, but the Azure **global** account requires a foreign-currency credit card,
which is a blocker for many China-based developers. This document covers the **equivalent
Railway path**, which only needs a GitHub login (no foreign card) and still demonstrates
the exact skills the UL JD asks for: **Cloud + Docker + automated CI/CD**.

> Platform is different, the pipeline shape is identical: `push` → auto `docker build`
> → auto deploy → public URL. UL uses Azure DevOps + Azure; Railway uses GitHub Actions
> + Railway. Same three stages, same story in an interview.

## What you must do manually (cannot be automated)

| # | Action | Why |
|---|--------|-----|
| 1 | Create a **GitHub** repo and `git push` this folder | Source of truth for the pipeline |
| 2 | Create a **Railway** account (log in with GitHub) | The cloud host |
| 3 | In Railway, create a **project** and link the GitHub repo (or deploy from the repo) | Tells Railway what to build |
| 4 | In Railway project **Settings → Tokens**, generate a **project token**, then store it in the GitHub repo as secret **`RAILWAY_TOKEN`** | Lets GitHub Actions authenticate to Railway |

## Step-by-step

### Step 1 — Push the code to GitHub
```bash
cd "/Users/hanglin/Documents/我的/简历/UL/lab-test-tracker"
git init
git add .
git commit -m "lab-test-tracker: FastAPI+Vue demo with Railway CI/CD"
git branch -M main
git remote add origin https://github.com/<you>/lab-test-tracker.git
git push -u origin main
```
> `.gitignore` already excludes `.venv/` and `node_modules`, so the venv is NOT pushed.

### Step 2 — Create the Railway project
1. Go to https://railway.app and **Log in with GitHub**.
2. **New Project → Deploy from GitHub repo** → pick this repo.
3. Railway auto-detects the `Dockerfile` and builds the image.
4. Once deployed, it gives you a public URL like `https://lab-test-tracker.up.railway.app`.

### Step 3 — Add the deploy token to GitHub Secrets
1. In the Railway project: **Settings → Tokens → New Token** (scope = this project).
2. Copy the token.
3. In the GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
   - Name: `RAILWAY_TOKEN`
   - Value: the token you copied.

### Step 4 — Trigger the pipeline
Push any change to `main` (or click **Run workflow** under the Actions tab). GitHub Actions
will:
1. `checkout` the code,
2. install the Railway CLI,
3. `railway up` → build the Docker image on Railway → deploy it.

Watch the **Actions** tab for a green check, then open the Railway-provided URL.

### Step 5 — Verify
- Open the public URL → you should see the lab record UI.
- Open `<url>/api/health` → returns `{"status":"ok"}`.
- Click **Seed** → rows appear → server-side pagination works end to end on the cloud.

## Mapping to the UL JD

| JD requirement | This project demonstrates |
|---|---|
| Python backend (Django/Flask/FastAPI) | FastAPI backend |
| Modern JS framework (Vue/React/Angular) | Vue 3 + TypeScript |
| TypeScript | frontend + tsconfig |
| Docker containers | multi-stage `Dockerfile` |
| **Cloud (Azure/AWS)** | deployed to a **cloud platform** (Railway here; Azure in `deploy-azure.sh`) |
| **Azure DevOps / Agile** | CI/CD pipeline (`github/workflows/deploy.yml`; also `azure-pipelines.yml`) |
| Cross-functional / lab domain | lab test-record domain model |

Interview line:
> "I deployed this through a CI/CD pipeline to a cloud platform — push to `main` auto-builds
> the Docker image and deploys it. UL uses Azure DevOps + Azure; I also have that config
> (`azure-pipelines.yml`), but for this demo I used Railway because it needs only a GitHub
> login. The pipeline shape — build, push image, auto-deploy — is the same."

## Notes / gotchas
- **Port**: the `Dockerfile` `CMD` now listens on `${PORT:-8000}` so Railway's injected
  `PORT` is honored; local `docker compose` still uses 8000.
- **SQLite persistence**: the container filesystem is ephemeral on Railway. The DB lives at
  `/data/labtracker.db` (same `SQLITE_DB` var as `docker-compose`). For a lasting demo,
  attach a Railway **Volume** mounted at `/data` in project settings; otherwise re-run Seed
  after a restart. This is fine for a portfolio demo.
- **Free tier**: Railway free tier may sleep/idle; hit the URL once before a demo to wake it.
- **Azure alternative**: `deploy-azure.sh` + `azure-pipelines.yml` remain in the repo and
  are kept on purpose, so you can show you know the Azure DevOps syntax too.
