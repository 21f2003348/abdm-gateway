# PowerShell script to test authentication
# Run this with: .\test_auth.ps1

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

Write-Host "Testing authentication..." -ForegroundColor Yellow
Write-Host "URL: $uri" -ForegroundColor Cyan
Write-Host "Headers:" -ForegroundColor Cyan
$headers | Format-Table
Write-Host "Body:" -ForegroundColor Cyan
Write-Host $body -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $uri -Method POST -Headers $headers -Body $body
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    Write-Host ""
    Write-Host "Access Token:" -ForegroundColor Yellow
    Write-Host $response.accessToken -ForegroundColor White
} catch {
    Write-Host "❌ ERROR!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Error Message:" -ForegroundColor Red
    $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body:" -ForegroundColor Red
        Write-Host $responseBody -ForegroundColor Yellow
    }
}

