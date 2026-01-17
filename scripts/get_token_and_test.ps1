# PowerShell script to get a fresh token and test bridge registration

Write-Host "Step 1: Getting access token..." -ForegroundColor Yellow

$uri = "http://127.0.0.1:8000/api/auth/session"

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

try {
    $response = Invoke-RestMethod -Uri $uri -Method POST -Headers $headers -Body $body
    $token = $response.accessToken
    
    Write-Host "✅ Token received!" -ForegroundColor Green
    Write-Host "`nAccess Token:" -ForegroundColor Cyan
    Write-Host $token -ForegroundColor White
    Write-Host "`nToken expires in: $($response.expiresIn) seconds" -ForegroundColor Cyan
    
    Write-Host "`n" + "="*60 -ForegroundColor Gray
    Write-Host "Step 2: Testing Bridge Registration with this token..." -ForegroundColor Yellow
    
    $bridgeUri = "http://127.0.0.1:8000/api/bridge/register"
    $bridgeHeaders = @{
        "accept" = "application/json"
        "REQUEST-ID" = [System.Guid]::NewGuid().ToString()
        "TIMESTAMP" = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        "X-CM-ID" = "sbx"
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $bridgeBody = @{
        bridgeId = "bridge-001"
        entityType = "HIP"
        name = "Test Hospital"
    } | ConvertTo-Json
    
    $bridgeResponse = Invoke-RestMethod -Uri $bridgeUri -Method POST -Headers $bridgeHeaders -Body $bridgeBody
    Write-Host "✅ Bridge registration successful!" -ForegroundColor Green
    Write-Host "`nResponse:" -ForegroundColor Cyan
    $bridgeResponse | ConvertTo-Json -Depth 10 | Write-Host
    
    Write-Host "`n" + "="*60 -ForegroundColor Gray
    Write-Host "Copy this token for your curl command:" -ForegroundColor Yellow
    Write-Host "Authorization: Bearer $token" -ForegroundColor White
    
} catch {
    Write-Host "❌ ERROR!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body:" -ForegroundColor Red
        Write-Host $responseBody -ForegroundColor Yellow
    } else {
        Write-Host "Error Message: $($_.Exception.Message)" -ForegroundColor Red
    }
}

