from http.cookiejar import MozillaCookieJar


def load_cookies_mozilla(path: str) -> MozillaCookieJar:
    cj = MozillaCookieJar(path)
    cj.load(ignore_discard=True, ignore_expires=True)
    return cj
