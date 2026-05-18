# AGENTS.md — STEMAIDE Docs

MkDocs documentation site for STEMAIDE, an Arduino/electronics STEM curriculum for African learners.

## Commands

```bash
pip install -r requirements.txt && pip install pyyaml
python scripts/validate_nav.py   # ensures every .md is in mkdocs.yml nav
python scripts/lint_cpp.py       # lints C++/Arduino code blocks in .md files
mkdocs build --strict            # fails on warnings (broken links, etc.)
mkdocs serve                     # dev server
```

## CI

Runs on push/PR to `main`/`master` (`.github/workflows/ci.yml`). Pipeline order:
`validate_nav.py` → `lint_cpp.py` → `mkdocs build --strict`. Must pass all three.

## Content structure

- `docs/1.0/` — basic component missions (LED, buzzer, servo, sensors)
- `docs/2.0/` — combined circuit missions (ultrasonic+LED, etc.)
- `docs/3.0/` — smart system missions (parking, traffic, security)
- `docs/getting-started/`, `docs/guides/` — setup, user guide, developer guide
- Images go in `docs/assets/`, CSS in `docs/stylesheets/extra.css`

New missions follow the Innovator's Journey format: problem → components → wiring → code → challenge (`docs/guides/developer-guide.md`). The expanded 7-section structure used in Level 3 missions is: Call to Adventure → Toolkit → Blueprint → Logic → Code → Troubleshooting → Extensions.



## Quirks

- `site/` (built output) is committed to git — do not add to `.gitignore`
- `.agent/` is gitignored (local-only writing-style config for narrative content)
- `pyyaml` is a separate install from `requirements.txt` (needed by validation scripts)
- UK English, learner-as-protagonist, narrative-driven instruction style
- All missions use placeholder GIF references (`Placeholder_for_*.gif`) and placeholder wiring diagram links — these are intentional and standard across the entire curriculum
- `mkdocs build --strict` produces ~60 pre-existing warnings from placeholder images in existing missions; a new mission following the same placeholder pattern does not regress the build
- Individual mission files are not in `mkdocs.yml` nav (only version index pages); `validate_nav.py` will flag them. When adding a new Level 3 mission, add it to the nav alongside `version3.md` to reduce the gap

## Quirks

- `site/` (built output) is committed to git — do not add to `.gitignore`
- `.agent/` is gitignored (local-only writing-style config for narrative content)
- `pyyaml` is a separate install from `requirements.txt` (needed by validation scripts)
- UK English, learner-as-protagonist, narrative-driven instruction style

## Agent config

`opencode.json` does not exist. This file (`AGENTS.md`) is the single agent configuration point.
