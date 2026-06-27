"""Deterministic install-command risk analysis.

This module is intentionally local and side-effect free. It inspects command
text and returns structured findings; it does not execute commands, fetch URLs,
or inspect the host system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Iterable


SEVERITY_ORDER = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    title: str
    evidence: str
    why_it_matters: str
    recommendation: str


@dataclass(frozen=True)
class Report:
    command: str
    risk_level: str
    summary: str
    findings: list[Finding]
    next_steps: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "command": self.command,
            "risk_level": self.risk_level,
            "summary": self.summary,
            "findings": [asdict(finding) for finding in self.findings],
            "next_steps": self.next_steps,
        }


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str
    title: str
    pattern: re.Pattern[str]
    why_it_matters: str
    recommendation: str


def _compile(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)


RULES: tuple[Rule, ...] = (
    Rule(
        id="remote-shell-pipe",
        severity="critical",
        title="Remote script is piped directly into an interpreter",
        pattern=_compile(r"\b(curl|wget)\b[^|;\n]*https?://[^|;\n]+[|]\s*(sudo\s+)?(sh|bash|zsh|fish|python3?|ruby|perl)\b"),
        why_it_matters="The downloaded content can change between review and execution, and it runs before you inspect it.",
        recommendation="Download the script first, inspect it, verify the source, and prefer a signed package or official package manager when available.",
    ),
    Rule(
        id="remote-command-substitution",
        severity="critical",
        title="Remote content is executed through command substitution",
        pattern=_compile(r"\b(sh|bash|zsh|fish)\b[^;\n]*[$][(]\s*(curl|wget)\b[^)]*https?://"),
        why_it_matters="The shell executes whatever the remote server returns, which bypasses local review.",
        recommendation="Fetch the remote content to a file, inspect it, and run only the reviewed version if you still trust it.",
    ),
    Rule(
        id="root-privilege",
        severity="high",
        title="Command requests elevated privileges",
        pattern=_compile(r"(^|[;&|]\s*)(sudo|doas|su\s+-c)\b"),
        why_it_matters="A privileged installer can modify system directories, services, shells, certificates, and package-manager state.",
        recommendation="Understand exactly which steps require privilege and approve them separately after inspection.",
    ),
    Rule(
        id="npm-global-install",
        severity="high",
        title="Global JavaScript package install",
        pattern=_compile(r"\b(npm|pnpm)\s+(install|i|add)\b[^;&|\n]*(\s-g\b|\s--global\b)|\byarn\s+global\s+add\b"),
        why_it_matters="Global installs can put executables on PATH and may run package lifecycle scripts from the dependency tree.",
        recommendation="Prefer project-local installs, pinned versions, or a trusted package-manager formula when possible.",
    ),
    Rule(
        id="package-lifecycle-scripts",
        severity="medium",
        title="Package lifecycle scripts may run",
        pattern=_compile(r"\b(npm\s+(install|i)|pnpm\s+(install|add|i)|yarn\s+(install|add)|bun\s+(install|add))\b"),
        why_it_matters="JavaScript package managers can run install hooks from direct or transitive dependencies.",
        recommendation="Inspect package metadata and consider script-disabling options when installing unfamiliar packages.",
    ),
    Rule(
        id="pip-as-root",
        severity="high",
        title="Python package install appears to run as root",
        pattern=_compile(r"(^|[;&|]\s*)(sudo|doas)\s+((python3?|py)\s+-m\s+)?pip\s+install\b"),
        why_it_matters="Root Python installs can overwrite system-managed packages and place code into privileged import paths.",
        recommendation="Use a virtual environment, pipx, or a user-local install unless the system package manager explicitly requires otherwise.",
    ),
    Rule(
        id="pip-break-system-packages",
        severity="high",
        title="Python install bypasses system package protections",
        pattern=_compile(r"\bpip\s+install\b[^;&|\n]*--break-system-packages\b"),
        why_it_matters="This flag can override distribution safeguards that prevent pip from damaging system Python state.",
        recommendation="Use a virtual environment, pipx, or distribution package instead of bypassing the guardrail.",
    ),
    Rule(
        id="path-modification",
        severity="high",
        title="Command modifies shell startup or PATH",
        pattern=_compile(r"\bexport\s+PATH=|(\>\>|\btee\s+-a\b)[^;&|\n]*(\.bashrc|\.zshrc|\.profile|\.bash_profile|/etc/profile)|\bshellenv\b|\bsetx\s+PATH\b"),
        why_it_matters="PATH changes can make future shells run different binaries than the user expects.",
        recommendation="Review the exact PATH entry, prefer reversible edits, and record which startup file changes.",
    ),
    Rule(
        id="service-or-daemon",
        severity="high",
        title="Command may install or start a service",
        pattern=_compile(r"\b(systemctl\s+(enable|start)|launchctl\s+(load|bootstrap|enable)|brew\s+services\s+start|crontab\b|schtasks\b|sc\.exe\s+create)\b|/Library/Launch(Daemons|Agents)"),
        why_it_matters="Services and daemons persist beyond the install command and can run automatically in the background.",
        recommendation="Inspect the service definition, permissions, network behavior, and uninstall path before enabling it.",
    ),
    Rule(
        id="downloaded-binary-execution",
        severity="high",
        title="Downloaded file appears to be made executable",
        pattern=_compile(r"\b(curl|wget)\b[^;&|\n]*https?://[^;&|\n]*(;|&&)[^;&|\n]*chmod\s+(\+x|[0-7]*x)"),
        why_it_matters="A downloaded binary or script may be run without signature, checksum, or provenance checks.",
        recommendation="Verify checksums and signatures when available, inspect the source, and avoid running binaries from ad hoc URLs.",
    ),
    Rule(
        id="direct-local-execution-after-download",
        severity="high",
        title="Downloaded artifact appears to be executed immediately",
        pattern=_compile(r"\b(curl|wget)\b.*https?://.*(;|&&).*(\./|bash\s+|sh\s+)[A-Za-z0-9._/-]+"),
        why_it_matters="The command collapses download, trust decision, and execution into one step.",
        recommendation="Split the command into download, verify, inspect, and execute phases.",
    ),
    Rule(
        id="apt-unauthenticated",
        severity="critical",
        title="Package manager authentication is bypassed",
        pattern=_compile(r"\bapt(-get)?\b[^;&|\n]*(--allow-unauthenticated|trusted=yes)"),
        why_it_matters="Disabling package authentication removes a core supply-chain protection.",
        recommendation="Use signed repositories and verify the repository key fingerprint through an independent source.",
    ),
    Rule(
        id="deprecated-apt-key",
        severity="medium",
        title="Command uses apt-key",
        pattern=_compile(r"\bapt-key\s+add\b"),
        why_it_matters="apt-key is deprecated and can grant broad trust to repositories if used carelessly.",
        recommendation="Use a repository-specific keyring and signed-by configuration instead.",
    ),
    Rule(
        id="unsafe-permission-flag",
        severity="high",
        title="Command uses an unsafe permission or force flag",
        pattern=_compile(r"\b(--unsafe-perm|--allow-root|--force|-f)\b"),
        why_it_matters="Force and unsafe-permission flags often bypass checks that would otherwise stop risky installs.",
        recommendation="Find out which check is being bypassed and whether there is a safer install path.",
    ),
    Rule(
        id="broad-permission-change",
        severity="critical",
        title="Command makes broad filesystem permission changes",
        pattern=_compile(r"\b(chmod\s+-R\s+(777|a\+rw|a\+rwx)|chown\s+-R\b|rm\s+-rf\s+/)\b"),
        why_it_matters="Broad recursive permission or removal commands can damage system integrity or hide later compromise.",
        recommendation="Stop and inspect the path, scope, and reason before running any recursive privileged filesystem operation.",
    ),
)


def analyze_command(command: str) -> Report:
    command = command.strip()
    if not command:
        return Report(
            command="",
            risk_level="low",
            summary="No command was provided.",
            findings=[],
            next_steps=["Paste the install command you want Packy to inspect."],
        )

    findings = _dedupe(_find_matches(command))
    risk_level = _risk_level(findings)
    summary = _summary(risk_level, findings)
    return Report(
        command=command,
        risk_level=risk_level,
        summary=summary,
        findings=findings,
        next_steps=_next_steps(findings),
    )


def _find_matches(command: str) -> Iterable[Finding]:
    for rule in RULES:
        match = rule.pattern.search(command)
        if match:
            yield Finding(
                id=rule.id,
                severity=rule.severity,
                title=rule.title,
                evidence=_evidence(command, match),
                why_it_matters=rule.why_it_matters,
                recommendation=rule.recommendation,
            )


def _dedupe(findings: Iterable[Finding]) -> list[Finding]:
    seen: set[str] = set()
    unique: list[Finding] = []
    for finding in findings:
        if finding.id in seen:
            continue
        seen.add(finding.id)
        unique.append(finding)
    return sorted(unique, key=lambda item: (-SEVERITY_ORDER[item.severity], item.id))


def _risk_level(findings: list[Finding]) -> str:
    if not findings:
        return "low"
    return max(findings, key=lambda item: SEVERITY_ORDER[item.severity]).severity


def _summary(risk_level: str, findings: list[Finding]) -> str:
    if not findings:
        return "No obvious high-risk install pattern was detected. This is not a trust guarantee."
    count = len(findings)
    noun = "finding" if count == 1 else "findings"
    return f"{risk_level.capitalize()} risk: Packy found {count} install-safety {noun}."


def _next_steps(findings: list[Finding]) -> list[str]:
    if not findings:
        return [
            "Confirm the source is the official project or package manager.",
            "Prefer pinned versions and signed packages when available.",
            "Record what changed after install if you proceed.",
        ]

    ids = {finding.id for finding in findings}
    steps: list[str] = []
    if {"remote-shell-pipe", "remote-command-substitution", "direct-local-execution-after-download"} & ids:
        steps.append("Split download, inspection, verification, and execution into separate steps.")
    if {"downloaded-binary-execution", "apt-unauthenticated"} & ids:
        steps.append("Look for signatures, checksums, release provenance, or a trusted package-manager path.")
    if {"root-privilege", "pip-as-root", "broad-permission-change"} & ids:
        steps.append("Avoid privilege until you know exactly which files and services will change.")
    if {"npm-global-install", "package-lifecycle-scripts"} & ids:
        steps.append("Inspect package metadata and lifecycle scripts before installing unfamiliar packages.")
    if {"path-modification", "service-or-daemon"} & ids:
        steps.append("Identify persistence changes and the uninstall or rollback path.")
    steps.append("Save a before/after note for commands, files, services, and PATH changes if you continue.")
    return steps


def _evidence(command: str, match: re.Match[str]) -> str:
    start = max(0, match.start() - 32)
    end = min(len(command), match.end() + 32)
    snippet = command[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(command):
        snippet = snippet + "..."
    return snippet
