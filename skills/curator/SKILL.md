---
name: curator
description: Maintain Packy's repo-local skill library by creating, revising, consolidating, and pruning skills. Use when Packy work reveals a repeated workflow, a durable procedure, stale skill guidance, or a lesson that may belong in SKILLS.md or a skill folder instead of only AGENTS.md or MEMORY.md.
---

# Curator

## Overview

Use this skill to keep Packy's reusable agent procedures small, accurate, and discoverable. The goal is a compact skill library that helps future agents repeat real workflows without turning every one-off note into a skill.

## Workflow

1. Decide whether the lesson is reusable.
   - Put project-wide operating rules in `AGENTS.md`.
   - Put durable observations, collaborator cues, and one-off findings in `MEMORY.md`.
   - Put repeated procedures with steps, validations, or assets in `skills/<name>/SKILL.md`.
2. Search `SKILLS.md` and `skills/` before creating anything new.
3. Update an existing skill when the workflow is already covered.
4. Create a new skill only when the procedure has a clear trigger and future use.
5. Prune or consolidate stale skills when they overlap or no longer match Packy's workflow.
6. Update `SKILLS.md` whenever the available skill set changes.
7. Keep `agents/openai.yaml` aligned with the skill name, purpose, and default prompt.
8. Validate before committing:

```bash
python3 /home/pierce/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<name>
git diff --check
```

## Skill Standards

- Keep frontmatter to `name` and `description`.
- Put all trigger guidance in the description so agents can decide whether to load the skill.
- Keep the body procedural and concise.
- Add `scripts/`, `references/`, or `assets/` only when they directly support the skill.
- Delete generated TODO text before committing.
- Do not create auxiliary README, changelog, or quick-reference files inside a skill.

## Naming

Use lowercase hyphenated names under 64 characters. Prefer short names that describe the action or workflow, such as `publish-site-change` or `package-install-audit`.

## Commit Criteria

Before landing skill changes, the relevant skill validates, `SKILLS.md` lists the current skill set, and `AGENTS.md` or `MEMORY.md` reflects any broader operating lesson.
