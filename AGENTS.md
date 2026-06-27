# AGENTS.md - Instructions for Coding Agents

## Self-Improvement Directive

When working on Packy, update this file whenever you learn something important that future agents should not have to rediscover. Capture both successes to repeat and failures to avoid. Include collaborator preferences when they are useful and appropriate.

Record:

- Verified build, test, preview, and publish commands
- Project conventions and naming patterns
- Common errors and their fixes
- Dependencies, tools, and local setup requirements
- Positive or negative results from experiments
- Navigation tips for the repository
- Collaboration preferences observed during work

## Persona, Rapport & Operating Context

Packy is an early local-first desktop AI friend for safer software installs. The intended UX is a dock, tray, or menu-bar companion that notices install-related activity, explains software supply-chain risk, and asks before risky steps. The elephant mascot can stay friendly, but the product value is security and safer installs, not a generic elephant-themed package manager.

When this file is first read with the human, introduce yourself by name if you have one. If your responsibilities are unclear, ask before assuming ownership of unrelated work.

## Responsibilities

- Keep Packy's public project page accurate and easy to scan.
- Preserve the local-first desktop companion positioning in docs and implementation decisions.
- Avoid claiming install-watching, package verification, command execution, signature checks, or blocking behavior before it exists in code.
- Keep Packy's copy concrete about install risk: `curl | sh`, unsigned binaries, global npm installs, pip-as-root, typosquatting, suspicious postinstall scripts, new daemons/services, PATH edits, and risky dependency chains.
- Maintain repo-local guidance in `AGENTS.md`, `MEMORY.md`, `SKILLS.md`, and `skills/`.
- Verify changes before committing and pushing.

## Project Overview

This repository currently hosts a static GitHub Pages site for Packy. The page describes the intended product direction: a local-first desktop package-safety assistant. Implementation code has not landed yet, so public copy must be explicit when something is planned rather than shipped.

Important files:

- `index.html`: static public page served by GitHub Pages
- `README.md`: short project overview and verification commands
- `AGENTS.md`: canonical agent instructions
- `MEMORY.md`: compact map for durable notes
- `SKILLS.md`: compact index of reusable repo-local skills
- `skills/curator/SKILL.md`: skill maintenance workflow

## Build & Test Commands

There is no build step yet. Validate the current repo with:

```bash
python3 /home/pierce/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/curator
xmllint --html --noout index.html
git diff --check
```

Open `index.html` directly in a browser for local preview.

## Coding Conventions

- Prefer static, dependency-free files until Packy needs real application code.
- Keep public copy concrete: local-first privacy, desktop/dock companion UX, install inspection, package metadata, signatures, advisories, and supply-chain risk.
- Phrase unimplemented capabilities as "planned", "designed to", "aims to", or "early direction".
- Use the elephant mascot as branding and visual identity, while keeping security value obvious.
- Keep docs in plain Markdown and avoid generated boilerplate.
- Use ASCII unless a file already has a clear reason to use non-ASCII.

## Known Issues & Solutions

- Packy is scaffolded as a public project page. There is no package-manager implementation yet.
- The project should not describe install-watching, registry checks, command execution, signature verification, advisory lookups, local models, or policy gates as shipped until code backs them.
- The old generic "AI package management system" landing page was a placeholder and should not be preserved as product direction.
- The GitHub CLI may need to run outside the sandbox on this machine because `gh` is installed through snap.

## Agent Tips

- Search `AGENTS.md`, `MEMORY.md`, and `SKILLS.md` before broad repo work.
- Add reusable procedures to `skills/<name>/SKILL.md` only when a workflow is likely to repeat.
- Keep one-off findings in `MEMORY.md` or a memory note instead of turning every observation into a skill.
- When publishing site changes, verify HTML and push `main` so GitHub Pages can rebuild.

## Tooling Preferences

- Prefer CLI workflows that can be repeated and committed.
- Use `rg` for text and file searches.
- Use `gh` for GitHub repository and Pages operations.
- Use small scripts only when they reduce repeated manual work.

## Memory & Skills Structure

- Keep `MEMORY.md` as the compact map for durable notes, people, and logs.
- Keep `SKILLS.md` as the compact catalog for reusable procedures.
- Keep detailed procedure in `skills/<name>/SKILL.md`.
- Use `curator` as the default skill for creating, revising, consolidating, and pruning skills.

## Harness Compatibility

`AGENTS.md` is canonical. If another harness expects its own instruction file, use symlinks so every agent reads the same guidance:

```bash
ln -s AGENTS.md CLAUDE.md
ln -s AGENTS.md GEMINI.md
```

## Rapport & Reflection

- Note collaborator preferences, tone, and formatting asks when they materially improve future work.
- Keep this file concise as the context grows.
- Consolidate stale guidance instead of appending forever.
