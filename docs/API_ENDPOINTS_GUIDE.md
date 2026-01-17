# ABDM Gateway - API Endpoints Guide

## Base URL
```
http://127.0.0.1:8000
```

## Quick Access Links

### 📚 Interactive API Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### 🏠 Basic Endpoints
- **Root**: http://127.0.0.1:8000/
- **Health Check**: http://127.0.0.1:8000/health
- **Hello**: http://127.0.0.1:8000/hello

---

## API Endpoints

### 🔐 Authentication (`/api/auth`)

#### 1. Create Session (Get Access Token)
**POST** `/api/auth/session`

**Headers:**
```
Content-Type: application/json
REQUEST-ID: <uuid>
TIMESTAMP: <iso-timestamp>
X-CM-ID: sbx
```

**Request Body:**
```json
{
  "clientId": "test_client",
  "clientSecret": "test_secret",
  "grantType": "client_credentials"
}
```

**Response:**
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expiresIn": 900,
  "tokenType": "Bearer"
}
```

#### 2. Get Certificates
**GET** `/api/auth/certs`

**Response:**
```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "demo-key-1",
      "alg": "RS256",
      "n": "placeholder",
      "e": "AQAB"
    }
  ]
}
```

---

### 🌉 Bridge Management (`/api/bridge`)

**Required Headers for all Bridge endpoints:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
REQUEST-ID: <uuid>
TIMESTAMP: <iso-timestamp>
X-CM-ID: sbx
```

#### 1. Register Bridge
**POST** `/api/bridge/register`

**Request Body:**
```json
{
  "bridgeId": "bridge-001",
  "entityType": "HIP",
  "name": "Hospital Name"
}
```

**Response:**
```json
{
  "bridgeId": "bridge-001",
  "entityType": "HIP",
  "name": "Hospital Name"
}
```

#### 2. Update Bridge Webhook URL
**PATCH** `/api/bridge/url`

**Request Body:**
```json
{
  "bridgeId": "bridge-001",
  "webhookUrl": "https://example.com/webhook"
}
```

#### 3. List Bridge Services
**GET** `/api/bridge/{bridge_id}/services`

**Response:**
```json
[
  {
    "id": "bridge-001-svc-1",
    "name": "Service-1",
    "active": true,
    "version": "v1"
  }
]
```

#### 4. Get Service by ID
**GET** `/api/bridge/service/{service_id}`

---

### 🔗 Patient Linking (`/api/link`)

**Required Headers for all Link endpoints:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
REQUEST-ID: <uuid>
TIMESTAMP: <iso-timestamp>
X-CM-ID: sbx
```

#### 1. Generate Link Token
**POST** `/api/link/token/generate`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "hipId": "hip-001"
}
```

**Response:**
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "expiresIn": 300
}
```

#### 2. Link Care Contexts
**POST** `/api/link/carecontext`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "careContexts": [
    {
      "id": "cc-001",
      "referenceNumber": "ref-001"
    }
  ]
}
```

#### 3. Discover Patient
**POST** `/api/link/discover`

**Request Body:**
```json
{
  "mobile": "9876543210",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "patientId": "pat-9876543210",
  "status": "FOUND"
}
```

#### 4. Initialize Link
**POST** `/api/link/init`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "txnId": "txn-001"
}
```

#### 5. Confirm Link
**POST** `/api/link/confirm`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "txnId": "txn-001",
  "otp": "123456"
}
```

#### 6. Notify Link Status
**POST** `/api/link/notify`

**Request Body:**
```json
{
  "txnId": "txn-001",
  "status": "CONFIRMED"
}
```

---

### ✅ Consent Management (`/api/consent`)

**Required Headers for all Consent endpoints:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
REQUEST-ID: <uuid>
TIMESTAMP: <iso-timestamp>
X-CM-ID: sbx
```

#### 1. Initialize Consent
**POST** `/api/consent/init`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "hipId": "hip-001",
  "purpose": {
    "code": "TREATMENT",
    "text": "Treatment purpose"
  }
}
```

**Response:**
```json
{
  "consentRequestId": "consent-001",
  "status": "REQUESTED"
}
```

#### 2. Get Consent Status
**GET** `/api/consent/status/{consentRequestId}`

