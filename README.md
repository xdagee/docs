# STEMAIDE Docs

Documentation site for the [STEMAIDE](https://stemaide.com) Arduino/electronics STEM curriculum — narrative-driven missions that teach young African learners (ages 10–14) to build real electronic systems.

Built with [MkDocs](https://www.mkdocs.org/) + [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Curriculum

| Level | Name | Focus |
|---|---|---|
| 1 | The Lab | Basic components: LED, buzzer, servo, sensors |
| 2 | The Neighbourhood | Combined circuits: street lights, alarms, smart gates |
| 3 | The Smart City | Smart systems: parking, traffic, security, **irrigation** |

## Recent changes

- **New mission: Smart Irrigation (3.7)** — "The Smart Farm" introduces multi-threshold analog decision logic using an LDR as a soil moisture proxy with 3-state LED feedback and servo-actuated valve control.
- **Level 3 nav added** — The Smart City section now appears in the navigation alongside Manual 3.0 and the new mission.

## Quick start

```bash
pip install -r requirements.txt && pip install pyyaml
mkdocs serve              # dev server at http://127.0.0.1:8000
```

## CI pipeline

Push/PR to `main`/`master` runs (`.github/workflows/ci.yml`):

1. `python scripts/validate_nav.py` — every `.md` must be in `mkdocs.yml` nav
2. `python scripts/lint_cpp.py` — lints Arduino code blocks in markdown
3. `mkdocs build --strict` — fails on warnings (broken links, etc.)

**Note:** `mkdocs build --strict` produces ~60 pre-existing warnings from placeholder images in existing missions. These are intentional — every mission uses placeholder GIF references to be replaced with real content later. New missions following the same convention do not regress the build.

## Writing conventions

- UK English, second person, present tense
- Learner-as-protagonist narrative style ("you")
- Level 3 missions use a 7-section structure: Call to Adventure → Toolkit → Blueprint → Logic → Code → Troubleshooting → Extensions
- Level 1/2 missions use the 5-section Innovator's Journey

See [`AGENTS.md`](./AGENTS.md) for build commands, CI details, and project quirks. See [`docs/guides/developer-guide.md`](./docs/guides/developer-guide.md) for mission authoring guidelines.
