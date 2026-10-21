param([Parameter(Mandatory=$true)][string]$EvidenceDirectory)
$ErrorActionPreference='Stop'
$capture=Join-Path $PSScriptRoot 'Capture-CA001StageB.ps1'
$parseTokens=$null; $parseErrors=$null
[void][Management.Automation.Language.Parser]::ParseFile($capture,[ref]$parseTokens,[ref]$parseErrors)
if($parseErrors.Count) { throw 'Capture script syntax error.' }
. $capture -LibraryOnly
$program=Join-Path $PSHOME 'powershell.exe'
if(Test-Path -LiteralPath $EvidenceDirectory) { throw 'Self-test evidence directory must be new.' }
[void][IO.Directory]::CreateDirectory($EvidenceDirectory)
$cases=@(
    @{name='raw-streams';code='[Console]::Out.Write("stand-in-out");[Console]::Error.Write("stand-in-err");exit 0';seconds=5;limit=1048576;status='completed';exit=0},
    @{name='nonzero';code='exit 7';seconds=5;limit=1048576;status='completed';exit=7},
    @{name='timeout';code='Start-Sleep -Seconds 10';seconds=0.25;limit=1048576;status='timeout';exit=$null},
    @{name='stdout-limit';code='$b=[byte[]]::new(16384);[Console]::OpenStandardOutput().Write($b,0,$b.Length)';seconds=5;limit=1024;status='output-limit';exit=$null},
    @{name='stderr-limit';code='$b=[byte[]]::new(16384);[Console]::OpenStandardError().Write($b,0,$b.Length)';seconds=5;limit=1024;status='output-limit';exit=$null},
    @{name='combined-limit';code='$b=[byte[]]::new(700);[Console]::OpenStandardOutput().Write($b,0,700);[Console]::OpenStandardError().Write($b,0,700)';seconds=5;limit=1024;status='output-limit';exit=$null}
)
$results=@()
foreach($case in $cases) {
    $directory=Join-Path $EvidenceDirectory $case.name
    [void][IO.Directory]::CreateDirectory($directory)
    $encoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($case.code))
    $result=Capture-CA001Process -Program $program -Arguments @('-NoProfile','-NonInteractive','-EncodedCommand',$encoded) -InputBytes ([byte[]]::new(0)) -Directory $directory -Seconds $case.seconds -OutputLimit $case.limit
    $ok=($result.status -ceq $case.status -and $result.retained_output_bytes -le $case.limit)
    if($null -ne $case.exit) { $ok=$ok -and $result.exit_code -eq $case.exit }
    if($case.name -ceq 'raw-streams') {
        $ok=$ok -and [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes((Join-Path $directory 'stdout.bin'))) -ceq 'stand-in-out'
        $ok=$ok -and [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes((Join-Path $directory 'stderr.bin'))) -ceq 'stand-in-err'
    }
    $results+= @{case=$case.name;passed=$ok;observed_status=$result.status}
}
$directory=Join-Path $EvidenceDirectory 'launch-failure'
[void][IO.Directory]::CreateDirectory($directory)
$result=Capture-CA001Process -Program (Join-Path $directory 'nonexistent-stand-in.exe') -Arguments @() -InputBytes ([byte[]]::new(0)) -Directory $directory -Seconds 1
$results+= @{case='launch-failure';passed=($result.status -ceq 'capture-error');observed_status=$result.status}
$hash=Get-CA001BytesHash ([Text.Encoding]::ASCII.GetBytes('abc'))
$results+= @{case='byte-hash';passed=($hash -ceq 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');observed_status='checked'}
$rejected=$false
try { [void](Resolve-CA001Directory ([IO.Path]::GetFullPath((Join-Path $EvidenceDirectory '..'))) $EvidenceDirectory) }
catch { $rejected=$true }
$results+= @{case='directory-traversal';passed=$rejected;observed_status='checked'}
$report=@{record_type='capture-mechanics-only-not-ca001-evaluation';cases=$results;candidate_executed=$false;stage_a_tests_executed=$false}
Write-CA001Json (Join-Path $EvidenceDirectory 'self-test.json') $report
$report | ConvertTo-Json -Depth 5 -Compress
if(@($results | Where-Object {-not $_.passed}).Count) { throw 'Capture mechanics self-test failure; evidence retained.' }
