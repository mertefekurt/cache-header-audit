from __future__ import annotations

from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class HeaderResponse:
    url: str
    status: int
    headers: dict[str, str]


def fetch_headers(
    url: str,
    *,
    method: str = "HEAD",
    timeout: float = 8.0,
    user_agent: str = "cache-header-audit/0.1",
) -> HeaderResponse:
    request = Request(url, method=method.upper(), headers={"User-Agent": user_agent})

    try:
        with urlopen(request, timeout=timeout) as response:
            return HeaderResponse(
                url=response.geturl(),
                status=response.status,
                headers=dict(response.headers.items()),
            )
    except HTTPError as error:
        if error.code == 405 and method.upper() == "HEAD":
            return fetch_headers(
                url,
                method="GET",
                timeout=timeout,
                user_agent=user_agent,
            )

        return HeaderResponse(
            url=url,
            status=error.code,
            headers=dict(error.headers.items()),
        )
