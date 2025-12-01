# Script to update all .env files from .env.tunnel
# Run this script after updating tunnel URLs in .env.tunnel

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  Updating .env files from .env.tunnel" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.tunnel exists
if (-not (Test-Path ".env.tunnel")) {
    Write-Host "[ERROR] .env.tunnel not found!" -ForegroundColor Red
    exit 1
}

# Read .env.tunnel
$tunnelEnv = @{}
Get-Content ".env.tunnel" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $tunnelEnv[$matches[1].Trim()] = $matches[2].Trim()
    }
}

Write-Host "[INFO] Loaded tunnel URLs:" -ForegroundColor Green
Write-Host "  BACKEND_TUNNEL_URL: $($tunnelEnv['BACKEND_TUNNEL_URL'])" -ForegroundColor White
Write-Host "  BUSINESS_TUNNEL_URL: $($tunnelEnv['BUSINESS_TUNNEL_URL'])" -ForegroundColor White
Write-Host "  SHOP_TUNNEL_URL: $($tunnelEnv['SHOP_TUNNEL_URL'])" -ForegroundColor White
Write-Host ""

# Update shop/.env
Write-Host "[1/3] Updating shop/.env..." -ForegroundColor Yellow
$shopEnv = @"
# Auto-generated from tunnel config
# Generated at: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
BACKEND_TUNNEL_URL=$($tunnelEnv['BACKEND_TUNNEL_URL'])
SHOP_TUNNEL_URL=$($tunnelEnv['SHOP_TUNNEL_URL'])
NUXT_PUBLIC_API_BASE=$($tunnelEnv['BACKEND_TUNNEL_URL'])/api/v1/ecommerce
NUXT_PUBLIC_DEFAULT_HOST=$($tunnelEnv['SHOP_TUNNEL_URL'])
"@
Set-Content "shop/.env" $shopEnv -NoNewline
Write-Host "      [OK] shop/.env updated" -ForegroundColor Green

# Update business/.env
Write-Host "[2/3] Updating business/.env..." -ForegroundColor Yellow
$businessEnv = @"
# Auto-generated from tunnel config
# Generated at: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
BACKEND_TUNNEL_URL=$($tunnelEnv['BACKEND_TUNNEL_URL'])
BUSINESS_TUNNEL_URL=$($tunnelEnv['BUSINESS_TUNNEL_URL'])
NUXT_PUBLIC_API_BASE=$($tunnelEnv['BACKEND_TUNNEL_URL'])/api/v1/ecommerce
NUXT_PUBLIC_DEFAULT_HOST=$($tunnelEnv['BUSINESS_TUNNEL_URL'])
"@
Set-Content "business/.env" $businessEnv -NoNewline
Write-Host "      [OK] business/.env updated" -ForegroundColor Green

# Update backend/config.env - add tunnel URL to ALLOWED_HOSTS and CORS
Write-Host "[3/3] Updating backend/config.env..." -ForegroundColor Yellow

$configPath = "backend/config.env"
$configContent = Get-Content $configPath -Raw

# Extract backend tunnel URL without https://
$backendHost = $tunnelEnv['BACKEND_TUNNEL_URL'] -replace '^https?://', ''

# Update DJANGO_ALLOWED_HOSTS if not already present
if ($configContent -notmatch [regex]::Escape($backendHost)) {
    # Add to ALLOWED_HOSTS
    $configContent = $configContent -replace '(DJANGO_ALLOWED_HOSTS=[^\r\n]*)', "`$1,$backendHost"
    Write-Host "      [OK] Added $backendHost to DJANGO_ALLOWED_HOSTS" -ForegroundColor Green
} else {
    Write-Host "      [INFO] $backendHost already in DJANGO_ALLOWED_HOSTS" -ForegroundColor Cyan
}

# Update CORS_ALLOWED_ORIGINS
$shopUrl = $tunnelEnv['SHOP_TUNNEL_URL']
$businessUrl = $tunnelEnv['BUSINESS_TUNNEL_URL']
$backendUrl = $tunnelEnv['BACKEND_TUNNEL_URL']

if ($configContent -notmatch [regex]::Escape($shopUrl)) {
    $configContent = $configContent -replace '(CORS_ALLOWED_ORIGINS=[^\r\n]*)', "`$1,$shopUrl"
    Write-Host "      [OK] Added $shopUrl to CORS_ALLOWED_ORIGINS" -ForegroundColor Green
}

if ($configContent -notmatch [regex]::Escape($businessUrl)) {
    $configContent = $configContent -replace '(CORS_ALLOWED_ORIGINS=[^\r\n]*)', "`$1,$businessUrl"
    Write-Host "      [OK] Added $businessUrl to CORS_ALLOWED_ORIGINS" -ForegroundColor Green
}

if ($configContent -notmatch [regex]::Escape($backendUrl)) {
    $configContent = $configContent -replace '(CORS_ALLOWED_ORIGINS=[^\r\n]*)', "`$1,$backendUrl"
    Write-Host "      [OK] Added $backendUrl to CORS_ALLOWED_ORIGINS" -ForegroundColor Green
}

# Update VNPAY_RETURN_URL to use SHOP_TUNNEL_URL
$vnpayReturnUrl = "$($tunnelEnv['SHOP_TUNNEL_URL'])/payment/vnpay/return"
if ($configContent -match 'VNPAY_RETURN_URL=([^\r\n]*)') {
    $oldVnpayUrl = $matches[1]
    if ($oldVnpayUrl -ne $vnpayReturnUrl) {
        $configContent = $configContent -replace 'VNPAY_RETURN_URL=[^\r\n]*', "VNPAY_RETURN_URL=$vnpayReturnUrl"
        Write-Host "      [OK] Updated VNPAY_RETURN_URL to $vnpayReturnUrl" -ForegroundColor Green
    } else {
        Write-Host "      [INFO] VNPAY_RETURN_URL already correct" -ForegroundColor Cyan
    }
} else {
    Write-Host "      [WARN] VNPAY_RETURN_URL not found in config.env" -ForegroundColor Yellow
}

Set-Content -Path $configPath -Value $configContent -NoNewline
Write-Host "      [OK] backend/config.env updated" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  SUCCESS - All .env files updated!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart backend: cd backend; python manage.py runserver 8008" -ForegroundColor White
Write-Host "  2. Restart shop: cd shop; npm run dev -- --port 3011" -ForegroundColor White
Write-Host "  3. Restart business: cd business; npm run dev -- --port 3008" -ForegroundColor White
Write-Host ""
