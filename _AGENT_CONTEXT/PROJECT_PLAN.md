# Heaven Toolbox Release — live project plan (2026-10-09)

**Status:** new Toolbox-only channel setup in PR; publication LOCKED. No releases created or signed.

## R-001 — Repository isolation (active candidate)
Set canonical `fengie/heaven-toolbox-release`, empty index, no MHW content/history, read-only policy workflow, negative tests and exact CI proof. After safe main merge verify zero GitHub Releases.

## R-002 — Signed production publishing (BLOCKED)
Coordinate with existing private Toolbox #666/#763. Requires independent signer, reviewed authorization, exact source SHA, public artifact signature/digest, no secrets, installed consumer and rollback. No initial Toolbox binary should be published until all conditions pass.

MHW historical releases belong to `fengie/heaven-mod-manager-release`. Do not rename/erase signed historical `updater-main-*` tags, their SHA-256 digest records, or client URLs. Rulesets need separate GitHub admin settings; code cannot configure them through the current connector.
