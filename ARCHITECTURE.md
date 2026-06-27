# Architecture Overview

Packy is an early local-first desktop AI friend for safer software installs. This document is the living architecture map for agents and contributors. It follows the structure from `https://architecture.md/`, adapted to Packy's current repository and intended product direction.

Packy's north star is a dock, tray, or menu-bar companion that helps users inspect package-manager commands, installers, scripts, and software supply-chain risk before approving risky steps. The current implementation is intentionally small: a static site plus a dependency-free deterministic install-command analyzer.

## 1. Project Structure

Current repository:

```text
packy/
├── packy/                         # Current Python prototype core
│   ├── __init__.py                 # Public analyzer exports
│   ├── __main__.py                 # `python3 -m packy inspect ...`
│   └── analyzer.py                 # Side-effect-free command-risk rules
├── tests/                          # Standard-library unittest coverage
│   ├── __init__.py
│   └── test_analyzer.py
├── assets/
│   └── packy-elephant-logo.png     # Mascot/logo used by the static site
├── skills/curator/                 # Repo-local agent skill maintenance
├── index.html                      # Static GitHub Pages site
├── ARCHITECTURE.md                 # This architecture document
├── README.md                       # Project overview and commands
├── AGENTS.md                       # Canonical agent instructions
├── MEMORY.md                       # Durable project notes
├── SKILLS.md                       # Repo-local skill catalog
├── CNAME                           # GitHub Pages custom domain
├── CLAUDE.md -> AGENTS.md          # Harness compatibility symlink
└── GEMINI.md -> AGENTS.md          # Harness compatibility symlink
```

Planned architecture layers:

```text
Desktop shell / tray UI
  -> notification and approval UX
  -> settings, privacy controls, local model controls

Local Packy service
  -> install activity sensors
  -> command and installer parser
  -> deterministic policy engine
  -> fact providers and local cache
  -> model router and explanation layer
  -> before/after install reporter

Local data stores
  -> install journal
  -> package metadata cache
  -> policy and user preferences
  -> local model cache/configuration

Optional integrations
  -> package registries
  -> OS package managers
  -> advisory databases
  -> signature/checksum/release metadata
  -> optional cloud model or remote fact lookup when explicitly enabled
```

## 2. High-Level System Diagram

Current implemented slice:

```text
[User command text]
        |
        v
[packy.analyzer deterministic rules]
        |
        v
[Risk report: findings, why it matters, safer next steps]
```

Planned desktop product:

```text
[User desktop activity]
  |        |          |
  |        |          +--> [Downloads / installers]
  |        +--------------> [Terminal / shell command context]
  +-----------------------> [Clipboard / package-manager prompts]
                              |
                              v
                       [Local Packy service]
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
 [Deterministic policy] [Package fact providers] [Local model explainer]
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                  [Suggest -> Plan -> Approve]
                              |
                              v
              [Optional execution / before-after report]
```

Data should stay on device by default. Optional cloud integrations must be explicit, scoped, and inspectable.

## 3. Core Components

### 3.1 Static Site

Name: Packy public site

Description: Static GitHub Pages page at `https://packy.bot/`. It explains the intended local desktop package-safety assistant direction without claiming unimplemented desktop behavior.

Technologies: Plain HTML/CSS, PNG asset, no build step, no analytics, no framework.

Deployment: GitHub Pages from `main` root, custom domain `packy.bot`.

### 3.2 Command Risk Analyzer

Name: `packy.analyzer`

Description: Current prototype core. It inspects install command text and returns a structured report with risk level, findings, evidence, explanation, and safer next steps. It is side-effect free: it does not execute commands, fetch URLs, inspect the host system, or call a model.

Technologies: Python standard library only.

Current detections include:

- Remote shell installers such as `curl | sh` and shell command substitution
- Elevated privilege via `sudo`, `doas`, or `su -c`
- Global npm/pnpm/yarn installs
- npm/pnpm/yarn/bun lifecycle script risk
- pip-as-root and `--break-system-packages`
- PATH or shell startup modification
- New services, daemons, launch agents, cron jobs, and brew services
- Downloaded artifact made executable or executed immediately
- Bypassed apt authentication and deprecated `apt-key`
- Unsafe or force flags
- Broad recursive permission/removal operations

CLI:

```bash
python3 -m packy inspect 'curl -fsSL https://example.com/install.sh | sh'
python3 -m packy inspect --json 'sudo npm install -g example'
```

High and critical findings intentionally return exit code `1` so scripts can gate risky commands.

