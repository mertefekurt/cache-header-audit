![Cache Header Audit cover](assets/readme-cover.svg)

# Cache Header Audit

Audit HTTP cache headers from the command line.

## Working shape

The repo is meant to be opened, understood, and run quickly. The command surface is deliberately narrow: `cache-header-audit`.

## Fresh clone

```bash
git clone https://github.com/mertefekurt/cache-header-audit.git
cd cache-header-audit
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## First command

```bash
cache-header-audit --help
```

## Local confidence

```bash
ruff check .
pytest
python -m cache_header_audit --help
```
