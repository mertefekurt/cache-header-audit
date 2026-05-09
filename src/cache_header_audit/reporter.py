from __future__ import annotations

import json
from typing import Iterable

from .auditor import AuditResult


def render_json(results: Iterable[AuditResult]) -> str:
    return json.dumps([result.as_dict() for result in results], indent=2, sort_keys=True)


def render_table(results: Iterable[AuditResult], *, color: bool = True) -> str:
    rows = list(results)
    if not rows:
        return "no urls audited"

    widths = {
        "url": max(3, min(54, max(len(result.url) for result in rows))),
        "score": 5,
        "grade": 5,
        "issue": max(5, min(52, max(len(_primary_issue(result)) for result in rows))),
    }
    header = (
        f"{'url':<{widths['url']}}  "
        f"{'score':>{widths['score']}}  "
        f"{'grade':^{widths['grade']}}  "
        f"{'primary issue':<{widths['issue']}}"
    )
    divider = "-" * len(header)
    lines = [header, divider]

    for result in rows:
        grade = _paint(result.grade, result.score, color)
        lines.append(
            f"{_trim(result.url, widths['url']):<{widths['url']}}  "
            f"{result.score:>{widths['score']}}  "
            f"{grade:^{widths['grade'] + (_ansi_padding(grade) if color else 0)}}  "
            f"{_trim(_primary_issue(result), widths['issue']):<{widths['issue']}}"
        )

    return "\n".join(lines)


def _primary_issue(result: AuditResult) -> str:
    if not result.findings:
        return "cache policy looks healthy"
    return result.findings[0].message


def _trim(value: str, width: int) -> str:
    if len(value) <= width:
        return value
    return value[: max(0, width - 3)] + "..."


def _paint(grade: str, score: int, enabled: bool) -> str:
    if not enabled:
        return grade
    if score >= 75:
        code = "32"
    elif score >= 45:
        code = "33"
    else:
        code = "31"
    return f"\033[{code}m{grade}\033[0m"


def _ansi_padding(value: str) -> int:
    return value.count("\033[") * 4 + value.count("m")