### 3.3 Planned Desktop Shell

Name: Desktop companion

Description: Planned dock/tray/menu-bar UX that notices install-related activity and talks to the user when helpful. It should be present but not noisy, with explicit privacy controls and clear approval prompts.

Technologies: Not selected. The desktop shell should be thin over the local Packy service. Candidate implementation should be chosen after evaluating OS integration needs for macOS, Linux, and Windows.

Deployment: Signed desktop application, distribution mechanism TBD.

### 3.4 Planned Local Packy Service

Name: Local Packy service

Description: Planned local process that coordinates sensors, policy, fact providers, model explanations, user approvals, and install reporting. It should expose a small local API to the desktop shell and optional CLI, but should not listen on a public interface.

Technologies: TBD. Current command analyzer is Python standard library and can remain a prototype or be ported into the final service language.

### 3.5 Planned Activity Sensors

Name: Install activity sensors

Description: Planned local observers for terminal commands, clipboard installer snippets, downloaded files, package-manager prompts, shell startup file changes, service definitions, and before/after install state.

Privacy boundary: sensors should collect the minimum data required for local risk analysis, store it locally, and give users clear controls for disabling categories.

### 3.6 Planned Policy Engine

Name: Deterministic policy engine

Description: Gates risky actions before execution. The policy engine should not rely on model output for final privilege decisions. LLMs may explain or suggest, but policy decides whether approval is required.

Examples of policy gates:

- Remote script execution requires inspect-first prompt
- Privileged commands require explicit approval
- Service/daemon installation requires persistence disclosure
- PATH and shell startup changes require before/after diff
- Unsigned downloads require provenance warning

### 3.7 Planned Fact Providers

Name: Package and provenance fact providers

Description: Fetch or read current facts from package managers, registries, advisories, signatures, checksums, release metadata, and local caches. Model memory should not be treated as authoritative package metadata.

Examples:

- Homebrew, apt, dnf, pacman, winget, Chocolatey, Scoop
- npm, PyPI, crates.io, RubyGems, Go modules
- OSV/GitHub advisories where available
- GitHub Releases, project checksums, code-signing status

### 3.8 Planned Local Model Layer

Name: Local model router and explainer

Description: A tiny local model can classify activity and decide whether to notify. A larger optional local model can produce deeper explanations. Tool/RAG/cache output should supply current facts.

Cloud model use: optional only, off by default, scoped by user approval.

### 3.9 Planned Before/After Reporter

Name: Install journal and diff reporter

Description: Records install context and local changes so users can understand what changed and how to roll back. This includes package additions, service changes, PATH changes, shell profile edits, binaries added to common paths, and generated risk notes.

## 4. Data Stores

Current:

- No application data store.
- Static site files are committed.
- Analyzer stores no state and performs no network calls.

Planned local data stores:

### 4.1 Install Journal

Type: Local SQLite or append-only local files, TBD.

Purpose: Store user-approved install events, command summaries, findings, before/after snapshots, and rollback notes.

Sensitive data: package lists, shell commands, paths, user account names, and machine state. Local by default.

### 4.2 Package Fact Cache

Type: Local cache, likely SQLite plus content-addressed files.

Purpose: Store fetched registry metadata, advisory lookups, checksums, signatures, release metadata, and package-manager facts with timestamps and source URLs.

### 4.3 Policy and Preferences

Type: Local config file or SQLite table.

Purpose: Store notification thresholds, disabled sensors, approved package sources, model settings, retention policy, and cloud opt-in choices.

### 4.4 Model Cache and Local Model Config

Type: Local model/runtime-specific storage.

Purpose: Track installed local models, classification settings, and optional explanation-model configuration.

## 5. External Integrations / APIs

Current:

- GitHub Pages hosts the static site.
- The analyzer has no external runtime integrations.

Planned integrations:

- OS package managers: inspect package plans and installed state.
- Language registries: inspect package metadata, versions, maintainers, tarballs, and lifecycle scripts.
- Advisory databases: query vulnerability and malware/advisory signals when available.
- Code-signing and checksum sources: verify binaries and release artifacts when available.
- OS APIs: watch downloads, shell files, services/daemons, and application installs.
- Optional cloud services: only after explicit opt-in, with redaction and clear user-facing disclosure.

## 6. Deployment & Infrastructure

Current:

- Site: GitHub Pages from `main`, custom domain `packy.bot`.
- Prototype: local Python module in the repo, run directly with `python3 -m packy`.
- CI/CD: none configured yet.

