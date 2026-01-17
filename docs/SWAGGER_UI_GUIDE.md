# Step-by-Step Guide: Using Swagger UI

## Step 1: Open Swagger UI

Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

You'll see the FastAPI interactive documentation with all available endpoints.

---

## Step 2: Get Access Token (Authentication)

### 2.1 Find the Authentication Endpoint
- Scroll down or look for **`POST /api/auth/session`**
- Click on it to expand

### 2.2 Click "Try it out"
- Click the blue **"Try it out"** button

### 2.3 Fill in the Request Body
Replace the default values with:
```json
{
  "clientId": "test_client",
  "clientSecret": "test_secret",
  "grantType": "client_credentials"
}
```

### 2.4 Add Required Headers
In the **Parameters** section, you'll see header fields. Fill them in:

- **REQUEST-ID**: Click "Add string item" or enter: `123e4567-e89b-12d3-a456-426614174000`
- **TIMESTAMP**: Enter current timestamp: `2024-01-16T18:15:52Z` (or use current time)
- **X-CM-ID**: Enter: `sbx`

### 2.5 Execute the Request
- Click the green **"Execute"** button at the bottom

### 2.6 Copy the Access Token
- You'll see a response like:
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expiresIn": 900,
  "tokenType": "Bearer"
}
```
- **Copy the `accessToken` value** (the long string starting with "eyJ...")

---

## Step 3: Authorize with the Token

### 3.1 Click the "Authorize" Button
- At the top right of the Swagger UI page, click the green **"Authorize"** button (🔒 icon)

### 3.2 Enter Your Token
- In the popup, you'll see a field for "Bearer"
- Enter: `Bearer <your_access_token>`
  - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
  - **Important**: Include the word "Bearer" followed by a space, then your token

### 3.3 Click "Authorize"
- Click the **"Authorize"** button in the popup
- Then click **"Close"**

Now all authenticated endpoints will automatically use this token!

---

## Step 4: Test Other Endpoints

Now you can test any endpoint. Here are some examples:

### 4.1 Register a Bridge
1. Find **`POST /api/bridge/register`**
2. Click **"Try it out"**
3. Fill in:
```json
{
  "bridgeId": "my-bridge-001",
  "entityType": "HIP",
  "name": "My Hospital"
}
```
4. Click **"Execute"**

### 4.2 Generate Link Token
1. Find **`POST /api/link/token/generate`**
2. Click **"Try it out"**
3. Fill in:
```json
{
  "patientId": "pat-12345",
  "hipId": "hip-001"
}
```
4. Click **"Execute"**

### 4.3 Initialize Consent
1. Find **`POST /api/consent/init`**
2. Click **"Try it out"**
3. Fill in:
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
4. Click **"Execute"**

### 4.4 Request Health Info
1. Find **`POST /api/data/request-info`**
2. Click **"Try it out"**
3. Fill in:
```json
{
  "patientId": "pat-12345",
  "hipId": "hip-001",
  "careContextId": "cc-001",
  "dataTypes": ["DiagnosticReport", "Prescription"]
}
```
4. Click **"Execute"**

---

## Step 5: Verify Data in Database

After testing endpoints, verify the data was stored:

```bash
python check_database.py
```

This shows all records in your database.

---

## Quick Reference: Test Credentials

- **Client ID**: `test_client`
- **Client Secret**: `test_secret`
- **Grant Type**: `client_credentials`
- **CM ID**: `sbx`

---

## Tips

1. **Token Expires**: Access tokens expire after 900 seconds (15 minutes). If you get a 401 error, get a new token.

2. **Headers**: Some endpoints require headers. Swagger UI will show which ones are required.

3. **Response Codes**:
   - `200` = Success
   - `400` = Bad Request (check your input)
   - `401` = Unauthorized (get a new token)
   - `404` = Not Found

4. **View Response**: After clicking "Execute", scroll down to see:
   - **Response body** - The actual data returned
   - **Response code** - HTTP status code
   - **Response headers** - Additional information

---

## Troubleshooting

### "Invalid client credentials" error
- Make sure you're using:
  - `clientId`: `test_client`
  - `clientSecret`: `test_secret`
  - NOT "string" or placeholder values

### "Missing required headers" error
- Make sure you added:
  - REQUEST-ID
  - TIMESTAMP
  - X-CM-ID

### "Unauthorized" error on authenticated endpoints
- Make sure you:
  1. Got a token from `/api/auth/session`
  2. Clicked "Authorize" button
  3. Entered: `Bearer <your_token>`
  4. Token hasn't expired (get a new one if needed)

### Can't see endpoints
- Make sure your server is running:
  ```bash
  uvicorn app.main:app --reload
  ```

---

## Summary Checklist

- [ ] Open http://127.0.0.1:8000/docs
- [ ] Test `/api/auth/session` to get token
- [ ] Copy the access token
- [ ] Click "Authorize" button
- [ ] Enter `Bearer <token>`
- [ ] Test other endpoints
- [ ] Verify data with `python check_database.py`

Happy testing! 🚀

