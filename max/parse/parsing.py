import asyncio
import random
import json
from bs4 import BeautifulSoup
from core.config import settings
from app.cookie import load_cookies_mozilla
from app.header import build_headers
from app.extract import extract_id_from_url, extract_first_p_from_discussion
from app.generate import generate_response
from max.parse.keyboard import build_project_keyboard
from max.utils import safe_send_message
import httpx

async def parse_projects_and_send(bot, chat_id, state):
    cj = load_cookies_mozilla(settings.cookies)
    cookie_dict = {c.name: c.value for c in cj}
    results = []

    async with httpx.AsyncClient(cookies=cookie_dict) as client:
        for page in range(settings.pages_from, settings.pages_to + 1):
            data = await state.get_data()
            task = data.get("parser_task")
            if task and task.cancelled():
                break

            if settings.max_projects and len(results) >= settings.max_projects:
                break

            search_url = settings.base_search.format(page)

            resp = await client.get(search_url, headers=build_headers())

            if resp.status_code != httpx.codes.OK:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            project_cards = soup.find_all(
                "div", class_="task-feed-list"
            )
            for card in project_cards:
                if settings.max_projects and len(results) >= settings.max_projects:
                    break
                a = card.find("a", href=True)
                if not a:
                    continue
                project_link = "https://freelance.ru" + a["href"]
                project_id = extract_id_from_url(project_link)
                if not project_id:
                    continue

                # https://freelance.ru/task/reply/create
                # text
                # taskId
                # post

                disc_resp = await client.get(project_link, headers=build_headers(referer=search_url))

                if disc_resp.status_code != httpx.codes.OK:
                    continue

                task_text = extract_first_p_from_discussion(disc_resp.text)
                if not task_text:
                    continue
                soup_disc = BeautifulSoup(disc_resp.text, "html.parser")

                div_cost = soup_disc.find("div", _class="tv-meta-item__val tv-meta-item__val--budget")
                cost = div_cost.find("span", _class="bold").get_text()
                if not cost:
                    cost = "цена не указана"

                term = soup_disc.find(
                    "div", _class="tv-meta-item__val"
                ).get_text()

                ai_response = generate_response(task_text)

                await state.update_data(
                    **{
                        f"project_{project_id}": {
                            "client": client,
                            "discussion_url": project_link,
                            "ai_response": ai_response,
                            "cost": cost,
                            "term": term,
                            "task_text": task_text,
                        }
                    }
                )
                keyboard = build_project_keyboard(project_id)
                await safe_send_message(
                    bot,
                    chat_id,
                    f"Задание:\n{task_text}\n\nGPT: {ai_response}\n\nДанные из формы сайта:\nЦена: {cost}\nСрок: {term}",
                    reply_markup=keyboard,
                    parse_mode="Markdown",
                )
                results.append(
                    {
                        "link": project_link,
                        "task": task_text,
                        "response": ai_response,
                    }
                )
                await asyncio.sleep(random.uniform(1.0, 2.0))
        with open(settings.output_json_result, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
