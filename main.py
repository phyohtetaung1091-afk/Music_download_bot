import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from yt_dlp import YoutubeDL

# Render Environment Variables မှ ဖတ်ယူခြင်း
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Channel Username များ (Link မှ @ နောက်ကစာသားကို ယူထားပါသည်)
CHANNELS = ["titokvideodowloader", "musicdowloader"] 

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    
    # Channel နှစ်ခုလုံး Join မ Join စစ်ဆေးခြင်း
    for channel in CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return await message.reply(
                f"⚠️ **အသုံးပြုရန်အတွက် အောက်ပါ Channel (၂) ခုလုံးကို Join ပေးရပါမယ် ခင်ဗျာ။**\n\n"
                f"1️⃣ @titokvideodowloader\n"
                f"2️⃣ @musicdowloader\n\n"
                "Join ပြီးပါက /start ကို ပြန်နှိပ်ပေးပါ ခင်ဗျာ။"
            )
    
    # Join ပြီးသားသူများအတွက် ပြမည့်စာသား
    await message.reply(
        f"ဟယ်လို {message.from_user.mention} ရေ... 👋\n\n"
        "🎶 **TikTok Music Downloader မှ ကြိုဆိုပါတယ်!**\n\n"
        "**အသုံးပြုနည်း -**\n"
        "သင် MP3 ပြောင်းချင်တဲ့ **TikTok Video Link** ကို ကျွန်တော့်ဆီ ပို့ပေးလိုက်ရုံပါပဲ။ ခဏအတွင်းမှာ သီချင်းအဖြစ် ပြောင်းလဲပေးသွားမှာပါ ခင်ဗျာ။\n\n"
        "ကဲ... အခုပဲ Link ပို့ပြီး စမ်းကြည့်လိုက်ရအောင်! 👇"
    )

@app.on_message(filters.regex(r"http"))
async def download_tiktok_music(client, message):
    url = message.text
    sent_msg = await message.reply("TikTok ကနေ သီချင်းကို ထုတ်ယူနေပါပြီ... ခေတ္တစောင့်ပေးပါ 🎵")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).replace(info['ext'], 'mp3')
            
        await message.reply_audio(
            file_path, 
            caption=f"✅ **TikTok Video မှ သီချင်းပြောင်းလဲခြင်း အောင်မြင်ပါတယ်!**\n\n🎧 **Title:** {info.get('title', 'Unknown')}\n\nပံ့ပိုးမှုအတွက် ကျေးဇူးတင်ပါတယ် ခင်ဗျာ။"
        )
        if os.path.exists(file_path):
            os.remove(file_path)
        await sent_msg.delete()
    except Exception as e:
        await sent_msg.edit(f"❌ **အမှားအယွင်းတစ်ခု ရှိသွားပါတယ်!**\n\nLink မှန်မမှန် သို့မဟုတ် Video က ပိတ်ထားတာလားဆိုတာ ပြန်စစ်ပေးပါဦး။")

app.run()
