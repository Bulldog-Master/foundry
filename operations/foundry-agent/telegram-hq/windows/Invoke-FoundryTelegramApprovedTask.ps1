param(
    [Parameter(Mandatory=$true)][string]$TaskFile,
    [Parameter(Mandatory=$true)][string]$WorkDir,
    [ValidateSet("read-only","workspace-write")][string]$Sandbox = "workspace-write",
    [string[]]$Actions = @(),
    [string]$Repository = "Bulldog-Master/foundry",
    [string]$Branch,
    [string]$ExpectedHeadSha,
    [Nullable[int]]$PrNumber,
    [int]$ApprovalMinutes = 5,
    [string]$ControlRoot = (Join-Path $env:USERPROFILE "Foundry-Control")
)

$ErrorActionPreference = "Stop"
$allowedActions = @("commit","push","pr-create","pr-update")
$telegramRoot = Join-Path $ControlRoot "telegram"
$tokenPath = Join-Path $telegramRoot "bot-token.dpapi"
$identityPath = Join-Path $telegramRoot "identity.json"
$launcher = Join-Path $ControlRoot "run-foundry-agent-task.ps1"
$statePath = Join-Path $ControlRoot "pause-kill\STATE.txt"
$evidenceRoot = Join-Path $ControlRoot "telegram-evidence"
$nl = [Environment]::NewLine

function Fail([string]$Message) { throw "BLOCKED: $Message" }

foreach ($p in @($tokenPath,$identityPath,$launcher,$statePath,$TaskFile)) {
    if (-not (Test-Path -LiteralPath $p)) { Fail "required path missing: $p" }
}
if ((Get-Content -LiteralPath $statePath -Raw).Trim() -ne "PAUSE") { Fail "controller state is not PAUSE" }

$taskInfo = Get-Item -LiteralPath $TaskFile
if ($taskInfo.Length -gt 16384) { Fail "task envelope exceeds 16 KiB" }
$taskHash = (Get-FileHash -LiteralPath $TaskFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actions.Count -ne (@($Actions | Select-Object -Unique)).Count) { Fail "duplicate actions" }
foreach ($a in $Actions) { if ($allowedActions -notcontains $a) { Fail "unauthorized action: $a" } }

$repoAction = $Actions.Count -gt 0
if ($Repository -ne "Bulldog-Master/foundry") { Fail "repository not allowed" }
if ($repoAction) {
    if ([string]::IsNullOrWhiteSpace($Branch)) { Fail "branch required" }
    if ($Branch.Contains("..") -or $Branch.StartsWith("/") -or $Branch.EndsWith("/")) { Fail "invalid branch" }
    if ($ExpectedHeadSha -notmatch '^[0-9a-fA-F]{40}$') { Fail "expected head SHA required" }
    if (($Actions -contains "pr-create") -and ($Actions -contains "pr-update")) { Fail "conflicting PR actions" }
    if ($Actions -contains "pr-update") {
        if (-not $PrNumber.HasValue -or $PrNumber.Value -le 0) { Fail "PR number required for pr-update" }
    } elseif ($PrNumber.HasValue) { Fail "unexpected PR number" }
}

