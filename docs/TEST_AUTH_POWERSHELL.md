# Testing Authentication in PowerShell

## The Problem
PowerShell aliases `curl` to `Invoke-WebRequest`, which doesn't accept the same syntax as Unix `curl`.

## Solution 1: Use PowerShell Script (Easiest)

Run the PowerShell script I created:
```powershell
.\test_auth.ps1
```

## Solution 2: Use Invoke-RestMethod (PowerShell Native)

```powershell
$headers = @{
    "accept" = "application/json"
    "REQUEST-ID" = [System.Guid]::NewGuid().ToString()
    "TIMESTAMP" = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    "X-CM-ID" = "sbx"
    "Content-Type" = "application/json"
}

$body = @{
    clientId = "test_client"
    clientSecret = "test_secret"
    grantType = "client_credentials"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/session" -Method POST -Headers $headers -Body $body
```

## Solution 3: Use curl.exe Directly (If Available)

If you have curl.exe installed (Windows 10+ usually has it):

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/auth/session" `
  -H "accept: application/json" `
  -H "REQUEST-ID: 123e4567-e89b-12d3-a456-426614174000" `
  -H "TIMESTAMP: 2024-01-16T18:15:52Z" `
  -H "X-CM-ID: sbx" `
  -H "Content-Type: application/json" `
  -d '{\"clientId\": \"test_client\", \"clientSecret\": \"test_secret\", \"grantType\": \"client_credentials\"}'
```

Note: Use `curl.exe` instead of `curl` to avoid the PowerShell alias.

## Solution 4: Use Python (Always Works)

```powershell
python test_database.py
```

This will test everything automatically!

## Recommended: Use Swagger UI
Just open: http://127.0.0.1:8000/docs in your browser - it's the easiest way!

