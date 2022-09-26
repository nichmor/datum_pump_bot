import asyncio
import pytest
from pyrogram import Client
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message
from unittest.mock import AsyncMock, MagicMock, patch

from bot.app import echo, download_youtube
from tests.conftest import app as test_app



pytestmark = pytest.mark.asyncio


async def test_echo():
    client_mock, message_mock = (MagicMock(), AsyncMock())
    await echo(client_mock, message_mock)
    message_mock.reply_text.assert_awaited_with('echo')


async def test_download_youtube_without_url():
    client_mock, message_mock = MagicMock(), AsyncMock()
    message_mock.command = ["download_command"]
    await download_youtube(client_mock, message_mock)
    message_mock.reply.assert_awaited_with('Please provide youtube link, example: /download_command wwww.my.link')

@patch('bot.app.download_video')
async def test_download_youtube_download_video_failed(download_mock):
    client_mock, message_mock = MagicMock(), AsyncMock()
    message_mock.command = ["download_command", "url"]
    download_mock.return_value = None
    await download_youtube(client_mock, message_mock)
    message_mock.reply.assert_awaited_with('Something very bad happened with the video, check if it is not private, or retry later')

@patch('bot.app.download_video')
@patch('bot.app.progress_callback_builder')
async def test_download_youtube_download_only_video(callback_builder_mock, download_mock):
    client_mock, message_mock = MagicMock(), AsyncMock()
    message_mock.command = ["video", "url"]
    download_mock.return_value = 'filename'
    await download_youtube(client_mock, message_mock)
    message_mock.reply_video.assert_awaited_with('filename', progress=callback_builder_mock())


@patch('bot.app.download_video')
@patch('bot.app.convert_to_audio')
async def test_download_youtube_download_audio_failed(convert_to_audio_mock, download_mock):
    client_mock, message_mock = MagicMock(), AsyncMock()
    message_mock.command = ["audio", "url"]
    download_mock.return_value = 'filename'
    convert_to_audio_mock.return_value = None
    await download_youtube(client_mock, message_mock)
    message_mock.reply.assert_awaited_with('Something very bad happened with the audio, retry agains')

@patch('bot.app.download_video')
@patch('bot.app.convert_to_audio')
@patch('bot.app.progress_callback_builder')
async def test_download_youtube_download_only_audio(callback_builder_mock, convert_to_audio_mock, download_mock):
    client_mock, message_mock = MagicMock(), AsyncMock()
    message_mock.command = ["audio", "url"]
    download_mock.return_value = 'filename'
    convert_to_audio_mock.return_value = 'audio_name'
    await download_youtube(client_mock, message_mock)
    convert_to_audio_mock.assert_called_with('filename')
    message_mock.reply_audio.assert_awaited_with('audio_name', progress=callback_builder_mock())