function Get-PlainToken {
    $stored = Get-Content -LiteralPath $tokenPath -Raw
    $secure = ConvertTo-SecureString $stored
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function Invoke-Telegram([string]$Method, [hashtable]$Body = @{}) {
    $token = Get-PlainToken
    try {
        $response = Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot$token/$Method" -ContentType "application/json" -Body ($Body | ConvertTo-Json -Compress -Depth 12)
        if (-not $response.ok) { Fail "Telegram rejected $Method" }
        return $response
    }
    catch { Fail "Telegram API failure at $Method" }
    finally { $token = $null }
}

function Get-CurrentTarget {
    if (-not $repoAction) {
        return [ordered]@{ repository=$Repository; branch=$null; expected_head_sha=$null; pr_number=$null }
    }
    $headers = @{ Accept="application/vnd.github+json"; "User-Agent"="foundry-telegram-controller/0.1" }
    if ($Actions -contains "pr-update") {
        try { $pr = Invoke-RestMethod -Headers $headers -Uri "https://api.github.com/repos/$Repository/pulls/$($PrNumber.Value)" }
        catch { Fail "unable to read current PR target" }
        return [ordered]@{
            repository = [string]$pr.head.repo.full_name
            branch = [string]$pr.head.ref
            expected_head_sha = [string]$pr.head.sha
            pr_number = [int]$pr.number
        }
    }
    $escaped = [uri]::EscapeDataString($Branch)
    try { $b = Invoke-RestMethod -Headers $headers -Uri "https://api.github.com/repos/$Repository/branches/$escaped" }
    catch { Fail "unable to read current branch target" }
    return [ordered]@{
        repository = $Repository
        branch = [string]$b.name
        expected_head_sha = [string]$b.commit.sha
        pr_number = $null
    }
}

$resolved = (& wsl.exe -d Foundry-Agent -u foundry-agent -- readlink -f -- $WorkDir 2>$null | Select-Object -First 1).Trim()
if ([string]::IsNullOrWhiteSpace($resolved) -or $resolved -ne $WorkDir) { Fail "workdir does not resolve exactly" }
if (-not $resolved.StartsWith("/home/foundry-agent/work/")) { Fail "workdir outside approved root" }

$currentTarget = Get-CurrentTarget
if ($repoAction) {
    if ($currentTarget.repository -ne $Repository -or $currentTarget.branch -ne $Branch -or $currentTarget.expected_head_sha -ne $ExpectedHeadSha) { Fail "repository target drift before approval" }
    if (($Actions -contains "pr-update") -and $currentTarget.pr_number -ne $PrNumber.Value) { Fail "PR target drift before approval" }
}

$identity = Get-Content -LiteralPath $identityPath -Raw | ConvertFrom-Json
$taskId = "t" + (Get-Date -Format "yyyyMMddHHmmss") + ([guid]::NewGuid().ToString("N").Substring(0,6))
$nonce = [guid]::NewGuid().ToString("N").Substring(0,16)
$expires = (Get-Date).ToUniversalTime().AddMinutes($ApprovalMinutes)

$envelope = [ordered]@{
    task_id = $taskId
    nonce = $nonce
    expires_at = $expires.ToString("o")
    task_sha256 = $taskHash
    workdir = $WorkDir
    sandbox = $Sandbox
    actions = @($Actions)
    summary = "Bounded Foundry-Agent task"
    repository = $Repository
    branch = $(if ($repoAction) { $Branch } else { $null })
    expected_head_sha = $(if ($repoAction) { $ExpectedHeadSha.ToLowerInvariant() } else { $null })
    pr_number = $(if (($Actions -contains "pr-update")) { $PrNumber.Value } else { $null })
}

$envelopeJson = $envelope | ConvertTo-Json -Compress -Depth 8
$sha = [Security.Cryptography.SHA256]::Create()
try {
    $bytes = [Text.Encoding]::UTF8.GetBytes($envelopeJson + $nl)
    $envelopeSha = ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-","").ToLowerInvariant()
} finally { $sha.Dispose() }

New-Item -ItemType Directory -Force -Path $evidenceRoot | Out-Null
$evidence = Join-Path $evidenceRoot $taskId
New-Item -ItemType Directory -Path $evidence | Out-Null
$envelopeJson | Set-Content -LiteralPath (Join-Path $evidence "task-envelope.json") -Encoding UTF8
$envelopeSha | Set-Content -LiteralPath (Join-Path $evidence "task-envelope.sha256") -Encoding ASCII

$baseline = Invoke-Telegram "getUpdates" @{ timeout=0; allowed_updates=@("callback_query") }
$offset = 0
foreach ($u in $baseline.result) { if ([int64]$u.update_id -ge $offset) { $offset=[int64]$u.update_id+1 } }

$actionText = if ($Actions.Count) { $Actions -join ", " } else { "local task only" }
$targetText = if ($repoAction) { "$Repository / $Branch / $ExpectedHeadSha" } else { "no GitHub mutation" }
$text = @(
    "FOUNDRY APPROVAL REQUIRED",
    "",
    "Task: $taskId",
    "Task SHA-256: $taskHash",
    "Envelope SHA-256: $envelopeSha",
    "Sandbox: $Sandbox",
    "Workdir: $WorkDir",
    "Actions: $actionText",
    "Target: $targetText",
    "Expires: $($expires.ToString("yyyy-MM-dd HH:mm:ss 'UTC'"))",
    "",
    "Approve this exact bounded task?"
) -join $nl

$approveData = "approve:" + $taskId + ":" + $nonce
$rejectData = "reject:" + $taskId + ":" + $nonce

$sent = Invoke-Telegram "sendMessage" @{
    chat_id = [string]$identity.chat_id
    text = $text
    reply_markup = @{
        inline_keyboard = @(@(
            @{ text="Approve"; callback_data=$approveData },
            @{ text="Reject"; callback_data=$rejectData }
        ))
    }
}
$messageId = [int]$sent.result.message_id
$decision = $null
$decisionUpdate = $null

while ((Get-Date).ToUniversalTime() -lt $expires -and -not $decision) {
    $updates = Invoke-Telegram "getUpdates" @{ offset=$offset; timeout=10; allowed_updates=@("callback_query") }
    foreach ($u in $updates.result) {
        $offset=[int64]$u.update_id+1
        $cb=$u.callback_query
        if (-not $cb) { continue }
        if ([string]$cb.from.id -ne [string]$identity.founder_user_id) { continue }
        if ([string]$cb.message.chat.id -ne [string]$identity.chat_id) { continue }
        if ([int]$cb.message.message_id -ne $messageId) { continue }
        if ($cb.data -eq $approveData) { $decision="APPROVE" }
        elseif ($cb.data -eq $rejectData) { $decision="REJECT" }
        if ($decision) {
            $decisionUpdate=[int64]$u.update_id
            Invoke-Telegram "answerCallbackQuery" @{ callback_query_id=$cb.id; text="Foundry decision recorded: $decision" } | Out-Null
            break
        }
    }
}

$decisionRecord = [ordered]@{
    decision = $(if ($decision) { $decision } else { "EXPIRED" })
    task_id = $taskId
    envelope_sha256 = $envelopeSha
    task_sha256 = $taskHash
    founder_user_id = [string]$identity.founder_user_id
    chat_id = [string]$identity.chat_id
    message_id = $messageId
    telegram_update_id = $decisionUpdate
    decided_at_utc = (Get-Date).ToUniversalTime().ToString("o")
}
$decisionRecord | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidence "decision.json") -Encoding UTF8

