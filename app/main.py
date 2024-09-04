from fastapi import FastAPI
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
