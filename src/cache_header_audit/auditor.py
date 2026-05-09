from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .parser import normalize_headers, parse_cache_control, parse_int


@dataclass(frozen=True)
class Finding:
    severity: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    url: str
    status: int
    score: int
    grade: str
    cache_control: dict[str, str | bool] = field(default_factory=dict)
    findings: tuple[Finding, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "url": self.url,
            "status": self.status,
            "score": self.score,
            "grade": self.grade,
            "cache_control": self.cache_control,
            "findings": [
                {"severity": finding.severity, "message": finding.message}
                for finding in self.findings
            ],
        }


def audit_headers(url: str, status: int, headers: Mapping[str, str]) -> AuditResult:
    normalized = normalize_headers(dict(headers))
    cache_control = parse_cache_control(normalized.get("cache-control"))
    findings: list[Finding] = []
    score = 0

    if status >= 500:
        findings.append(Finding("error", "server returned a 5xx response"))
    elif status >= 400:
        findings.append(Finding("warn", "resource returned a client error status"))
    else:
        score += 10

    if cache_control:
        score += 20
    else:
        findings.append(Finding("warn", "missing Cache-Control header"))

    max_age = parse_int(cache_control.get("max-age"))
    shared_max_age = parse_int(cache_control.get("s-maxage"))
    effective_age = shared_max_age if shared_max_age is not None else max_age

    if effective_age is None:
        findings.append(Finding("warn", "no max-age or s-maxage directive found"))
    elif effective_age <= 0:
        findings.append(Finding("warn", "cache lifetime is zero seconds"))
    elif effective_age < 60:
        score += 8
        findings.append(Finding("info", "cache lifetime is very short"))
    elif effective_age <= 604800:
        score += 25
    else:
        score += 18
        findings.append(Finding("info", "cache lifetime is longer than one week"))

    if "public" in cache_control:
        score += 8
    if "immutable" in cache_control:
        score += 8
    if "stale-while-revalidate" in cache_control:
        score += 10
    if "must-revalidate" in cache_control:
        score += 4

    if "no-store" in cache_control:
        score -= 30
        findings.append(Finding("error", "no-store prevents cache reuse"))
    if "no-cache" in cache_control:
        score -= 12
        findings.append(Finding("warn", "no-cache requires revalidation on every reuse"))
    if "private" in cache_control:
        score -= 8
        findings.append(Finding("info", "private blocks shared cache storage"))

    validators = [name for name in ("etag", "last-modified") if name in normalized]
    if validators:
        score += 15
    else:
        findings.append(Finding("warn", "missing ETag or Last-Modified validator"))

    if "expires" in normalized and effective_age is None:
        score += 8

    vary = normalized.get("vary", "")
    if vary == "*":
        score -= 18
        findings.append(Finding("error", "Vary: * makes the response effectively uncacheable"))
    elif vary:
        score += 5

    if "content-digest" in normalized or "digest" in normalized:
        score += 4

    final_score = max(0, min(100, score))
    return AuditResult(
        url=url,
        status=status,
        score=final_score,
        grade=_grade(final_score),
        cache_control=cache_control,
        findings=tuple(findings),
    )


def _grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 45:
        return "D"
    return "F"
