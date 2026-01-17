from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
import sqlite3

settings = get_settings()

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./abdm_gateway.db"


# Create engine with better SQLite configuration for concurrent access
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
)

# Enable WAL mode for better concurrency (Write-Ahead Logging)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set SQLite pragmas for better performance and concurrency"""
    try:
        cursor = dbapi_conn.cursor()
        # Try to enable WAL mode (may fail if database is locked, that's OK)
        try:
            cursor.execute("PRAGMA journal_mode=WAL")
        except sqlite3.OperationalError:
            # WAL mode may already be enabled or database locked, continue anyway
            pass
        # Enable foreign keys
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        except sqlite3.OperationalError:
            pass
        # Set busy timeout (wait up to 20 seconds for lock to be released)
        try:
            cursor.execute("PRAGMA busy_timeout=20000")
        except sqlite3.OperationalError:
            pass
        cursor.close()
    except Exception:
        # If setting pragmas fails, continue anyway - connection will still work
        pass

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

