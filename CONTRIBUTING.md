# Contributing to openclaw-install-kit

Thank you for helping improve this kit. Contributions are welcome — especially real-world test reports, OS/hardware validation, and fixes to skill files based on actual install experience.

---

## What kind of contributions are most useful

**High value:**
- Real-world test reports (see template in TESTING.md) — especially for Debian, macOS, Raspberry Pi, or hardware profiles other than the ASUS UX305FA
- Fixes to skill files where instructions failed or were incomplete
- Validation of WhatsApp Path B (Meta Business API) — currently undocumented/untested
- Reports of OpenClaw CLI changes that break skill file commands

**Medium value:**
- Additional troubleshooting entries for the skill 07 runbook template
- Integration guides for platforms not yet covered (Discord, Signal, Teams)
- Improvements to Phase 0a (computing selection) for specific hardware profiles

**Out of scope (for now):**
- Local LLM / Ollama setups
- Windows native support (WSL2 is an acceptable workaround)
- Cloud-only or managed OpenClaw offerings

---

## How to contribute

1. **Fork the repo** and create a branch from `main`
2. **Test your change** against a real install if possible — even one data point helps
3. **Submit a pull request** with:
   - What you changed and why
   - What hardware/OS you tested on
   - What output or behavior you observed

If you're reporting a broken skill step without a fix, open an issue instead.

---

## Reporting issues

Use the issue tracker. For install failures, include:
- Which phase failed (e.g. "Phase 4 — WhatsApp")
- The exact command that failed
- The output you got
- Your OS version and hardware (run `uname -a && lsb_release -a`)

---

## Skill file conventions

When editing skill files, follow the existing patterns:

- Every command block is followed by "Paste the output" — do not add commands that aren't verified
- Phase headers use the format `> **Phase N of 8 — Name**`
- Completion checklists use `- [ ]` items with the verification command inline
- Re-entry instructions are in the phase header blockquote
- Always use `systemctl --user` (not `sudo systemctl`) for OpenClaw service commands
- Always prefix openclaw commands with the nvm load line or reference it explicitly

---

## Test reports

If you run the kit on new hardware or OS, please add an entry to TESTING.md under "Part 3 — Ongoing validation" using the template there. A real test report, even if incomplete, is more valuable than theoretical coverage.

---

## Code of conduct

Be direct and constructive. Reports of broken steps are the most useful contribution. Treat other contributors' real-world test findings as evidence, not opinion.
