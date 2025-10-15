from core.ai_model_list import model_list
from core.config import settings
from g4f.client import Client

client = Client()


def generate_response(task_text: str) -> str:
    """Отправляем описание задания в GPT и получаем готовый отклик"""
    for model in model_list:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": settings.system_message},
                    {"role": "user", "content": task_text},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Ошибка GPT:", e)
            return "Здравствуйте. Готов выполнить ваш проект."
