MAX_LEN = 4096


async def safe_send_message(bot, chat_id, text, **kwargs):
    for i in range(0, len(text), MAX_LEN):
        await bot.send_message(chat_id, text[i : i + MAX_LEN], **kwargs)


async def safe_answer(message, text, **kwargs):
    for i in range(0, len(text), MAX_LEN):
        await message.answer(text[i : i + MAX_LEN], **kwargs)
