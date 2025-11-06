# main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from controller.userController import router as users_router
from controller.ticketController import router  as ticket_router # Import the ticket router
from database import Base, engine, DB_FILE  # optional DB_FILE if you check path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # import models here so SQLAlchemy registers tables (avoid circular import)
    import models

    # synchronous call inside async context is fine for this small setup
    Base.metadata.create_all(bind=engine)

    yield
    # teardown (if any) goes here

app = FastAPI(lifespan=lifespan)

# --- CORS config (your existing logic) ---
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
if isinstance(CORS_ORIGINS, str) and "," in CORS_ORIGINS:
    origins = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]
elif CORS_ORIGINS == "*" or not CORS_ORIGINS:
    origins = ["*"]
else:
    origins = [CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(ticket_router, prefix="/tickets", tags=["tickets"])  # Include ticket router