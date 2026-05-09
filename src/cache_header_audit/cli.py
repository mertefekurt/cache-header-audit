from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from urllib.error import URLError

from .auditor import audit_headers
from .reporter import render_json, render_table
from .transport import fetch_headers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cache-header-audit",
        description="Audit HTTP cache headers and score cache readiness.",
    )
    parser.add_argument("urls", nargs="+", help="HTTP or HTTPS URLs to audit")
    parser.add_argument(
        "--method",
        choices=("HEAD", "GET"),
        default="HEAD",
        help="request method used for the first probe",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=8.0,
        help="request timeout in seconds",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable JSON",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        metavar="SCORE",
        help="exit with status 2 when any URL scores below this value",
    )
    parser.add_argument(
        "--user-agent",
        default="cache-header-audit/0.1",
        help="User-Agent header sent with probes",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI colors in table output",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    results = []

    for url in args.urls:
        try:
            response = fetch_headers(
                url,
                method=args.method,
                timeout=args.timeout,
                user_agent=args.user_agent,
            )
        except (TimeoutError, URLError, OSError) as error:
            print(f"{url}: request failed: {error}", file=sys.stderr)
            return 1

        results.append(audit_headers(response.url, response.status, response.headers))

    if args.json:
        print(render_json(results))
    else:
        print(render_table(results, color=not args.no_color))

    if args.fail_under is not None and any(result.score < args.fail_under for result in results):
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
