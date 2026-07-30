from bs4 import BeautifulSoup


def extract_id_from_url(url: str) -> str:
    result = url.split("https://freelance.ru/task/view/")
    return result[1]


def extract_first_p_from_discussion(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    div_info = soup.find("div", class_="tcard tv-hero")
    if not div_info:
        return ""
    return div_info.get_text()
