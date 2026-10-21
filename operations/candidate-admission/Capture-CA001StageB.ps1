param(
    [string]$ManifestPath,
    [string]$ManifestSha256,
    [string]$AuthorizationReceiptPath,
    [string]$AuthorizationReceiptSha256,
    [switch]$Execute,
    [switch]$LibraryOnly
)
$ErrorActionPreference='Stop'

function Get-CA001Hash([string]$File) {
    (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-CA001BytesHash([byte[]]$Bytes) {
    $algorithm=[Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($algorithm.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant() }
    finally { $algorithm.Dispose() }
}

function Resolve-CA001Directory([string]$Directory,[string]$ControlRoot) {
    $resolved=[IO.Path]::GetFullPath($Directory).TrimEnd('\')
    $prefix=[IO.Path]::GetFullPath($ControlRoot).TrimEnd('\')+'\'
    if(-not $resolved.StartsWith($prefix,[StringComparison]::OrdinalIgnoreCase) -or
       -not (Test-Path -LiteralPath $resolved -PathType Container)) { throw 'Existing controller-contained directory required.' }
    $entry=Get-Item -LiteralPath $resolved
    while($null -ne $entry) {
        if($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point in controller path.' }
        $entry=$entry.Parent
    }
    return $resolved
}

function Write-CA001Json([string]$File, $Value) {
    [IO.File]::WriteAllText($File, ($Value | ConvertTo-Json -Depth 20), [Text.UTF8Encoding]::new($false))
}

function Get-CA001Arguments($Items) {
    ($Items | ForEach-Object {
        if($_ -ne '' -and $_ -notmatch '[\s"]') { $_ }
        else { '"' + ($_ -replace '(\\*)"','$1$1\"' -replace '(\\+)$','$1$1') + '"' }
    }) -join ' '
}

function Get-CA001IsolationArguments {
    $work='/home/foundry-agent/work/candidate-admission/ca001-v1'
    @('--unshare-all','--die-with-parent','--new-session',
      '--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64',
      '--ro-bind','/etc/passwd','/etc/passwd','--ro-bind','/etc/group','/etc/group',
      '--dir','/tmp','--proc','/proc','--dev','/dev','--bind',$work,$work,
      '--chdir',$work,'--remount-ro','/')
}

function Get-CA001IsolationLauncher {
@'
import hashlib,os,pathlib,sys
tool='/usr/bin/bwrap'
assert hashlib.sha256(pathlib.Path(tool).read_bytes()).hexdigest()==sys.argv[1]
os.execv(tool,[tool]+sys.argv[2:])
'@
}

function Capture-CA001Process {
    param([string]$Program, [string[]]$Arguments, [byte[]]$InputBytes,
          [string]$Directory, [double]$Seconds=60, [long]$OutputLimit=1048576,
          [switch]$CleanWSLEnvironment)
    $started=[DateTimeOffset]::UtcNow.ToString('o')
    $watch=[Diagnostics.Stopwatch]::StartNew()
    $process=[Diagnostics.Process]::new()
    $process.StartInfo=[Diagnostics.ProcessStartInfo]::new()
    $process.StartInfo.FileName=$Program
    $process.StartInfo.Arguments=Get-CA001Arguments $Arguments
    $process.StartInfo.UseShellExecute=$false
    $process.StartInfo.CreateNoWindow=$true
    $process.StartInfo.RedirectStandardInput=$true
    $process.StartInfo.RedirectStandardOutput=$true
    $process.StartInfo.RedirectStandardError=$true
    # Prevent Windows path exports from being translated before Linux env -i.
    # This changes only this child's environment, never the parent or WSL config.
    if($CleanWSLEnvironment) { $process.StartInfo.EnvironmentVariables['WSLENV']='' }
    $streams=@(); $files=@(); $pending=@(); $buffers=@(); $counts=@(0L,0L)
    $status='launch-error'; $exitCode=$null; $observed=0L; $retained=0L; $launched=$false
    try {
        [void]$process.Start()
        $launched=$true
        $streams=@($process.StandardOutput.BaseStream,$process.StandardError.BaseStream)
        foreach($name in @('stdout.bin','stderr.bin')) {
            $files+= [IO.File]::Open((Join-Path $Directory $name),[IO.FileMode]::CreateNew)
            $buffers+= ,([byte[]]::new(4096))
        }
        for($i=0;$i -lt 2;$i++) { $pending+= $streams[$i].ReadAsync($buffers[$i],0,4096) }
        # Bounded manifest only; no shell command or candidate input comes from stdin.
        $write=$process.StandardInput.BaseStream.WriteAsync($InputBytes,0,$InputBytes.Length)
        $inputClosed=$false; $open=2; $status='completed'
        while($true) {
            if($watch.Elapsed.TotalSeconds -ge $Seconds) { $status='timeout'; break }
            if(-not $inputClosed -and $write.IsCompleted) {
                $null=$write.GetAwaiter().GetResult(); $process.StandardInput.Close(); $inputClosed=$true
            }
            for($i=0;$i -lt 2;$i++) {
                if($null -eq $pending[$i] -or -not $pending[$i].IsCompleted) { continue }
                $size=$pending[$i].GetAwaiter().GetResult()
                if($size -eq 0) { $pending[$i]=$null; $open--; continue }
                $observed+=$size
                $keep=[int][Math]::Min($size,[Math]::Max(0,$OutputLimit-$retained))
                if($keep -gt 0) { $files[$i].Write($buffers[$i],0,$keep); $retained+=$keep; $counts[$i]+=$keep }
                if($observed -gt $OutputLimit) { $status='output-limit'; break }
                $pending[$i]=$streams[$i].ReadAsync($buffers[$i],0,4096)
            }
            if($status -eq 'output-limit') { break }
            if($open -eq 0 -and $process.HasExited) { break }
            Start-Sleep -Milliseconds 2
        }
        if(-not $process.HasExited) { $process.Kill() }
        if($process.WaitForExit(2000)) { $exitCode=$process.ExitCode }
        else { $status='client-cleanup-unverified' }
    } catch {
        $status='capture-error'
        if($launched -and -not $process.HasExited) { $process.Kill(); [void]$process.WaitForExit(2000) }
    } finally {
        foreach($file in $files) { $file.Dispose() }
        $watch.Stop()
        $record=[ordered]@{status=$status;exit_code=$exitCode;started_utc=$started;
            ended_utc=[DateTimeOffset]::UtcNow.ToString('o');seconds=$watch.Elapsed.TotalSeconds;
            command=@($Program)+$Arguments;observed_output_bytes=$observed;retained_output_bytes=$retained;
            stdout_bytes=$counts[0];stderr_bytes=$counts[1];output_complete=($status -eq 'completed');
            stdout_sha256=$null;stderr_sha256=$null;remote_cleanup_verified=$false;
            wsl_environment_cleared=[bool]$CleanWSLEnvironment}
        foreach($name in @('stdout','stderr')) {
            $file=Join-Path $Directory ($name+'.bin')
            if(Test-Path -LiteralPath $file) { $record[$name+'_sha256']=Get-CA001Hash $file }
        }
        Write-CA001Json (Join-Path $Directory 'capture.json') $record
        $process.Dispose()
    }
    return $record
}

if($LibraryOnly) { return }
if(-not $Execute) { throw 'Execution disabled; separate frozen Stage B authorization is required.' }
$auditRoot=$null; $attempt=$null
trap {
    # Before a valid custody root exists, rejection remains on the operator's
    # transcript. Once it is bound, retain preflight failures there as well.
    if($auditRoot -and -not $attempt) {
        $rejection=Join-Path $auditRoot ('rejected-'+[Guid]::NewGuid().ToString('N'))
        [void][IO.Directory]::CreateDirectory($rejection)
        Write-CA001Json (Join-Path $rejection 'preflight.json') @{
            status='rejected-before-child-launch';manifest_sha256=$ManifestSha256;
            authorization_receipt_sha256=$AuthorizationReceiptSha256;
            error=$_.Exception.Message;observed_utc=[DateTimeOffset]::UtcNow.ToString('o')}
    }
    throw
}
foreach($hash in @($ManifestSha256,$AuthorizationReceiptSha256)) {
    if($hash -cnotmatch '^[0-9a-f]{64}$') { throw 'Externally bound SHA256 is required.' }
}
$raw=[IO.File]::ReadAllBytes($ManifestPath)
$receiptBytes=[IO.File]::ReadAllBytes($AuthorizationReceiptPath)
if((Get-CA001BytesHash $raw) -cne $ManifestSha256 -or
   (Get-CA001BytesHash $receiptBytes) -cne $AuthorizationReceiptSha256) { throw 'Frozen input mismatch.' }
if($raw.Length -gt 65536) { throw 'Manifest size limit exceeded.' }
$manifest=[Text.Encoding]::UTF8.GetString($raw) | ConvertFrom-Json
$receipt=[Text.Encoding]::UTF8.GetString($receiptBytes) | ConvertFrom-Json
if($manifest.schema -cne 'ca001-stage-b-v1' -or
   $receipt.kind -cne 'CA-001-Stage-B-execution' -or
   $receipt.manifest_sha256 -cne $ManifestSha256 -or $receipt.pass_limit -ne 2 -or
   [DateTimeOffset]::Parse($receipt.expires_utc) -le [DateTimeOffset]::UtcNow.AddSeconds(120)) {
    throw 'Receipt does not bind this exact two-pass execution window.'
}
# Receipt custody/authenticity must be established outside this producer script.
$controlRoot=Join-Path $env:USERPROFILE 'Foundry-Control'
$stateFile=Join-Path $controlRoot 'pause-kill\STATE.txt'
if((Get-Content -LiteralPath $stateFile -Raw).Trim() -cne 'PAUSE') { throw 'Controller is not PAUSE.' }
$manifest.evidence_root=Resolve-CA001Directory $manifest.evidence_root $controlRoot
$auditRoot=$manifest.evidence_root
$wsl=Join-Path $env:WINDIR 'System32\wsl.exe'
if((Get-CA001Hash $PSCommandPath) -cne $manifest.capture_sha256 -or
   (Get-CA001Hash $wsl) -cne $manifest.wsl_sha256 -or
   $manifest.runtime.path -cnotmatch '^/usr/bin/python3\.[0-9]+$') { throw 'Capture/launcher/runtime drift.' }
if($manifest.isolation.mode -cne 'readonly-root-bwrap-v1' -or
   $manifest.isolation.path -cne '/usr/bin/bwrap' -or
   $manifest.isolation.sha256 -cnotmatch '^[0-9a-f]{64}$') { throw 'Frozen isolation profile required.' }
$manifest.frozen_source_root=Resolve-CA001Directory $manifest.frozen_source_root $controlRoot
$names=@('PROTOCOL-v0.1.md','CA-001-deterministic-rule-promotion.md','CA-001-EVALUATION-PACKET-v1.md',
    'ca001_checker.py','fixtures/ca001-v1.jsonl','test_ca001_checker.py','ca001_harness.py')
$frozen=@{}
foreach($name in $names) {
    $source=Join-Path $manifest.frozen_source_root $name
    $frozen[$name]=[IO.File]::ReadAllBytes($source)
    if((Get-CA001BytesHash $frozen[$name]) -cne $manifest.sources.$name) { throw 'Controller-frozen source drift.' }
}
$prerequisiteNames=@('reviewer-record.json','expected-results-confirmation.json','custody-record.json','environment-record.json')
foreach($name in $prerequisiteNames) {
    if($manifest.prerequisites.$name -cnotmatch '^[0-9a-f]{64}$') { throw 'Unresolved Stage B prerequisite record.' }
    $bytes=[IO.File]::ReadAllBytes((Join-Path $manifest.frozen_source_root $name))
    if((Get-CA001BytesHash $bytes) -cne $manifest.prerequisites.$name) { throw 'Prerequisite record drift.' }
    $frozen[$name]=$bytes
}
# Bootstrap bytes are bound by this controller script's hash. Never execute an
# actor-writable harness file before checking it against the frozen controller copy.
$bootstrap=@'
import base64,hashlib,io,json,sys
request=json.loads(sys.stdin.buffer.read(65537))
manifest=base64.b64decode(request['manifest'],validate=True)
assert hashlib.sha256(manifest).hexdigest()==sys.argv[1]
source=base64.b64decode(request['harness'],validate=True)
assert hashlib.sha256(source).hexdigest()==json.loads(manifest)['sources']['ca001_harness.py']
filename='/home/foundry-agent/work/candidate-admission/ca001-v1/ca001_harness.py'
sys.argv=[filename,'--execute','--manifest-sha256',sys.argv[1],'--deadline-utc',sys.argv[2]]
sys.stdin=io.TextIOWrapper(io.BytesIO(manifest),encoding='utf-8')
exec(compile(source,filename,'exec'),{'__name__':'__main__','__file__':filename})
'@
$request=@{manifest=[Convert]::ToBase64String($raw);harness=[Convert]::ToBase64String($frozen['ca001_harness.py'])}
$requestBytes=[Text.Encoding]::UTF8.GetBytes(($request | ConvertTo-Json -Compress))
if($requestBytes.Length -gt 65536) { throw 'Bootstrap input exceeds bound.' }
$isolationLauncher=Get-CA001IsolationLauncher
$lock=[IO.File]::Open((Join-Path $manifest.evidence_root 'ca001.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
$consumed=$null
try {
    $consumed=[IO.File]::Open((Join-Path $manifest.evidence_root ('used-'+$AuthorizationReceiptSha256)),[IO.FileMode]::CreateNew)
    $consumed.Dispose()
} catch { $lock.Dispose(); throw 'Authorization receipt already used or marker unavailable; no retry.' }
$attempt=Join-Path $manifest.evidence_root ('attempt-'+[Guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($attempt)
$summary=[ordered]@{status='incomplete';manifest_sha256=$ManifestSha256;
    authorization_receipt_sha256=$AuthorizationReceiptSha256;passes=@();identical_raw_outputs=$false;
    admission_approved=$false;independent_review='not_performed';custody_verified=$false}
try {
    [IO.File]::WriteAllBytes((Join-Path $attempt 'manifest.json'),$raw)
    [IO.File]::WriteAllBytes((Join-Path $attempt 'authorization-receipt.json'),$receiptBytes)
    foreach($name in @($names)+@($prerequisiteNames)) {
        $destination=Join-Path $attempt ('sources/'+$name)
        [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($destination))
        [IO.File]::WriteAllBytes($destination,$frozen[$name])
    }
    for($number=1;$number -le 2;$number++) {
        if((Get-Content -LiteralPath $stateFile -Raw).Trim() -cne 'PAUSE') { throw 'Controller state changed; preserved.' }
        if([DateTimeOffset]::Parse($receipt.expires_utc) -le [DateTimeOffset]::UtcNow.AddSeconds(60)) {
            throw 'Authorization window cannot cover this pass.'
        }
        $pass=Join-Path $attempt ('pass-'+$number); [void][IO.Directory]::CreateDirectory($pass)
        $deadline=([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()/1000.0+60).ToString('R',[Globalization.CultureInfo]::InvariantCulture)
        $work='/home/foundry-agent/work/candidate-admission/ca001-v1'
        $arguments=@('-d','Foundry-Agent','-u','foundry-agent','--cd',$work,'--exec',
            '/usr/bin/env','-i',$manifest.runtime.path,'-I','-B','-c',$isolationLauncher,
            $manifest.isolation.sha256)+@(Get-CA001IsolationArguments)+
            @($manifest.runtime.path,'-I','-B','-c',$bootstrap,$ManifestSha256,$deadline)
        $result=Capture-CA001Process -Program $wsl -Arguments $arguments -InputBytes $requestBytes -Directory $pass -CleanWSLEnvironment
        $summary.passes+= $result
        if($result.status -cne 'completed' -or $result.exit_code -ne 0) { throw 'Pass failed; no retry or next pass.' }
        $reported=[Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes((Join-Path $pass 'stdout.bin'))) | ConvertFrom-Json
        if($reported.all_expected_results -ne $true -or $reported.tests_ok -ne $true -or
           $reported.tests_run -ne 8 -or @($reported.cases).Count -ne 12) { throw 'Missing structured pass results.' }
        $expectedCases=[Text.Encoding]::UTF8.GetString($frozen['fixtures/ca001-v1.jsonl']).TrimEnd("`r","`n").Split("`n")
        for($index=0;$index -lt 12;$index++) {
            $expectedCase=$expectedCases[$index] | ConvertFrom-Json
            if($reported.cases[$index].case_id -cne $expectedCase.case_id -or
               $reported.cases[$index].result -cne $expectedCase.expected_result -or
               $reported.cases[$index].matches_expected -ne $true) { throw 'Controller-side expected-result mismatch.' }
        }
        if((Get-Content -LiteralPath $stateFile -Raw).Trim() -cne 'PAUSE') { throw 'Controller state changed; preserved.' }
    }
    $one=$summary.passes[0]; $two=$summary.passes[1]
    $summary.identical_raw_outputs=($one.stdout_sha256 -ceq $two.stdout_sha256 -and $one.stderr_sha256 -ceq $two.stderr_sha256)
    if(-not $summary.identical_raw_outputs) { throw 'Raw pass outputs differ.' }
    $summary.status='producer-pass-comparison-complete-not-admission'
} catch {
    $summary.status='failed-or-invalid-attempt'
    $summary.failure=$_.Exception.Message
} finally {
    Write-CA001Json (Join-Path $attempt 'summary.json') $summary
    Get-ChildItem -LiteralPath $attempt -Recurse -File | ForEach-Object {
        @{file=$_.FullName.Substring($attempt.Length+1);sha256=Get-CA001Hash $_.FullName}
    } | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $attempt 'files.json') -Encoding UTF8
    $lock.Dispose()
}
if($summary.status -cne 'producer-pass-comparison-complete-not-admission') { throw ('Attempt retained: '+$attempt) }
