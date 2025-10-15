import asyncio
import random
import json
from bs4 import BeautifulSoup
from core.config import settings
from app.cookie import load_cookies_mozilla
from app.header import build_headers
from app.extract import extract_id_from_url, extract_first_p_from_discussion
from app.generate import generate_response
from bot.keyboards import build_project_keyboard
import aiohttp
from bot.utils import safe_send_message


async def fetch(session, method, url, **kwargs):
    async with session.request(method, url, **kwargs) as resp:
        text = await resp.text()
        return type(
            "Resp",
            (),
            {"text": text, "status_code": resp.status, "ok": resp.status == 200},
        )


async def parse_projects_and_send(bot, chat_id, state):
    cj = load_cookies_mozilla(settings.cookies)
    cookie_dict = {c.name: c.value for c in cj}
    results = []
    async with aiohttp.ClientSession(cookies=cookie_dict) as session:
        try:
            for page in range(settings.pages_from, settings.pages_to + 1):
                data = await state.get_data()
                task = data.get("parser_task")
                if task and task.cancelled():
                    break
                if settings.max_projects and len(results) >= settings.max_projects:
                    break
                search_url = settings.base_search.format(page)
                resp = await fetch(session, "GET", search_url, headers=build_headers())
                if not resp or not resp.ok:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                project_cards = soup.find_all(
                    "div", class_="project-item-default-card project"
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
                    discussion_url = settings.discussion_template.format(project_id)
                    disc_resp = await fetch(
                        session,
                        "GET",
                        discussion_url,
                        headers=build_headers(referer=search_url),
                    )
                    if not disc_resp or not disc_resp.ok or not disc_resp.text:
                        continue
                    task_text = extract_first_p_from_discussion(disc_resp.text)
                    if not task_text:
                        continue
                    soup_disc = BeautifulSoup(disc_resp.text, "html.parser")
                    cost_input = soup_disc.find(
                        "input", {"name": "StartDiscussionForm[cost]"}
                    )
                    term_input = soup_disc.find(
                        "input", {"name": "StartDiscussionForm[term]"}
                    )
                    cost_value = (
                        cost_input["value"]
                        if (
                            cost_input
                            and cost_input.has_attr("value")
                            and cost_input["value"].strip()
                        )
                        else "цена не указана"
                    )
                    term_value = (
                        term_input["value"]
                        if (
                            term_input
                            and term_input.has_attr("value")
                            and term_input["value"].strip()
                        )
                        else "срок не указан"
                    )
                    ai_response = generate_response(task_text)
                    dispatch_id = f"{project_id}_{random.randint(1,1000000)}"
                    await state.update_data(
                        **{
                            f"project_{dispatch_id}": {
                                "session": session,
                                "discussion_url": discussion_url,
                                "ai_response": ai_response,
                                "cost": cost_value,
                                "term": term_value,
                                "task_text": task_text,
                            }
                        }
                    )
                    keyboard = build_project_keyboard(dispatch_id)
                    await safe_send_message(
                        bot,
                        chat_id,
                        f"Задание:\n{task_text}\n\nGPT: {ai_response}\n\nДанные из формы сайта:\nЦена: {cost_value}\nСрок: {term_value}",
                        reply_markup=keyboard,
                        parse_mode="Markdown",
                    )
                    results.append(
                        {
                            "link": discussion_url,
                            "task": task_text,
                            "response": ai_response,
                        }
                    )
                    await asyncio.sleep(random.uniform(1.0, 2.0))
            with open(settings.output_json_result, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        finally:
            await session.close()
