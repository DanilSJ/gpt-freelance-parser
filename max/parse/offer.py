from maxapi.types import MessageCreated, MessageCallback
from maxapi.context import MemoryContext
from max.parse.states import OfferStates
import app.send as send_mod
from app.generate import generate_response
from max.parse.keyboard import build_project_keyboard
from max.utils import safe_send_message, safe_answer


def get_project_key(dispatch_id):
    return f"project_{dispatch_id}"


async def start_offer_flow(callback: MessageCallback, state: MemoryContext):
    dispatch_id = callback.message.body.text.split("_", 1)[1]

    data = await state.get_data()
    project = data.get(get_project_key(dispatch_id))
    if not project:
        await callback.answer("Задание не найдено или устарело!")
        return
    await state.update_data(offer_dispatch_id=dispatch_id)
    await state.set_state(OfferStates.waiting_for_price)
    await callback.message.answer("Введите цену:")
    await callback.answer()


async def handle_offer_price(event: MessageCreated, state: MemoryContext):
    price = event.message.body.text.strip()
    await state.update_data(offer_price=price)
    await state.set_state(OfferStates.waiting_for_term)
    await event.message.answer("Введите срок:")


async def handle_offer_term(event: MessageCreated, state: MemoryContext):
    term = event.message.body.text.strip()
    data = await state.get_data()
    dispatch_id = data.get("offer_dispatch_id")
    project = data.get(get_project_key(dispatch_id))
    offer_txt = data.get("offer_result") or project["ai_response"]
    status = send_mod.send_message(
        project["session"],
        project["discussion_url"],
        offer_txt,
        data.get("offer_price"),
        term,
    )
    if status:
        await safe_answer(event.message, "Отклик успешно отправлен!")
    else:
        await safe_answer(event.message, "Ошибка при отправке отклика.")
    # Сброс состояния
    await state.clear()


async def regenerate_ai_response(callback: MessageCallback, state: MemoryContext):
    dispatch_id = callback.message.body.text.split("_", 1)[1]
    data = await state.get_data()
    project = data.get(get_project_key(dispatch_id))
    if not project:
        # edit_text тут не требуется
        return
    new_ai_response = generate_response(project["task_text"])
    project["ai_response"] = new_ai_response
    await state.update_data(**{get_project_key(dispatch_id): project})
    kb = build_project_keyboard(dispatch_id)
    big_text = f"Задание:\n{project['task_text']}\n\nGPT: {new_ai_response}\n\nДанные из формы сайта:\nЦена: {project['cost']}\nСрок: {project['term']}"
    if len(big_text) > 4096:
        await safe_send_message(
            callback.message.bot,
            callback.message.chat.id,
            big_text,
            reply_markup=kb,
            parse_mode="Markdown",
        )
    else:
        await callback.message.edit_text(
            big_text, parse_mode="Markdown", reply_markup=kb
        )
    await callback.answer("Ответ сгенерирован заново.")


async def request_offer_comment(callback: MessageCallback, state: MemoryContext):
    dispatch_id = callback.message.body.text.split("_", 1)[1]
    await state.update_data(offer_dispatch_id=dispatch_id)
    await state.set_state(OfferStates.waiting_for_comment)
    await callback.message.answer(
        "Введите условия для отклика (например, с каким приветствием начать или особенности формулировки):"
    )
    await callback.answer()


async def handle_offer_comment(event: MessageCreated, state: MemoryContext):
    comment = event.message.body.text.strip()
    data = await state.get_data()
    dispatch_id = data.get("offer_dispatch_id")
    project = data.get(get_project_key(dispatch_id))
    # Используем комментарий как промпт для генерации
    prompt = f"{comment}\n\n{project['task_text']}"
    ai_text = generate_response(prompt)
    await state.update_data(offer_result=ai_text)
    await state.set_state(OfferStates.waiting_for_price)
    await safe_answer(
        event.message,
        f"Вот отклик ИИ с учётом ваших условий:\n\n{ai_text}\n\nТеперь введите цену:",
    )
