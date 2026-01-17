# Testing Guide - Database Integration Verification

## Quick Test Methods

### Method 1: Automated Test Script (Recommended)

1. **Start your server** (in one terminal):
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Run the test script** (in another terminal):
   ```bash
   python test_database.py
   ```

   This will automatically test:
   - ✅ Root endpoint
   - ✅ Health check
   - ✅ Authentication (database lookup)
   - ✅ Bridge registration (database storage)
   - ✅ Link token generation (database storage)
   - ✅ Consent initiation (database storage)
   - ✅ Data request (database storage)
   - ✅ Database file existence

### Method 2: Check Database Contents Directly

Run this script to see what's stored in your database:
```bash
python check_database.py
```

This shows all records in all tables.

### Method 3: Manual Testing with Browser/Postman

#### Step 1: Check Basic Endpoints
- Open browser: `http://127.0.0.1:8000/`
- Should see welcome message
- Open: `http://127.0.0.1:8000/docs` - FastAPI interactive docs

#### Step 2: Test Authentication (Database)
**Endpoint:** `POST /api/auth/session`

**Request:**
```json
{
  "clientId": "test_client",
  "clientSecret": "test_secret",
  "grantType": "client_credentials"
}
```

**Headers:**
```
Content-Type: application/json
X-CM-ID: sbx
```

**Expected:** Should return access token (proves database lookup works)

#### Step 3: Test Bridge Registration (Database Storage)
**Endpoint:** `POST /api/bridge/register`

**Request:**
```json
{
  "bridgeId": "test-bridge-1",
  "entityType": "HIP",
  "name": "Test Hospital"
}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token_from_step_2>
X-CM-ID: sbx
```

**Expected:** Bridge created and stored in database

#### Step 4: Verify Data Persists
1. Stop the server (Ctrl+C)
2. Start it again
3. Check bridge still exists (use `check_database.py` or query again)

### Method 4: Using FastAPI Docs (Easiest)

1. Start server: `uvicorn app.main:app --reload`
2. Open browser: `http://127.0.0.1:8000/docs`
3. Test endpoints directly in the browser interface
4. Use the test client credentials:
   - Client ID: `test_client`
   - Client Secret: `test_secret`

## Verification Checklist

### ✅ Database File Created
- Check if `abdm_gateway.db` exists in project root
- File should be created automatically on first startup

### ✅ Database Tables Created
Run `check_database.py` to verify all tables exist and have proper structure.

### ✅ Authentication Works
- Test with valid credentials → Should succeed
- Test with invalid credentials → Should fail (401)
- This proves database lookup is working

### ✅ Data Persists
1. Create a bridge/consent/link token
2. Stop server
3. Start server again
4. Data should still be there (check with `check_database.py`)

### ✅ All Services Use Database
- Bridge registration → Stores in database
- Link token generation → Stores in database
- Consent creation → Stores in database
- Data requests → Stores in database

## Quick Commands

```bash
# Start server
uvicorn app.main:app --reload

# Run automated tests
python test_database.py

# Check database contents
python check_database.py

# Check database file size (should grow as you add data)
ls -lh abdm_gateway.db  # Linux/Mac
dir abdm_gateway.db     # Windows
```

## Expected Results

### ✅ Success Indicators:
- Database file `abdm_gateway.db` exists
- Server starts without errors
- Authentication returns access token
- Data persists after server restart
- All API endpoints work correctly
- `check_database.py` shows records in tables

### ❌ Failure Indicators:
- Database file not created
- Import errors on startup
- Authentication always fails
- Data lost after restart
- API returns 500 errors

## Troubleshooting

### If database file not created:
- Check server logs for errors
- Verify SQLAlchemy is installed: `pip install sqlalchemy`
- Check file permissions in project directory

### If authentication fails:
- Verify test client was seeded: Run `check_database.py`
- Check database file exists
- Look at server logs for SQL errors

### If data doesn't persist:
- Verify database file exists and is being written to
- Check server logs for database errors
- Ensure you're looking at the same database file

