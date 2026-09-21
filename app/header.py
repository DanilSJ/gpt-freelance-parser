from fake_useragent import UserAgent

ua = UserAgent()

def build_headers(referer: str = None) -> dict:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "User-Agent": ua.random,
        "Referer": referer if referer else "https://freelance.ru/",
    }
    return headers
