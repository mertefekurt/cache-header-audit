# Cache Header Audit

![Cache Header Audit cover](assets/readme-cover.svg)

![stack](https://img.shields.io/badge/stack-Python-b45309?style=flat-square) ![python](https://img.shields.io/badge/python-3.10-be185d?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-4b5563?style=flat-square) ![tests](https://img.shields.io/badge/tests-pytest-2563eb?style=flat-square)

> Audit HTTP cache headers from the command line

## How I use it

The project stays focused on one job: take a small input, produce a clear result, and avoid adding a heavy service around a problem that fits in a command line.

## Quick start

```bash
python -m pip install -e ".[dev]"
cache-header-audit --help
python -m cache_header_audit --help
```

## What is inside

```text
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m cache_header_audit --help
```
