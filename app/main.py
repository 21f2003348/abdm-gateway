from fastapi import FastAPI 
from loguru import logger 

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.routes import api_router
from app.db.init_db import init_db, seed_initial_data
from app.db.database import SessionLocal

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="ABDM Gateway",
    description="API Gateway for ABDM services",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to ABDM Gateway API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "api": "/api"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "abdm-gateway"}

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting ADBM Gateway on {settings.app_host}:{settings.app_port}")
    logger.info(f"Environment: {settings.app_env}")
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Seed initial data (optional - for development)
    if settings.app_env == "local":
        db = SessionLocal()
        try:
            seed_initial_data(db)
        finally:
            db.close()
    
    logger.info("Database initialization complete!")

@app.on_event("shutdown")
async def stutdown_event():
    logger.info("Setting down ABDM Gateway")

@app.get("/hello")
async def hello():
    return {"message": "Hello, ABDM Gateway!"}
