import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from . import __version__
from .core import compare, parse_env


def make_parser():
    parser = argparse.ArgumentParser(
        prog="dotenv-doctor",
        description="Check that a .env file has everything .env.example asks for.",
    )
    parser.add_argument("--env", default=".env")
    parser.add_argument("--example", default=".env.example")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="also fail on extra, empty and duplicate keys",
    )
    parser.add_argument(
        "--allow-empty",
        action="append",
        default=[],
        metavar="KEY",
        help="key that is allowed to be blank (can be repeated)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def print_report(report, env_path, example_path, strict):
    soft = "ERROR" if strict else "WARN"
    checks = [
        ("ERROR", report.missing, f"missing from {env_path}"),
        (soft, report.extra, f"not in {example_path}"),
        (soft, report.empty, "empty values"),
        (soft, report.duplicates, "duplicate keys"),
    ]

    found_something = False
    for level, keys, label in checks:
        if keys:
            found_something = True
            print(f"[{level}] {label} ({len(keys)}): {', '.join(keys)}")

    if not found_something:
        print(f"OK: {env_path} matches {example_path}")


def main(argv=None):
    args = make_parser().parse_args(argv)

    try:
        example = parse_env(Path(args.example).read_text(encoding="utf-8-sig"))
        env = parse_env(Path(args.env).read_text(encoding="utf-8-sig"))
    except FileNotFoundError as err:
        print(f"error: file not found: {err.filename}", file=sys.stderr)
        return 2

    report = compare(example, env, args.allow_empty)
    failed = report.failed(args.strict)

    if args.format == "json":
        print(json.dumps({**asdict(report), "ok": not failed}, indent=2))
    else:
        print_report(report, args.env, args.example, args.strict)

    return 1 if failed else 0
