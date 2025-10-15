import requests
from bs4 import BeautifulSoup
from app.header import build_headers


def send_message(
    session: requests.Session,
    discussion_url: str,
    message: str,
    cost: str,
    term: str = "15",
) -> bool:
    resp = session.get(discussion_url)
    if not resp or resp.status_code != 200:
        print("    Не удалось открыть страницу для отправки сообщения")
        return False

    soup = BeautifulSoup(resp.text, "html.parser")
    csrf_input = soup.find("input", {"name": "_csrf"})
    csrf_token = csrf_input["value"] if csrf_input else ""

    data = {
        "StartDiscussionForm[message]": message,
        "StartDiscussionForm[cost]": str(cost),
        "StartDiscussionForm[term]": str(term),
        "_csrf": csrf_token,
        "StartDiscussionForm[signature]": "1",
        "StartDiscussionForm[works_preview]": "1",
    }

    headers = build_headers(discussion_url)

    post_resp = session.post(discussion_url, data=data, headers=headers)
    if post_resp.status_code == 200:
        print("    Сообщение отправлено успешно")
        return True
    else:
        print("    Ошибка при отправке сообщения:", post_resp.status_code)
        return False
