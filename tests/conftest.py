import pytest
from dotenv import load_dotenv
from pyrogram import Client


def pytest_configure(config):
    # prepare something ahead of all tests
    load_dotenv('.test.env', override=True)
    
# @pytest.fixture
def app():
    client = Client("my_account_test", api_id=12249163, api_hash="test",  test_mode=True)
    return client