import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 設定
TARGET_USER_ID = 相手のID # ←ここだけ書き換え！
GITHUB_REPO = "kayutya/jaijiauto"
GH_TOKEN = os.getenv("GH_TOKEN")

# 最初はスタンプ機能をOFFにしておく
is_active = False

@client.event
async def on_ready():
    print(f'受付ボット起動: {client.user}')

@client.event
async def on_message(message):
    global is_active
    
    # コマンド判定（!on でスタンプ有効）
    if message.content == "!on":
        is_active = True
        await message.channel.send("ガイジが騒ぎ出しました。スタンプを押します。")
        return
    
    # コマンド判定（!off でスタンプ無効）
    if message.content == "!off":
        is_active = False
        await message.channel.send("ガイジは休憩に入りました。")
        return

    # スタンプ機能がONのときだけ動作
    if is_active and message.author.id == TARGET_USER_ID:
        for emoji in ["♿", "🇬", "🇦", "🇮", "🇯"]:
            await message.add_reaction(emoji)

client.run(os.getenv('DISCORD_BOT_TOKEN'))
