#!/usr/bin/env python3
# Copyright (C) 2026 Paul Monday
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""Kindle Template Generator — generate PDF templates for Kindle Scribe."""

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def _parse_cover_tokens(tokens: list) -> dict:
    """Parse ['key:value', ...] tokens into a dict. Skips entries without ':'."""
    result = {}
    for token in tokens:
        if ":" in token:
            k, _, v = token.partition(":")
            result[k.strip()] = v.strip()
    return result


def discover_templates() -> dict:
    """Scan templates/ for subdirectories containing template.py."""
    templates = {}
    templates_dir = ROOT / "templates"
    for item in sorted(templates_dir.iterdir()):
        entry = item / "template.py"
        if item.is_dir() and entry.exists():
            spec = importlib.util.spec_from_file_location(
                f"templates.{item.name}.template", entry
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            templates[item.name] = mod
    return templates


def print_catalog(templates: dict) -> None:
    print()
    print("  Kindle Template Generator")
    print("  " + "─" * 38)
    print()
    for i, (key, mod) in enumerate(templates.items(), 1):
        m = mod.METADATA
        print(f"  {i}.  {m['name']}")
        print(f"       {m['description']}")
        print(f"       {m['pages']} pages  •  default output: {m['output']}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Kindle Scribe PDF template.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("template", nargs="?",
                        help="Template name (e.g. scorecard). Omit for interactive menu.")
    parser.add_argument("-o", "--output",
                        help="Output file path (overrides template default).")
    parser.add_argument("--list", action="store_true",
                        help="List available templates and exit.")
    parser.add_argument("--cover", nargs="*", metavar="key:value",
                        help=(
                            "Generate a cover page. Omit values for interactive prompts, "
                            "or pass key:value pairs e.g. --cover visitor:Mets home:Rockies"
                        ))
    parser.add_argument(
        "--params", nargs="*", metavar="key:value",
        help=(
            "Pass template parameters. Omit values for interactive prompts, "
            "or pass key:value pairs e.g. --params first_day:Monday days:7"
        ),
    )
    args = parser.parse_args()

    templates = discover_templates()
    if not templates:
        print("No templates found in templates/")
        sys.exit(1)

    if args.list:
        print_catalog(templates)
        return

    if not args.template:
        print_catalog(templates)
        keys = list(templates.keys())
        try:
            raw = input("  Enter template number or name: ").strip()
            try:
                args.template = keys[int(raw) - 1]
            except (ValueError, IndexError):
                args.template = raw.lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

    if args.template not in templates:
        print(f"\n  Unknown template: '{args.template}'")
        print(f"  Run with --list to see available templates.\n")
        sys.exit(1)

    mod = templates[args.template]
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = args.output or str(output_dir / mod.METADATA["output"])

    # Collect cover metadata
    cover_meta = {}
    cover_fields = mod.METADATA.get("cover_fields", [])
    if args.cover is not None and cover_fields:
        provided = _parse_cover_tokens(args.cover)
        needs_prompt = [f for f in cover_fields if f["name"] not in provided]
        if needs_prompt:
            print("\n  Cover page:")
        for field in cover_fields:
            name = field["name"]
            if name in provided:
                val = provided[name]
            else:
                default = field.get("default", "")
                prompt = f"  {field['prompt']}"
                if default:
                    prompt += f" [{default}]"
                prompt += ": "
                try:
                    val = input(prompt).strip() or default
                except (EOFError, KeyboardInterrupt):
                    val = default
            if val:
                cover_meta[name] = val

    # Resolve template-level params defined in METADATA["template_fields"]
    params_meta = {}
    template_fields = mod.METADATA.get("template_fields", [])
    if template_fields:
        provided = _parse_cover_tokens(args.params or [])
        needs_prompt = [f for f in template_fields if f["name"] not in provided]
        if needs_prompt:
            print("\n  Template options:")
        for field in template_fields:
            name = field["name"]
            if name in provided:
                val = provided[name]
            else:
                default = field.get("default", "")
                prompt = f"  {field['prompt']}"
                if default:
                    prompt += f" [{default}]"
                prompt += ": "
                try:
                    val = input(prompt).strip() or default
                except (EOFError, KeyboardInterrupt):
                    val = default
            if val:
                params_meta[name] = val

    print(f"\n  Generating {mod.METADATA['name']} …")
    mod.generate(output_path, **params_meta, **cover_meta)

    if cover_meta:
        try:
            from core.thumbnail import embed_cover_thumbnail
            embed_cover_thumbnail(output_path)
            print("  Cover thumbnail embedded.")
        except Exception as e:
            print(f"  Note: cover thumbnail skipped — {e}")

    print(f"  Saved: {output_path}\n")


if __name__ == "__main__":
    main()
