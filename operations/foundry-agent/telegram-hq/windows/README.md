# Windows Telegram approval bridge

These scripts are a controller-side implementation candidate for the normal bounded Foundry-Agent approval path. They run on Bulldog-Surface Windows, not inside the Foundry-Agent execution distro.

Initialize-FoundryTelegramController.ps1 imports the existing Foundry Telegram bot token into a current-user DPAPI-protected controller file and pins Bulldog's private Telegram user and chat identity. It does not create or rotate a bot token and grants no task authority.

Invoke-FoundryTelegramApprovedTask.ps1 takes one already-prepared task file, sends its exact hash and bounds to the pinned Telegram identity, accepts one matching Approve or Reject callback, revalidates the task, workdir and repository target immediately before dispatch, invokes the existing run-foundry-agent-task.ps1 launcher, captures controller-side approval evidence, restores and verifies PAUSE, and reports the result to Telegram.

The bridge does not authorize merge, signing, production promotion, governance or doctrine changes, sealed-truth actions, new secrets or providers, founder overrides, or any unknown action. Repository actions are limited to commit, push, pr-create, and pr-update. Live repository target drift blocks dispatch.

Foundry-Agent must not receive the Telegram token or the DPAPI-protected token file. Approval evidence is written under C:\Users\John\Foundry-Control\telegram-evidence outside the agent workspace.
