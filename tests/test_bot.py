from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from bot.bot import progress_callback_builder, download_video, convert_to_audio

pytestmark = pytest.mark.asyncio

TELEGRAM_DEFAULT_GROUP = 0

async def test_progress_callback_builder():
    message_mock: AsyncMock = AsyncMock()
    callback = progress_callback_builder(message_mock)
    await callback(0, 100)
    message_expected = 'remains: 0%'
    message_mock.edit_text.assert_awaited_with(message_expected)

@patch('bot.bot.YoutubeDL')
async def test_download_video(youtube_mock: MagicMock):
    youtube_mock.return_value.__enter__.return_value.prepare_filename.return_value = 'temp_dir/test_filename'
    filename = download_video('test_url', 'temp_dir')
    assert filename == 'temp_dir/test_filename'

@patch('bot.bot.YoutubeDL')
async def test_download_video_fail(youtube_mock: MagicMock):
    youtube_mock.return_value.__enter__.return_value = Exception
    filename = download_video('test_url', 'temp_dir')
    assert not filename

@patch('bot.bot.mp.VideoFileClip')
async def test_convert_to_audio(clip_mocked: MagicMock):
    audio_name = convert_to_audio('filename')
    clip_mocked().audio.write_audiofile.assert_called_with('filename.mp3')
    assert audio_name == 'filename.mp3'

@patch('bot.bot.mp.VideoFileClip')
async def test_convert_to_audio_fail(clip_mocked: MagicMock):
    clip_mocked.return_value = Exception
    audio_name = convert_to_audio('filename')
    assert not audio_name