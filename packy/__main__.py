"""Command-line entry point for the first Packy analyzer slice."""

from __future__ import annotations

import argparse
import json
import sys

from .analyzer import analyze_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="packy",
        description="Inspect install commands for common local software-supply-chain risks.",
    )
    subparsers = parser.add_subparsers(dest="command_name")

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Analyze an install command without executing it.",
    )
    inspect_parser.add_argument(
        "command",
        nargs="*",
        help="Command text to inspect. If omitted, Packy reads stdin.",
    )
    inspect_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report.",
    )

    args = parser.parse_args(argv)
    if args.command_name != "inspect":
        parser.print_help(sys.stderr)
        return 2

    command_text = " ".join(args.command).strip()
    if not command_text and not sys.stdin.isatty():
        command_text = sys.stdin.read().strip()

    report = analyze_command(command_text)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(_format_report(report))

    return 0 if report.risk_level in {"info", "low", "medium"} else 1


def _format_report(report) -> str:
    lines = [
        f"Risk: {report.risk_level}",
        report.summary,
    ]
    if report.findings:
        lines.append("")
        lines.append("Findings:")
        for finding in report.findings:
            lines.extend(
                [
                    f"- [{finding.severity}] {finding.title}",
                    f"  Evidence: {finding.evidence}",
                    f"  Why: {finding.why_it_matters}",
                    f"  Safer path: {finding.recommendation}",
                ]
            )
    lines.append("")
    lines.append("Next steps:")
    lines.extend(f"- {step}" for step in report.next_steps)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
