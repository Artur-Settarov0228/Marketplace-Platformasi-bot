import os

from dotenv import load_dotenv

load_dotenv()


# class Settings:
#     BOT_TOKEN: str = os.getenv("BOT_TOKEN")
#     BASE_URL: str = os.getenv("API_BASE_URL")

# settings = Settings()


class Data:
    TOKEN = os.getenv("BOT_TOKEN")
    BASE_URL = os.getenv("API_BASE_URL")


settings = Data()

from enum import IntEnum


class RegisterStep(IntEnum):
    FULL_NAME = 0
    PHONE_NUMBER = 1
    AVATAR = 2
    CONFIRM = 3