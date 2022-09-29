from typing import Optional
from pyrogram.types import Message

import moviepy.editor as mp
from yt_dlp import YoutubeDL


def progress_callback_builder(message_to_edit: Message):
    async def _callback(current, total) -> None:
        remains_procentage = int((current * 100) / total)
        await message_to_edit.edit_text(f'remains: {remains_procentage}%')
    
    return _callback


def download_video(url: str, tmp_dir:str) -> Optional[str]:
    try:
        with YoutubeDL(params={'outtmpl': f'{tmp_dir}/%(title)s.%(ext)s'}) as dl:
            info = dl.extract_info(url, download=True)
            return dl.prepare_filename(info)
    except Exception as e:
        print('something bad happned while converting video', e)
        return None


def convert_to_audio(filename: str) -> Optional[str]:
    try:
        clip = mp.VideoFileClip(filename)
        audio_name = f'{filename}.mp3'
        clip.audio.write_audiofile(audio_name)
        return audio_name
    except Exception as e:
        print('something bad happned while converting as audio', e)
        return None
    