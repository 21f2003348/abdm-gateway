# Database Integration Guide

## Overview
The ABDM Gateway has been successfully integrated with SQLite database using SQLAlchemy ORM. All in-memory data storage has been replaced with persistent database storage.

## Database Structure

### Tables Created:
1. **clients** - Client credentials for authentication
2. **bridges** - Bridge entities (HIP/HIU)
3. **bridge_services** - Services associated with bridges
4. **link_tokens** - Link tokens for patient linking
5. **link_transactions** - Link transactions for care context linking
6. **consents** - Consent requests and artefacts
7. **health_data** - Health information data transfers
8. **data_requests** - Health information data requests

## Installation Steps

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This will install SQLAlchemy along with other dependencies.

2. **Database Initialization**:
   The database is automatically initialized when you start the application. The database file `abdm_gateway.db` will be created in the project root directory.

3. **Start the Application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Database Location
- **File**: `abdm_gateway.db` (SQLite database file in project root)
- **Connection**: Automatically handled by SQLAlchemy

## Initial Data
When running in `local` environment, a default test client is automatically created:
- **Client ID**: `test_client`
- **Client Secret**: `test_secret`

You can use these credentials to test authentication endpoints.

## Manual Database Initialization
If you need to manually initialize the database:

```python
from app.db.init_db import init_db, seed_initial_data
from app.db.database import SessionLocal

# Initialize tables
init_db()

# Seed initial data (optional)
db = SessionLocal()
try:
    seed_initial_data(db)
finally:
    db.close()
```

Or run:
```bash
python -m app.db.init_db
```

## Database Models

All models are defined in `app/db/models.py`:
- `Client` - Authentication clients
- `Bridge` - Bridge entities
- `BridgeService` - Bridge services
- `LinkToken` - Patient linking tokens
- `LinkTransaction` - Link transactions
- `Consent` - Consent requests
- `HealthData` - Health data transfers
- `DataRequest` - Data requests

## Changes Made

### Services Updated:
- ✅ `auth_service.py` - Now uses database for client validation
- ✅ `bridge_service.py` - Bridges and services stored in database
- ✅ `linking_service.py` - Link tokens and transactions in database
- ✅ `consent_service.py` - Consents stored in database
- ✅ `data_service.py` - Health data and requests in database

### Routes Updated:
All route handlers now accept `db: Session = Depends(get_db)` parameter for database access.

### Main Application:
- Database initialization on startup
- Automatic table creation
- Optional seed data for local environment

## Testing the Integration

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Test authentication** (using default test client):
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/auth/session" \
     -H "Content-Type: application/json" \
     -H "X-CM-ID: sbx" \
     -d '{
       "clientId": "test_client",
       "clientSecret": "test_secret",
       "grantType": "client_credentials"
     }'
   ```

3. **Check database**:
   You can use SQLite tools or Python to inspect the database:
   ```python
   from app.db.database import SessionLocal
   from app.db.models import Client
   
   db = SessionLocal()
   clients = db.query(Client).all()
   print([c.client_id for c in clients])
   db.close()
   ```

## Next Steps

1. **Add more clients**: Create additional client credentials in the database
2. **Database migrations**: Consider using Alembic for database migrations in production
3. **Backup strategy**: Implement regular backups for the SQLite database
4. **Production database**: For production, consider migrating to PostgreSQL or MySQL

## Notes

- The database file (`abdm_gateway.db`) is created automatically
- All data persists between application restarts
- The database schema is version-controlled through SQLAlchemy models
- For production, consider using a more robust database like PostgreSQL

