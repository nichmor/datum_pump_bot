import asyncio
import tempfile
from typing import Any

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import get_app
from bot.bot import progress_callback_builder, download_video, convert_to_audio

app = get_app()



@app.on_message(filters.command(['audio', 'video']))
async def download_youtube(client, message: Message):
    command_args = message.command
    if len(command_args) == 1:
        await message.reply(f'Please provide youtube link, example: /{command_args[0]} wwww.my.link')
        return
    
    await message.reply('Downloading started')
    progress_message = await message.reply_text('remains: calculating')
    with tempfile.TemporaryDirectory() as tmp_dirname:
        filename = download_video(command_args[1], tmp_dir=tmp_dirname)
        if not filename:
            await message.reply('Something very bad happened with the video, check if it is not private, or retry later')
            return

        if command_args[0] == 'video':
            await message.reply_video(filename, progress=progress_callback_builder(progress_message))
        else:
            audio_name = convert_to_audio(filename)
            if not audio_name:
                await message.reply('Something very bad happened with the audio, retry agains')
                return
            
            await message.reply_audio(audio_name, progress=progress_callback_builder(progress_message))

    await progress_message.delete()

@app.on_message(filters.command(['echo']))
async def echo(client, message: Message):
    await message.reply_text('echo')