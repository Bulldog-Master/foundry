$ErrorActionPreference = 'Stop'
$runtime = '288f8f9117764d8e18db67c885d4f7319b93c85a'
$manifest = '62957533ca9b3ff9b76a9bec8a24dc164ef8ae378e023ba58e691791a858caf1'
$oldHead = 'f949d06fa43581b8851b789e28d108b7da9950b5'
$newHead = 'bd78909848c07e7f9cfea04f761fd9981640874e'
$base = '4c2c611b61a1947bef409e5357f5426703bca452'
$source = "/var/lib/foundry-evaluator/handoffs/$manifest/source"
function Native([string]$program, [string[]]$arguments) {
    & $program @arguments
    if ($LASTEXITCODE -ne 0) { throw "$program failed with exit $LASTEXITCODE; evidence retained" }
}
function ExactPr([string]$expectedHead) {
    $pr = Invoke-RestMethod -Uri 'https://api.github.com/repos/Bulldog-Master/foundry/pulls/26' -Headers @{ 'User-Agent' = 'foundry-pr26-founder-handoff'; 'Accept' = 'application/vnd.github+json' }
    if ($pr.state -ne 'open' -or $pr.head.sha -ne $expectedHead -or $pr.base.sha -ne $base -or $pr.head.repo.id -ne 1297877588 -or $pr.base.repo.id -ne 1297877588) { throw 'PR head/base/repository drift; evidence retained' }
}
Get-Command git.exe -ErrorAction Stop | Out-Null
Get-Command wsl.exe -ErrorAction Stop | Out-Null
ExactPr $oldHead
$bootstrap = @'
set -euo pipefail
umask 077
runtime='RUNTIME'
manifest='MANIFEST'
source='/var/lib/foundry-evaluator/handoffs/MANIFEST/source'
install -d -o root -g root -m 0700 "/var/lib/foundry-evaluator/handoffs/$manifest"
if [[ ! -d "$source" ]]; then
  git -c credential.helper= -c core.askPass= clone --no-checkout https://github.com/Bulldog-Master/foundry.git "$source"
  git -C "$source" checkout --detach "$runtime"
fi
[[ $(git -C "$source" rev-parse HEAD) == "$runtime" ]]
[[ $(sha256sum "$source/MANIFEST.sha256" | cut -d' ' -f1) == "$manifest" ]]
bash "$source/pr26-root-handoff.sh" install-publish
'@
$bootstrap = $bootstrap.Replace("runtime='RUNTIME'", "runtime='$runtime'")
$bootstrap = $bootstrap.Replace("manifest='MANIFEST'", "manifest='$manifest'")
$bootstrap = $bootstrap.Replace("handoffs/MANIFEST/source", "handoffs/$manifest/source")
$encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($bootstrap.Replace("`r", '')))
Native 'wsl.exe' @('-d','Foundry-Agent','-u','root','--','bash','-lc',"printf '%s' '$encoded' | base64 -d | bash")
# This step cannot run until the root handoff verifies completed App failure publication.
ExactPr $oldHead
$bundlePath = "\\wsl.localhost\Foundry-Agent\tmp\foundry-pr26-$newHead.bundle"
$prRepo = Join-Path ([IO.Path]::GetTempPath()) ('foundry-pr26-push-' + [Guid]::NewGuid().ToString('N'))
Native 'git.exe' @('init', $prRepo)
Native 'git.exe' @('-C',$prRepo,'remote','add','origin','https://github.com/Bulldog-Master/foundry.git')
Native 'git.exe' @('-C',$prRepo,'fetch','origin','refs/heads/foundry2/review-packet-contract-v0.1')
$observed = (& git.exe -C $prRepo rev-parse FETCH_HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $observed -ne $oldHead) { throw 'Fetched PR head differs; no push' }
Native 'git.exe' @('-C',$prRepo,'bundle','verify',$bundlePath)
Native 'git.exe' @('-C',$prRepo,'fetch',$bundlePath,'HEAD')
$bundled = (& git.exe -C $prRepo rev-parse FETCH_HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $bundled -ne $newHead) { throw 'Remediation bundle SHA mismatch; no push' }
Native 'git.exe' @('-C',$prRepo,'merge-base','--is-ancestor',$oldHead,$newHead)
ExactPr $oldHead
Native 'git.exe' @('-C',$prRepo,'push','origin',"${newHead}:refs/heads/foundry2/review-packet-contract-v0.1")
ExactPr $newHead
Native 'wsl.exe' @('-d','Foundry-Agent','-u','root','--','bash',"$source/pr26-root-handoff.sh",'seal')
