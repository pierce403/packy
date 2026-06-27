# Packy

Packy is an early local-first desktop AI friend for safer software installs. The intended product is a dock/tray companion that helps users inspect package-manager commands, installers, scripts, and software supply-chain risk before approving risky steps.

The current repository contains the static GitHub Pages site, agent operating notes, an architecture document, and a first dependency-free command-risk analyzer. Do not describe install-watching, package verification, signature checks, desktop notifications, or blocking behavior as shipped until implementation code exists.

## Project Site

The GitHub Pages entry point is [index.html](index.html). It is a plain static page with no build step.

Production URL: <https://packy.bot/>

Primary logo asset: [assets/packy-elephant-logo.png](assets/packy-elephant-logo.png)

Preview locally by opening `index.html` in a browser.

## Architecture

Read [ARCHITECTURE.md](ARCHITECTURE.md) for the current architecture map, planned desktop assistant scope, security model, local data-store direction, and roadmap.

## Prototype Analyzer

The first implementation slice is a local, deterministic analyzer for install command text. It does not execute commands, fetch URLs, inspect the host system, or call a model.

```bash
python3 -m packy inspect 'brew install jq'
python3 -m packy inspect --json 'sudo npm install -g example'
```

High and critical findings intentionally return exit code `1` so scripts can gate risky commands.

## Product Direction

- Desktop companion first: Packy should feel like a local dock/tray friend, not a CLI-first tool.
- Local-first by default: install history, package lists, shell commands, and machine state should stay on device unless the user opts in.
- Security-conscious: Packy should warn about remote shell installers, unsigned binaries, global npm installs, pip-as-root, typosquatting, suspicious postinstall scripts, new services/daemons, PATH edits, and risky dependency chains.
- Honest status: public copy should use "planned", "designed to", "aims to", or "early direction" for capabilities that are not implemented.

## Agent Setup

- [AGENTS.md](AGENTS.md) is the canonical instruction file for coding agents.
- [SKILLS.md](SKILLS.md) indexes repo-local reusable procedures.
- [skills/curator/SKILL.md](skills/curator/SKILL.md) maintains the skill library when Packy workflows become repeatable.

## Verification

```bash
python3 -m unittest
python3 /home/pierce/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/curator
xmllint --html --noout index.html
git diff --check
```
