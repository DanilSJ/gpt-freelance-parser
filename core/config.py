from pydantic_settings import BaseSettings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    Telegram: bool = False
    Max: bool = True

    telegram_token: str = os.environ["TELEGRAM_TOKEN"]
    max_token: str = os.environ["MAX_TOKEN"]
    allowed_user_id: int = int(os.environ["TELEGRAM_USER_ID"])
    system_message: str = os.environ["RULES_FOR_AI"]
    pages_from: int = 1
    pages_to: int = 1
    request_timeout: int = 15
    max_retries: int = 2
    max_projects: int = 10
    base_search: str = (
        "https://freelance.ru/project/search?q=&a=1&v=1&c%5B0%5D=4&page={}"
    )
    discussion_template: str = "https://freelance.ru/project/discussion/start/{}"

    cookies: str = "core/cookies/freelance.ru_cookies.txt"
    output_json_result: str = "output/freelance_projects_with_responses.json"


settings = Settings()

bot = Bot(
    token=settings.telegram_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
