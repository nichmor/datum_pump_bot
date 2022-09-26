import os

from pyrogram.client import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


def get_app():
    return Client("datum_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)