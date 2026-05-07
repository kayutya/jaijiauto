import discord
from discord.ext import commands
import asyncio
import time
import os

# --- 基本設定 ---
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ID = 1172772592534568971
is_active = False
last_stamp_time = 0
COOLDOWN_SECONDS = 5 # 一度スタンプを押したら5秒間は次を押さない

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_content="!", intents=intents)

@bot.event
async def on_message(message):
    global is_active, last_stamp_time

    if message.author == bot.user:
        return

    # オンオフ切り替え
    if message.content == "!on":
        is_active = True
        await message.channel.send("ガイジが騒ぎ出しました。スタンプを押します。")
        return
    
    if message.content in ["!off", "!fuck off", "!寝ろ"]:
        is_active = False
        await message.channel.send("ガイジは休憩に入りました。")
        return

    # スタンプ爆撃
    if is_active and message.author.id == TARGET_USER_ID:
        current_time = time.time()
        
        # 5秒以内の連投なら無視
        if current_time - last_stamp_time < COOLDOWN_SECONDS:
            return

        # 順番：車いす ➔ 生姜 ➔ 医者
        emojis = ["🧑‍🦽", "🫚", "🧑‍⚕️"] 
        
        # スタンプ時間を更新
        last_stamp_time = current_time

        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
                await asyncio.sleep(0.5) # 制限回避
            except:
                pass

bot.run(TOKEN)
