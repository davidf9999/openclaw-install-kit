#!/usr/bin/env python3
"""
Validates kit.md frontmatter schema and checks that all referenced skill files exist.
Run from the repo root: python .github/scripts/validate_kit.py
"""

import sys
import os
import yaml

REQUIRED_FIELDS = ['schema', 'slug', 'title', 'version', 'skills']
REQUIRED_SKILL_FIELDS = []  # reserved for future per-skill validation

errors = []
warnings = []


def load_frontmatter(path):
    with open(path) as f:
        content = f.read()
    if not content.startswith('---'):
        errors.append(f"{path}: missing YAML frontmatter (file must start with ---)")
        return None
    try:
        end = content.index('---', 3)
    except ValueError:
        errors.append(f"{path}: frontmatter block not closed (missing closing ---)")
        return None
    try:
        return yaml.safe_load(content[3:end])
    except yaml.YAMLError as e:
        errors.append(f"{path}: YAML parse error — {e}")
        return None


def validate_kit(fm):
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"kit.md: missing required field '{field}'")

    if 'schema' in fm and fm['schema'] != 'kit/1.0':
        warnings.append(f"kit.md: schema is '{fm['schema']}', expected 'kit/1.0'")

    if 'skills' not in fm:
        return
    if not isinstance(fm['skills'], list):
        errors.append("kit.md: 'skills' must be a list")
        return

    for skill_path in fm['skills']:
        if not os.path.exists(skill_path):
            errors.append(f"kit.md: skill file not found: {skill_path}")
        else:
            validate_skill_file(skill_path)


def validate_skill_file(path):
    with open(path) as f:
        content = f.read()
    # Check for phase header pattern
    if '> **Phase' not in content:
        warnings.append(f"{path}: no phase header found (expected '> **Phase N of 8 ...**')")
    # Check for completion check section (orientation intentionally has none)
    no_completion_needed = {'skills/00-orientation.md'}
    has_completion = any(h in content for h in [
        '## Completion check', '## Completion', '## Final verification', '## Final check'
    ])
    if not has_completion and path not in no_completion_needed:
        warnings.append(f"{path}: no completion check section found")


# --- Run ---
fm = load_frontmatter('kit.md')
if fm:
    validate_kit(fm)

if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  ✗ {e}")
if warnings:
    print("WARNINGS:")
    for w in warnings:
        print(f"  ⚠ {w}")

if not errors and not warnings:
    skills = fm.get('skills', [])
    print(f"✓ kit.md valid — {len(skills)} skill(s) referenced and present")
    for s in skills:
        print(f"  {s}")
elif not errors:
    print(f"\nPassed with {len(warnings)} warning(s).")

if errors:
    sys.exit(1)