**Response:**
```json
{
  "consentRequestId": "consent-001",
  "status": "REQUESTED",
  "grantedAt": null
}
```

#### 3. Fetch Consent
**POST** `/api/consent/fetch`

**Request Body:**
```json
{
  "consentRequestId": "consent-001"
}
```

#### 4. Notify Consent Status
**POST** `/api/consent/notify`

**Request Body:**
```json
{
  "consentRequestId": "consent-001",
  "status": "GRANTED"
}
```

---

### 📊 Health Data Transfer (`/api/data`)

**Required Headers for all Data endpoints:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
REQUEST-ID: <uuid>
TIMESTAMP: <iso-timestamp>
X-CM-ID: sbx
```

#### 1. Send Health Information
**POST** `/api/data/health-info`

**Request Body:**
```json
{
  "txnId": "txn-001",
  "patientId": "pat-12345",
  "hipId": "hip-001",
  "careContextId": "cc-001",
  "healthInfo": {
    "encryptedData": "encrypted_data_here",
    "keyMaterial": "key_material_here"
  },
  "metadata": {
    "type": "DiagnosticReport",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

#### 2. Request Health Information
**POST** `/api/data/request-info`

**Request Body:**
```json
{
  "patientId": "pat-12345",
  "hipId": "hip-001",
  "careContextId": "cc-001",
  "dataTypes": ["DiagnosticReport", "Prescription"]
}
```

**Response:**
```json
{
  "requestId": "req-001",
  "status": "REQUESTED"
}
```

#### 3. Get Request Status
**GET** `/api/data/request/{request_id}`

#### 4. Notify Data Flow
**POST** `/api/data/notify`

**Request Body:**
```json
{
  "txnId": "txn-001",
  "status": "PROCESSED",
  "hipId": "hip-001"
}
```

---

## Testing with cURL

### 1. Get Access Token
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/session" \
  -H "Content-Type: application/json" \
  -H "REQUEST-ID: $(uuidgen)" \
  -H "TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -H "X-CM-ID: sbx" \
  -d '{
    "clientId": "test_client",
    "clientSecret": "test_secret",
    "grantType": "client_credentials"
  }'
```

### 2. Register Bridge (using token from step 1)
```bash
curl -X POST "http://127.0.0.1:8000/api/bridge/register" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "REQUEST-ID: $(uuidgen)" \
  -H "TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -H "X-CM-ID: sbx" \
  -d '{
    "bridgeId": "bridge-001",
    "entityType": "HIP",
    "name": "Test Hospital"
  }'
```

---

## Testing with Python

```python
import requests
import uuid
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def get_headers(token=None):
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat(),
        "X-CM-ID": "sbx"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# 1. Get token
response = requests.post(
    f"{BASE_URL}/api/auth/session",
    headers=get_headers(),
    json={
        "clientId": "test_client",
        "clientSecret": "test_secret",
        "grantType": "client_credentials"
    }
)
token = response.json()["accessToken"]

# 2. Register bridge
response = requests.post(
    f"{BASE_URL}/api/bridge/register",
    headers=get_headers(token),
    json={
        "bridgeId": "bridge-001",
        "entityType": "HIP",
        "name": "Test Hospital"
    }
)
print(response.json())
```

---

## Testing with Browser

1. **Open Swagger UI**: http://127.0.0.1:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the required fields
5. Click "Execute"

**Note**: For authenticated endpoints, you'll need to:
1. First call `/api/auth/session` to get a token
2. Click "Authorize" button at top of Swagger UI
3. Enter: `Bearer <your_token>`
4. Then test other endpoints

---

## Default Test Credentials

- **Client ID**: `test_client`
- **Client Secret**: `test_secret`
- **CM ID**: `sbx`

---

## Database Verification

After making API calls, verify data is stored:

```bash
python check_database.py
```

This shows all records stored in the database.

---

## Next Steps

1. **Explore Swagger UI**: http://127.0.0.1:8000/docs
2. **Test endpoints**: Use the interactive documentation
3. **Check database**: Run `python check_database.py` to see stored data
4. **Add more clients**: Create additional client credentials in database
5. **Build your application**: Integrate these APIs into your frontend/client application

