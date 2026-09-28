from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.tasks import router as tasks_router
from backend.app.api.v1.categories import router as categories_router
from backend.app.db.session import engine
from backend.app.db.session import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when Uvicorn starts up and automatically creates tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Code here runs when the application shuts down
    
    
app = FastAPI(title="Multi-User ToDo API", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}

