import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from yt_dlp import YoutubeDL

# Render Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

CHANNELS = ["titokvideodowloader", "musicdowloader"] 

app = Client("tiktok_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    for channel in CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return await message.reply(
                f"⚠️ **အသုံးပြုရန်အတွက် အောက်ပါ Channel (၂) ခုလုံးကို Join ပေးပါ။**\n\n"
                f"1️⃣ @titokvideodowloader\n2️⃣ @musicdowloader\n\n"
                "Join ပြီးပါက /start ကို ပြန်နှိပ်ပေးပါ ခင်ဗျာ။"
            )
    await message.reply(
        "👋 **TikTok Music Downloader မှ ကြိုဆိုပါတယ်!**\n\n"
        "**အသုံးပြုနည်း:**\n"
        "သင် MP3 ပြောင်းချင်တဲ့ TikTok Link ကို ကျွန်တော့်ဆီ ပို့ပေးလိုက်ပါ။\n\n"
        "သီချင်းပြောင်းချင်တဲ့ TikTok Video Link ကို အခုပဲ ပို့လိုက်ပါ ခင်ဗျာ။ 👇"
    )

@app.on_message(filters.regex(r"http"))
async def download_tiktok(client, message):
    url = message.text
    sent_msg = await message.reply("သီချင်းကို ထုတ်ယူနေပါပြီ... ခေတ္တစောင့်ပေးပါ 🎵")
    
    # TikTok ဒေါင်းလုဒ်ဆွဲရာမှာ Error မတက်အောင် ဒါလေးတွေ ထည့်ရပါမယ်
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    try:
        # Event Loop ကို သုံးပြီး ဒေါင်းလုဒ်ဆွဲခြင်း (Bot ဟန်မသွားစေရန်)
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: YoutubeDL(ydl_opts).extract_info(url, download=True))
        file_path = YoutubeDL(ydl_opts).prepare_filename(info).replace(info['ext'], 'mp3')
        
        await message.reply_audio(file_path, caption=f"✅ **TikTok Music Success!**\n\n🎧 **Title:** {info.get('title', 'Unknown')}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        await sent_msg.delete()
        
    except Exception as e:
        # Error တက်ရင် ဘာကြောင့်တက်လဲဆိုတာ သိရအောင် Log ထဲမှာ ပြခိုင်းပါမယ်
        print(f"Error Details: {str(e)}")
        await sent_msg.edit(f"❌ **အမှားအယွင်းရှိသွားပါသည်။**\n\nLink က မှန်ပေမယ့် Video က Private ဖြစ်နေတာ ဒါမှမဟုတ် ဒေါင်းလုဒ်ဆွဲခွင့် ပိတ်ထားတာ ဖြစ်နိုင်ပါတယ် ခင်ဗျာ။")

app.run()
