import re

from bs4 import BeautifulSoup


def extract_id_from_url(url: str) -> str:
    m = re.search(r"(\d+)\.html\s*$", url)
    return m.group(1) if m else ""


def extract_first_p_from_discussion(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    div_info = soup.find("div", class_="project-info")
    if not div_info:
        return ""
    p_tags = div_info.find_all("p")
    if not p_tags:
        return ""
    return p_tags[0].get_text(separator="\n").strip()
