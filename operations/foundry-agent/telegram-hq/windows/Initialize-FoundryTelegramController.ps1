param(
    [string]$ControlRoot = (Join-Path $env:USERPROFILE "Foundry-Control")
)

$ErrorActionPreference = "Stop"
$telegramRoot = Join-Path $ControlRoot "telegram"
$tokenPath = Join-Path $telegramRoot "bot-token.dpapi"
$identityPath = Join-Path $telegramRoot "identity.json"
$launcher = Join-Path $ControlRoot "run-foundry-agent-task.ps1"
$statePath = Join-Path $ControlRoot "pause-kill\STATE.txt"

if (-not (Test-Path -LiteralPath $launcher)) { throw "Foundry-Agent launcher missing" }
if (-not (Test-Path -LiteralPath $statePath)) { throw "PAUSE/KILL state missing" }
if ((Get-Content -LiteralPath $statePath -Raw).Trim() -ne "PAUSE") { throw "Controller must be PAUSE before Telegram initialization" }

New-Item -ItemType Directory -Force -Path $telegramRoot | Out-Null
$currentIdentity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
& icacls.exe $telegramRoot /inheritance:r /grant:r "${currentIdentity}:(OI)(CI)F" "SYSTEM:(OI)(CI)F" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Unable to restrict Telegram controller directory ACL" }

$secure = Read-Host "Paste the EXISTING Foundry Telegram bot token (hidden)" -AsSecureString
$secure | ConvertFrom-SecureString | Set-Content -LiteralPath $tokenPath -Encoding ASCII
& icacls.exe $tokenPath /inheritance:r /grant:r "${currentIdentity}:F" "SYSTEM:F" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Unable to restrict token file ACL" }

function Get-PlainToken {
    $stored = Get-Content -LiteralPath $tokenPath -Raw
    $value = ConvertTo-SecureString $stored
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($value)
    try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function Invoke-Telegram([string]$Method, [hashtable]$Body = @{}) {
    $token = Get-PlainToken
    try {
        $response = Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot$token/$Method" -ContentType "application/json" -Body ($Body | ConvertTo-Json -Compress -Depth 10)
        if (-not $response.ok) { throw "Telegram rejected $Method" }
        return $response
    }
    finally { $token = $null }
}

$me = Invoke-Telegram "getMe"
if (-not $me.ok) { throw "Telegram bot credential validation failed" }

$baseline = Invoke-Telegram "getUpdates" @{ timeout = 0; allowed_updates = @("message") }
$offset = 0
foreach ($u in $baseline.result) { if ([int64]$u.update_id -ge $offset) { $offset = [int64]$u.update_id + 1 } }

Write-Host "Send /foundry-register to the existing Foundry bot from Bulldog's PRIVATE Telegram account."
$deadline = (Get-Date).AddMinutes(3)
$registration = $null

while ((Get-Date) -lt $deadline -and -not $registration) {
    $updates = Invoke-Telegram "getUpdates" @{ offset = $offset; timeout = 10; allowed_updates = @("message") }
    foreach ($u in $updates.result) {
        $offset = [int64]$u.update_id + 1
        $m = $u.message
        if (-not $m -or $m.text -ne "/foundry-register") { continue }
        if ($m.chat.type -ne "private") { continue }
        if ([string]$m.chat.id -ne [string]$m.from.id) { continue }
        $registration = [ordered]@{
            founder_user_id = [string]$m.from.id
            chat_id = [string]$m.chat.id
            bot_id = [string]$me.result.id
            bot_username = [string]$me.result.username
            registered_at_utc = (Get-Date).ToUniversalTime().ToString("o")
        }
        break
    }
}

if (-not $registration) { throw "No valid private /foundry-register message received" }
$registration | ConvertTo-Json | Set-Content -LiteralPath $identityPath -Encoding UTF8
& icacls.exe $identityPath /inheritance:r /grant:r "${currentIdentity}:F" "SYSTEM:F" | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Unable to restrict identity file ACL" }

Invoke-Telegram "sendMessage" @{ chat_id = $registration.chat_id; text = "Foundry Telegram controller identity pinned. No standing task authority was granted." } | Out-Null

Write-Host "FOUNDRY_TELEGRAM_CONTROLLER=INITIALIZED"
Write-Host "IDENTITY=$identityPath"
