from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db, engine, Base
from .seed import seed_if_empty

Base.metadata.create_all(bind=engine)

# Frontend build output (populated in production / Docker image)
# main.py lives at <root>/backend/app/main.py -> three dirnames up = project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIST = os.path.join(PROJECT_ROOT, "frontend", "dist")


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_if_empty()
    yield


app = FastAPI(title="Lab Test Record Tracker", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/records", response_model=list[schemas.TestRecordOut])
def list_records(
    skip: int = 0,
    limit: int = 50,
    status: str = None,
    keyword: str = None,
    db: Session = Depends(get_db),
):
    return crud.get_records(db, skip, limit, status, keyword)


@app.get("/api/records/count")
def count(status: str = None, keyword: str = None, db: Session = Depends(get_db)):
    return {"total": crud.count_records(db, status, keyword)}


@app.post("/api/records", response_model=schemas.TestRecordOut, status_code=201)
def create(rec: schemas.TestRecordCreate, db: Session = Depends(get_db)):
    return crud.create_record(db, rec)


@app.put("/api/records/{record_id}", response_model=schemas.TestRecordOut)
def update(record_id: int, rec: schemas.TestRecordUpdate, db: Session = Depends(get_db)):
    r = crud.update_record(db, record_id, rec)
    if not r:
        raise HTTPException(404, "record not found")
    return r


@app.delete("/api/records/{record_id}")
def delete(record_id: int, db: Session = Depends(get_db)):
    if not crud.delete_record(db, record_id):
        raise HTTPException(404, "record not found")
    return {"ok": True}


@app.post("/api/seed")
def seed(n: int = 1000, db: Session = Depends(get_db)):
    return {"inserted": crud.bulk_create(db, n)}


# Serve the built SPA if present (single-container production mode)
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="spa")
else:

    @app.get("/")
    def root():
        return {
            "message": "API only. Frontend not built. Run `npm run build` in frontend/.",
            "docs": "/docs",
        }
