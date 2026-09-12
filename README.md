# Lab Test Record Tracker

A small full-stack demo built to practice the exact stack in the **UL Solutions (Suzhou) Software Engineer** JD:
**Python (FastAPI) + Vue 3 / TypeScript + Docker + Azure + Azure DevOps**, themed on laboratory test-record management.

> Note: this is a personal portfolio / learning project, not employment work. It exists to demonstrate the JD's tech stack end-to-end.

## Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite, Pydantic v2
- **Frontend**: Vue 3 + TypeScript + Vite
- **Container**: multi-stage Docker (Node build → Python serves static)
- **Cloud**: Azure App Service / Railway (cloud deployment via CI/CD)
- **CI/CD**: Azure DevOps Pipelines + GitHub Actions

## Run locally (dev)
Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Frontend (separate terminal):
```bash
cd frontend
npm install
npm run dev          # http://localhost:5173 (proxies /api -> :8000)
```
API docs: http://localhost:8000/docs

## Run as a single container
```bash
docker compose up --build
# open http://localhost:8000
```

## Deploy to Azure
**Option A — manual CLI** (see `deploy-azure.sh`):
```bash
bash deploy-azure.sh
```
**Option B — Azure DevOps Pipelines** (`azure-pipelines.yml`):
1. Create an ACR + service connection `UL-Azure-ACR` and a subscription connection `UL-Azure-Conn` in Azure DevOps.
2. Adjust the resource names in the pipeline to match your subscription.
3. Push to `main` → image built, pushed to ACR, deployed to App Service.

**Option C — Railway + GitHub Actions** (no foreign card needed):
1. Push the repo to GitHub, create a Railway project, link it, and store a Railway project token as the `RAILWAY_TOKEN` secret.
2. `git push` to `main` triggers `.github/workflows/deploy.yml` → auto build + deploy.
3. Full step-by-step in **[DEPLOY_CLOUD.md](./DEPLOY_CLOUD.md)**.

## API
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/health | health check |
| GET | /api/records | list (query: `skip`,`limit`,`status`,`keyword`) |
| GET | /api/records/count | total count |
| POST | /api/records | create a record |
| PUT | /api/records/{id} | update a record |
| DELETE | /api/records/{id} | delete a record |
| POST | /api/seed?n=5000 | bulk-generate mock rows (demo large dataset) |

## Mapping to the UL JD
| JD requirement | Covered by |
|---|---|
| Python backend (Django/Flask/FastAPI) | FastAPI backend |
| Modern JS framework (Vue/React/Angular) | Vue 3 + TypeScript |
| TypeScript | frontend + tsconfig |
| Docker containers | multi-stage `Dockerfile` |
| Cloud (Azure/AWS) | Azure App Service / Railway cloud deploy |
| Azure DevOps / Agile | `azure-pipelines.yml` + `github/workflows/deploy.yml` + repo |
| Cross-functional / lab domain | lab test-record domain model |

## Notes
- SQLite keeps it zero-config; swap `SQLITE_DB` / the engine for Postgres in production.
- The "Seed 5,000 rows" button demonstrates server-side pagination for large lab datasets.

## Debug in Cursor / VS Code
项目已附带 `.vscode/launch.json` 与 `.vscode/tasks.json`，可直接断点调试（基于 VS Code 内核，Cursor 同样适用）：

- **后端（Python / FastAPI）**：把解释器选为 `lab-test-tracker/.venv`，按 `F5` 选 `Python: Uvicorn (Backend)`；在 `backend/app/crud.py` 等文件行号左侧打断点，访问 `http://localhost:8000/api/records` 即会命中。
- **前端（Vue 3）**：按 `F5` 选 `Frontend: Chrome (5173)`，会自动启动 Vite dev server 并在 Chrome 打开 `http://localhost:5173`，在 `.vue` 文件打断点可命中（依赖 source map）。
- **全栈一起**：按 `F5` 选 `Full Stack (Backend + Frontend)` 同时启动前后端。

> 调试态用本地 venv + `uvicorn --reload`，与 `docker compose up` 的容器演示态互不冲突；开发迭代用前者，演示验证用后者。
