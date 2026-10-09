# Heaven Toolbox Releases

> ⏱️ Last README update: **October 9, 2026 · 7:10:22 PM EDT** _(repo-enforced)_

Canonical public release-only repository: `fengie/heaven-toolbox-release` (GitHub ID **1412539542**). Private source: `fengie/heaven-toolbox`.

**LOCKED: no binaries published or authorized.** This new repository is intentionally separate from [Heaven Mod Manager Releases](https://github.com/fengie/heaven-mod-manager-release), which retains historical MHW `updater-main-*` artifacts, hashes and compatibility links.

All release artifacts must originate from reviewed, signed exact-source Toolbox builds, be verified through public signatures/digests and installed-client rollback checks before `publication_enabled` can change. Review [RELEASE_CONTRACT.md](RELEASE_CONTRACT.md) and [_AGENT_CONTEXT/PROJECT_PLAN.md](_AGENT_CONTEXT/PROJECT_PLAN.md).

CI: `python -m unittest discover -s tests -v` and `python scripts/verify_release_repo.py --live`. No scheduled agents, hidden release publisher, AppDeploy, private source code, or MHW binaries are permitted here.
