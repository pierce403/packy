# Packy

Packy is a local-first AI package management system with an elephant theme. The project is currently a public static project page plus agent operating notes; implementation code should preserve the local-first promise as it lands.

## Project Site

The GitHub Pages entry point is [index.html](index.html). It is a plain static page with no build step.

Preview locally by opening `index.html` in a browser.

## Agent Setup

- [AGENTS.md](AGENTS.md) is the canonical instruction file for coding agents.
- [SKILLS.md](SKILLS.md) indexes repo-local reusable procedures.
- [skills/curator/SKILL.md](skills/curator/SKILL.md) maintains the skill library when Packy workflows become repeatable.

## Verification

```bash
python3 /home/pierce/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/curator
xmllint --html --noout index.html
git diff --check
```
