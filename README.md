![Project Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=180&section=header&text=cache-header-audit&fontSize=50&fontAlignY=38)

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

# cache-header-audit

Fast CLI for scoring HTTP cache headers across production URLs.

| Output | Use case |
| --- | --- |
| Score + grade | Quick release checks |
| Primary issue | Actionable cache fixes |
| JSON mode | CI gates and dashboards |

![Terminal Output](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=400&size=14&duration=1500&pause=500&center=false&vCenter=false&multiline=true&width=600&height=200&lines=$+cache-header-audit+https://example.com+--no-color;https://example.com+++++25++++F++++missing+Cache-Control+header)

## Install

```bash
python3 -m pip install .
```

## Run

```bash
cache-header-audit https://example.com https://static.example.com/app.js
cache-header-audit https://example.com --json
cache-header-audit https://example.com --fail-under 75
```

## Code Snapshot

![Code Snippet](assets/code-snapshot.png)

## Architecture

```mermaid
flowchart LR
    A["CLI arguments"] --> B["transport.fetch_headers"]
    B --> C["auditor.audit_headers"]
    C --> D["cache-control parser"]
    C --> E["score + findings"]
    E --> F{"output mode"}
    F --> G["terminal table"]
    F --> H["JSON report"]
    E --> I["fail-under exit code"]
```

## CLI Reference

| Argument / flag | Default | Purpose |
| --- | ---: | --- |
| `urls` | required | One or more HTTP(S) URLs to inspect |
| `--method HEAD\|GET` | `HEAD` | First request method for probing headers |
| `--timeout SECONDS` | `8.0` | Network timeout per URL |
| `--json` | `false` | Print structured JSON |
| `--fail-under SCORE` | none | Exit with code `2` below the score |
| `--user-agent TEXT` | `cache-header-audit/0.1` | Custom probe user agent |
| `--no-color` | `false` | Disable ANSI grade colors |

## Scoring Signals

| Signal | Effect |
| --- | --- |
| `Cache-Control` present | positive |
| `max-age` / `s-maxage` | positive when useful |
| `ETag` / `Last-Modified` | positive validator coverage |
| `stale-while-revalidate` | positive resilience |
| `no-store`, `Vary: *` | strong negative |
| missing validators | warning |

## Project Layout

```text
src/cache_header_audit/
  auditor.py      scoring and findings
  cli.py          command-line interface
  parser.py       Cache-Control parsing
  reporter.py     table and JSON rendering
  transport.py    HTTP header probing
tests/
  test_auditor.py
  test_parser.py
```

## Test

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
