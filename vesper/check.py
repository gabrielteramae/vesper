from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from vesper.sites import SITES, fetch, normalize_username


def check_username(username: str, timeout: float = 6) -> dict:
    handle = normalize_username(username)
    results = []

    def one(site):
        started = time.perf_counter()
        url = site.profile(handle)
        try:
            status, body = fetch(site.probe(handle), timeout)
            state = site.read(status, body)
        except Exception:
            state = "unknown"
        return {
            "site": site.name,
            "url": url,
            "state": state,
            "ms": int((time.perf_counter() - started) * 1000),
        }

    with ThreadPoolExecutor(max_workers=len(SITES)) as pool:
        futures = [pool.submit(one, site) for site in SITES]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item["site"])
    return {"username": handle, "results": results}