if ($decision -ne "APPROVE") {
    Invoke-Telegram "sendMessage" @{ chat_id=[string]$identity.chat_id; text="Foundry task $taskId was not approved. Nothing executed." } | Out-Null
    Fail "task not approved"
}

if ((Get-Date).ToUniversalTime() -ge $expires) { Fail "approval expired before dispatch" }
if ((Get-Content -LiteralPath $statePath -Raw).Trim() -ne "PAUSE") { Fail "controller state changed before dispatch" }
if ((Get-FileHash -LiteralPath $TaskFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskHash) { Fail "task changed after approval" }

$resolvedNow = (& wsl.exe -d Foundry-Agent -u foundry-agent -- readlink -f -- $WorkDir 2>$null | Select-Object -First 1).Trim()
if ($resolvedNow -ne $resolved) { Fail "workdir changed after approval" }

$currentTargetNow = Get-CurrentTarget
if (($currentTargetNow | ConvertTo-Json -Compress) -ne ($currentTarget | ConvertTo-Json -Compress)) { Fail "repository target changed after approval" }

$launcherOutput = $null
try {
    Invoke-Telegram "sendMessage" @{ chat_id=[string]$identity.chat_id; text="Approved $taskId. Dispatching Foundry-Agent now." } | Out-Null
    $launcherOutput = & $launcher -TaskFile $TaskFile -WorkDir $WorkDir -Sandbox $Sandbox 2>&1 | Out-String
    $launcherOutput | Set-Content -LiteralPath (Join-Path $evidence "launcher-output.txt") -Encoding UTF8
}
finally {
    Set-Content -LiteralPath $statePath -Value "PAUSE" -Encoding ASCII
}

$finalState=(Get-Content -LiteralPath $statePath -Raw).Trim()
if ($finalState -ne "PAUSE") { Fail "failed to restore PAUSE" }

$job=[regex]::Match($launcherOutput,'JOB=([^\r\n]+)').Groups[1].Value.Trim()
$exit=[regex]::Match($launcherOutput,'CODEX_EXIT=([^\r\n]+)').Groups[1].Value.Trim()
$launcherEvidence=[regex]::Match($launcherOutput,'EVIDENCE=([^\r\n]+)').Groups[1].Value.Trim()

$final=[ordered]@{
    task_id=$taskId
    job=$job
    codex_exit=$exit
    final_state=$finalState
    launcher_evidence=$launcherEvidence
    approval_evidence=$evidence
}
$final | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidence "result.json") -Encoding UTF8

Get-ChildItem -LiteralPath $evidence -File | ForEach-Object {
    "$((Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant())  $($_.Name)"
} | Set-Content -LiteralPath (Join-Path $evidence "evidence.sha256") -Encoding ASCII

$complete = @(
    "FOUNDRY TASK COMPLETE",
    "Task: $taskId",
    "JOB: $job",
    "CODEX_EXIT: $exit",
    "FINAL_STATE: $finalState",
    "Evidence: $evidence"
) -join $nl
Invoke-Telegram "sendMessage" @{ chat_id=[string]$identity.chat_id; text=$complete } | Out-Null

$final
