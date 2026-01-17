# Quick Test Commands

## Correct Authentication Request

### Using cURL (Windows PowerShell)
```powershell
curl -X POST "http://127.0.0.1:8000/api/auth/session" `
  -H "accept: application/json" `
  -H "REQUEST-ID: 123e4567-e89b-12d3-a456-426614174000" `
  -H "TIMESTAMP: 2024-01-16T18:15:52Z" `
  -H "X-CM-ID: sbx" `
  -H "Content-Type: application/json" `
  -d '{
    "clientId": "test_client",
    "clientSecret": "test_secret",
    "grantType": "client_credentials"
  }'
```

### Using cURL (Linux/Mac)
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/session" \
  -H "accept: application/json" \
  -H "REQUEST-ID: $(uuidgen)" \
  -H "TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -H "X-CM-ID: sbx" \
  -H "Content-Type: application/json" \
  -d '{
    "clientId": "test_client",
    "clientSecret": "test_secret",
    "grantType": "client_credentials"
  }'
```

## Correct Credentials

- **clientId**: `test_client` (NOT "string")
- **clientSecret**: `test_secret` (NOT "string")
- **grantType**: `client_credentials` (NOT "string")
- **X-CM-ID**: `sbx` (NOT "123")
- **TIMESTAMP**: ISO format timestamp (e.g., `2024-01-16T18:15:52Z`)
- **REQUEST-ID**: Any UUID (e.g., `123e4567-e89b-12d3-a456-426614174000`)

## Expected Response

```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expiresIn": 900,
  "tokenType": "Bearer"
}
```

## Common Mistakes

❌ **Wrong:**
```json
{
  "clientId": "string",
  "clientSecret": "string",
  "grantType": "string"
}
```

✅ **Correct:**
```json
{
  "clientId": "test_client",
  "clientSecret": "test_secret",
  "grantType": "client_credentials"
}
```

## Using Swagger UI (Easiest)

1. Go to: http://127.0.0.1:8000/docs
2. Click on `POST /api/auth/session`
3. Click "Try it out"
4. Replace the default values with:
   - clientId: `test_client`
   - clientSecret: `test_secret`
   - grantType: `client_credentials`
5. In the headers section, add:
   - REQUEST-ID: `123e4567-e89b-12d3-a456-426614174000`
   - TIMESTAMP: `2024-01-16T18:15:52Z`
   - X-CM-ID: `sbx`
6. Click "Execute"

