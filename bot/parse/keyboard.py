from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_project_keyboard(dispatch_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Принять", callback_data=f"accept_{dispatch_id}"),
                InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{dispatch_id}"),
                InlineKeyboardButton(text="Сгенерировать заново", callback_data=f"regen_{dispatch_id}"),
                InlineKeyboardButton(text="Комментарий ИИ", callback_data=f"comment_{dispatch_id}"),
            ]
        ]
    )
