# Toolbox release admission — publication locked

**Owner:** `fengie/heaven-toolbox-release` (new public repo, GitHub ID 1412539542).
**Source:** `fengie/heaven-toolbox` (private). **State:** no authorized release producer or Toolbox binaries.

1. Any published Toolbox release requires an independently trusted exact-commit authorization, valid signing key and artifact SHA-256/attestation verified by a separate public verifier.
2. Package identity must include source SHA, semantic version/tag `toolbox-v<semver>`, signed manifest, artifact digest, and real installed-client compatibility, update and rollback receipts.
3. The initial verifier rejects **all nonempty release indexes and GitHub Releases**. It has read-only GitHub Actions rights. Do not treat green policy CI as authorization to publish.
4. Existing MHW releases remain exclusively at `fengie/heaven-mod-manager-release` (different repository ID 1395549117). Never copy its `updater-main-*` artifacts, records or Git history.
5. Any proposal to unlock publication must introduce verified signing and independent evidence, negative tests, reviewer authorization and exact-head CI in a distinct reviewed PR. Never embed secrets or substitute metadata labels for cryptographic proofs.

On violation, stop promotion and preserve original bytes/evidence; do not silently replace or delete releases. No scheduled agents or non-GitHub source-of-truth.
