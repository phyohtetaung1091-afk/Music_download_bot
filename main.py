import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# Bot အချက်အလက်များ
API_ID = 26569261 # သင့် API ID ထည့်ပါ (နမူနာထည့်ထားသည်)
API_HASH = "8738396656774e14f08e5e3476685c69" # သင့် API HASH ထည့်ပါ
BOT_TOKEN = "8357499732:AAFYRlqZbINCxGtgcaBCvS-d6jSb_5QRkf0"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! Send me any video link to convert it to MP3. 🎧")

@app.on_message(filters.regex(r"http"))
async def download_music(client, message):
    url = message.text
    sent_msg = await message.reply("Downloading... Please wait. ⏳")
    
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
            file_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            title = info.get('title', 'Music')

        await sent_msg.edit("Uploading to Telegram... 📤")
        await message.reply_audio(audio=file_path, caption=f"✅ **{title}**\n\nDownloaded by @YourBot")
        
        if os.path.exists(file_path):
            os.remove(file_path) # Storage မပြည့်အောင် ပြန်ဖျက်ခြင်း
        await sent_msg.delete()

    except Exception as e:
        await sent_msg.edit(f"❌ Error: Link မမှန်တာ (သို့) Server အခက်အခဲ ဖြစ်နေပါတယ်။")
        print(f"Log: {e}")

app.run()
