import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# Render Environment Variables မှ အချက်အလက်များကို ဖတ်ယူခြင်း
# API_ID ကို ဂဏန်း (Integer) အဖြစ် သေချာပြောင်းလဲထားသည်
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! Send me any video link to download as MP3.")

@app.on_message(filters.regex(r"http"))
async def download_music(client, message):
    url = message.text
    sent_msg = await message.reply("Downloading... Please wait.")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace(info['ext'], 'mp3')
            
        await message.reply_audio(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        await sent_msg.delete()
    except Exception as e:
        await sent_msg.edit(f"Error: {str(e)}")

app.run()