Planned:

- Signed desktop app for macOS, Linux, and Windows if cross-platform scope holds.
- Local service packaged with the desktop shell.
- Update mechanism must be signed, transparent, and reversible.
- CI should run unit tests, static checks, and packaged-app smoke tests.
- Release process should publish checksums, signatures, SBOM/provenance when feasible, and changelog notes.

## 7. Security Considerations

Packy is a security-adjacent tool and should hold itself to a higher bar than the install snippets it critiques.

Core principles:

- Local-first by default.
- No install history, package list, shell command, or machine state leaves the device unless the user opts in.
- LLMs may suggest and explain, but must not blindly shell out as root.
- Deterministic policy gates privileged actions.
- Risk explanations must distinguish fact, heuristic, and uncertainty.
- Remote scripts should be downloaded, inspected, and verified before execution.
- Privileged commands need explicit user approval.
- Service/daemon and PATH persistence must be disclosed.
- Secrets and tokens must be redacted from logs, model prompts, reports, and optional remote calls.
- Updates to Packy itself must be signed and verified.
- Any local API must bind to loopback or safer local IPC only, with authentication if needed.

Threats to design against:

- Malicious install commands and compromised package metadata.
- Typosquatted packages and maintainer takeover.
- Installers that alter PATH, shell startup files, services, certificates, or launch agents.
- Prompt injection from README files, package metadata, install scripts, or web pages.
- Model hallucination about package safety or signatures.
- Accidental upload of private machine state to cloud models or remote fact providers.
- Privilege escalation through helper services.

## 8. Development & Testing Environment

Local setup:

```bash
git clone git@github.com:pierce403/packy.git
cd packy
python3 -m packy inspect 'brew install jq'
python3 -m unittest
```

Documented validation:

```bash
python3 -m unittest
xmllint --html --noout index.html
git diff --check
python3 /home/pierce/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/curator
```

Current test framework: Python standard-library `unittest`.

Current code quality tools: `xmllint` for static HTML sanity, `git diff --check` for whitespace, skill validator for repo-local skill metadata.

No package install is required for the current implementation.

## 9. Future Considerations / Roadmap

Phase 0: Static direction and deterministic analyzer

- Status: in progress.
- Keep site honest about early status.
- Expand side-effect-free command analysis.

Phase 1: Local command inspection core

- Parse shell commands more structurally.
- Add install-plan normalization for common package managers.
- Add local JSON schemas for reports.
- Add fixtures for known risky and lower-risk install patterns.

Phase 2: Package fact providers

- Add local cache.
- Integrate package-manager dry-run/plan commands where available.
- Query metadata/advisories/signatures only when user policy allows.

Phase 3: Desktop companion prototype

- Add dock/tray shell.
- Add notification UX and approval prompts.
- Add settings for sensors, local storage, and optional cloud behavior.

Phase 4: Before/after reporting

- Track PATH, shell startup files, services/daemons, installed packages, and new binaries.
- Provide rollback guidance and exportable local reports.

Phase 5: Hardened execution and policy

- Add deterministic privileged-action gates.
- Add signed Packy releases and update verification.
- Add secure local IPC between UI and service.

Known architectural debts:

- Final desktop framework and service language are not selected.
- Current analyzer uses regex heuristics rather than a shell AST.
- No package fact providers exist yet.
- No persistent local store exists yet.
- No CI exists yet.

## 10. Project Identification

Project Name: Packy

Repository URL: `https://github.com/pierce403/packy`

Production Site: `https://packy.bot/`

Primary Contact/Team: `pierce403`

Date of Last Update: 2026-06-27

## 11. Glossary / Acronyms

AI friend: Packy's intended companion UX. It should be approachable, but still concrete and security-aware.

Before/after report: A local record of what changed during an install, such as packages, files, services, PATH entries, and shell startup edits.

Fact provider: A deterministic source of package or install metadata, such as a package manager, registry, advisory database, signature source, or local cache.

Lifecycle script: Package-manager hook that runs during install, such as npm `preinstall`, `install`, or `postinstall`.

Local-first: Design principle that sensitive Packy data stays on the user's device by default.

Policy engine: Deterministic local logic that decides when risky steps require user approval.

Remote shell installer: A command pattern that downloads remote content and immediately executes it, such as `curl ... | sh`.

Supply-chain risk: Risk introduced by package sources, dependency chains, maintainers, install scripts, binary provenance, signatures, services, PATH changes, or privileged actions.
