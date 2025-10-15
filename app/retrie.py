import random
import time

from core.config import settings


def get_with_retries(
    session,
    url,
    headers,
    timeout=settings.request_timeout,
    max_retries=settings.max_retries,
):
    for _ in range(max_retries):
        try:
            r = session.get(url, headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r
        except Exception:
            pass
        time.sleep(0.5 + random.random())
    return None
