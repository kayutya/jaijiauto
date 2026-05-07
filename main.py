import discord
from discord.ext import commands
import asyncio
import os

# --- 基本設定 ---
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ID = 1172772592534568971
is_active = False
# 連投検知用のカウンター
pending_tasks = {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    global is_active

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

    # スタンプ爆撃（連投の最後にだけ反応）
    if is_active and message.author.id == TARGET_USER_ID:
        
        # すでに「待ち」状態のタスクがあればキャンセル（最新の発言を優先するため）
        if TARGET_USER_ID in pending_tasks:
            pending_tasks[TARGET_USER_ID].cancel()

        # 新しい「待ち」タスクを作成
        task = asyncio.create_task(wait_and_react(message))
        pending_tasks[TARGET_USER_ID] = task

async def wait_and_react(message):
    # 1.5秒間、次の発言が来るのを待つ（ここを調整して「待ち時間」を変えられます）
    await asyncio.sleep(2.5)
    
    # 順番：車いす ➔ 生姜 ➔ 医者
    emojis = ["🧑‍🦽", "🫚", "🧑‍⚕️"] 
    
    for emoji in emojis:
        try:
            await message.add_reaction(emoji)
            await asyncio.sleep(0.4) 
        except:
            pass
    
    # 終わったらタスクリストから消す
    if TARGET_USER_ID in pending_tasks:
        del pending_tasks[TARGET_USER_ID]

bot.run(TOKEN)
