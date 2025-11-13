# main.py
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Routers from your controllers (preserve your naming)
from controller.authController import router as auth_router
from controller.userController import router as users_router
from controller.ticketController import router as ticket_router
from controller.paymentController import router as payment_router

# database Base/engine
from database import Base, engine, DB_FILE

# --- Lifespan: import models then create tables ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Import model modules here so SQLAlchemy sees all declarative classes
    before calling Base.metadata.create_all(...). Import modules (not names)
    to avoid triggering circular name-resolution problems.
    """
    # import model modules (these register models with Base)
    import models.userModel
    import models.paymentModel
    import models.ticketModel

    # create tables (idempotent)
    Base.metadata.create_all(bind=engine)

    # yield to start the app
    yield

# --- App setup ---
app = FastAPI(lifespan=lifespan)

# CORS setup: support an env var "CORS_ORIGINS" containing comma-separated origins,
# otherwise default to allowing all origins (useful during development).
cors_env = os.getenv("CORS_ORIGINS", "")
if cors_env:
    origins = [o.strip() for o in cors_env.split(",") if o.strip()]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(ticket_router, prefix="/tickets", tags=["tickets"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(payment_router, prefix="/payments", tags=["payments"])

# --- Simple health endpoint ---
@app.get("/", tags=["root"])
async def root():
    return {"status": "ok", "db_file": DB_FILE}
