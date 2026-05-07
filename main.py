import discord
from discord.ext import commands
import asyncio
import os  # ← これを足しました！これでエラーが消えます

# --- 基本設定 ---
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ID = 1172772592534568971
is_active = False
# 連投検知用のカウンター
pending_tasks = {}
# 通知を送るチャンネルを保存する変数
notification_channel = None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # 起動時はまだどこでオンになるか分からないので、ログに出すだけ
    print("ボット起動：!on が打たれたチャンネルで診察を開始します。")

@bot.event
async def on_message(message):
    global is_active, notification_channel

    if message.author == bot.user:
        return

    # オンオフ切り替え
    if message.content == "!on":
        is_active = True
        # ★コマンドが打たれたチャンネルを記憶する
        notification_channel = message.channel
        await notification_channel.send("ガイジが騒ぎ出しました。スタンプを押します。")
        return
    
    if message.content in ["!off", "!fuck off", "!寝ろ"]:
        is_active = False
        if notification_channel:
            await notification_channel.send("ガイジは休憩に入りました。")
        return

    # スタンプ爆撃（連投の最後にだけ反応）
    if is_active and message.author.id == TARGET_USER_ID:
        if TARGET_USER_ID in pending_tasks:
            pending_tasks[TARGET_USER_ID].cancel()

        task = asyncio.create_task(wait_and_react(message))
        pending_tasks[TARGET_USER_ID] = task

async def wait_and_react(message):
    try:
        await asyncio.sleep(1.5) # 1.5秒溜める
        
        # 順番：車いす ➔ 生姜 ➔ 医者
        emojis = ["🧑‍🦽", "🫚", "🧑‍⚕️"] 
        
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
                await asyncio.sleep(0.4) 
            except:
                pass
                
    except asyncio.CancelledError:
        pass
    finally:
        if TARGET_USER_ID in pending_tasks:
            if pending_tasks[TARGET_USER_ID] == asyncio.current_task():
                del pending_tasks[TARGET_USER_ID]

bot.run(TOKEN)
