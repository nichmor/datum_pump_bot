import os
from dotenv import load_dotenv

def test_config_is_initialized():
    from bot.config import API_ID, API_HASH, BOT_TOKEN

    assert API_ID == 123
    assert (API_HASH, BOT_TOKEN) == ('hash1', 'hash2')