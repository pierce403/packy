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

Packy is a local-first AI package management system with an elephant theme. Treat the theme as a clear product signal, not an excuse for vague copy or fake functionality.

When this file is first read with the human, introduce yourself by name if you have one. If your responsibilities are unclear, ask before assuming ownership of unrelated work.

## Responsibilities

- Keep Packy's public project page accurate and easy to scan.
- Preserve the local-first positioning in docs and implementation decisions.
- Avoid claiming package-manager capabilities before they exist in code.
- Maintain repo-local guidance in `AGENTS.md`, `MEMORY.md`, `SKILLS.md`, and `skills/`.
- Verify changes before committing and pushing.

## Project Overview

This repository currently hosts a static GitHub Pages site for Packy. The project description is intentionally product-level until implementation code is added.

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
- Keep public copy concrete: local-first, AI-assisted package management, transparent manifests, and user-owned state.
- Use the elephant theme as branding and visual identity, while keeping text practical.
- Keep docs in plain Markdown and avoid generated boilerplate.
- Use ASCII unless a file already has a clear reason to use non-ASCII.

## Known Issues & Solutions

- Packy is scaffolded as a public project page. There is no package-manager implementation yet.
- The project should not describe registry, install, or agent features as shipped until code backs them.
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
