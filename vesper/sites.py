from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

USER = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,37}[A-Za-z0-9])?$")
AGENT = "vesper/0.1 (+https://github.com/gabrielteramae/vesper)"


def normalize_username(value: str) -> str:
    username = value.strip()
    if not USER.fullmatch(username):
        raise ValueError("use só letras, números, ponto, _ ou hífen (máx. 39).")
    return username


@dataclass(frozen=True)
class Site:
    name: str
    profile: Callable[[str], str]
    probe: Callable[[str], str]
    read: Callable[[int, str], str]


def _json_status(found_status: int = 200):
    def read(status: int, body: str) -> str:
        if status == found_status:
            return "found"
        if status == 404:
            return "missing"
        return "unknown"

    return read


def _gitlab(status: int, body: str) -> str:
    if status != 200:
        return "unknown"
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return "unknown"
    if isinstance(data, list):
        return "found" if data else "missing"
    return "unknown"


def _path(username: str) -> str:
    return quote(username, safe="")


SITES: tuple[Site, ...] = (
    Site(
        "GitHub",
        lambda u: f"https://github.com/{_path(u)}",
        lambda u: f"https://api.github.com/users/{_path(u)}",
        _json_status(),
    ),
    Site(
        "GitLab",
        lambda u: f"https://gitlab.com/{_path(u)}",
        lambda u: f"https://gitlab.com/api/v4/users?username={_path(u)}",
        _gitlab,
    ),
    Site(
        "Codeberg",
        lambda u: f"https://codeberg.org/{_path(u)}",
        lambda u: f"https://codeberg.org/api/v1/users/{_path(u)}",
        _json_status(),
    ),
    Site(
        "Hugging Face",
        lambda u: f"https://huggingface.co/{_path(u)}",
        lambda u: f"https://huggingface.co/api/users/{_path(u)}/overview",
        _json_status(),
    ),
    Site(
        "npm",
        lambda u: f"https://www.npmjs.com/~{_path(u)}",
        lambda u: f"https://registry.npmjs.org/-/user/org.couchdb.user:{_path(u)}",
        _json_status(),
    ),
    Site(
        "dev.to",
        lambda u: f"https://dev.to/{_path(u)}",
        lambda u: f"https://dev.to/api/users/by_username?url={_path(u)}",
        _json_status(),
    ),
)


def fetch(url: str, timeout: float = 6) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": AGENT, "Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(200_000)
            return response.status, raw.decode("utf-8", "replace")
    except HTTPError as exc:
        raw = exc.read(20_000).decode("utf-8", "replace")
        return exc.code, raw
    except URLError as exc:
        raise TimeoutError(str(exc.reason)) from exc
