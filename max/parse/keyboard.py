from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types import CallbackButton

def build_project_keyboard(dispatch_id):
    return InlineKeyboardBuilder().row(
        CallbackButton(
            text="Принять",
            payload=f"accept_{dispatch_id}"
        ),
        CallbackButton(
            text="Отклонить",
            payload=f"reject_{dispatch_id}",
        ),    CallbackButton(
            text="Сгенерировать заново",
            payload=f"regen_{dispatch_id}",
        ),    CallbackButton(
            text="Комментарий ИИ",
            payload=f"comment_{dispatch_id}",
        ),
    )
