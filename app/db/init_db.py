"""
Database initialization script
Creates all tables and optionally seeds initial data
"""
from app.db.database import engine, Base
from app.db.models import Client
from app.core.config import get_settings
from loguru import logger
from sqlalchemy.orm import Session

settings = get_settings()

def init_db():
    """Create all database tables"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

def seed_initial_data(db: Session):
    """Seed initial data (optional - for development/testing)"""
    # Check if any clients exist
    existing_client = db.query(Client).first()
    if existing_client:
        logger.info("Database already has data, skipping seed")
        return
    
    # Create a default client for testing
    default_client = Client(
        client_id="test_client",
        client_secret="test_secret",
        cm_id=settings.cm_id,
        is_active=True
    )
    db.add(default_client)
    db.commit()
    logger.info("Seeded initial test client: test_client / test_secret")

if __name__ == "__main__":
    init_db()
    logger.info("Database initialization complete!")

