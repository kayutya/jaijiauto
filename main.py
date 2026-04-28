import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 反応したい相手のユーザーIDをここに数字で入れる
TARGET_USER_ID = 808264919862214658

# つけたいスタンプの順番
REACTIONS = ["♿", "🇬", "🇦", "🇮", "🇯"]

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    # ボット自身の発言には反応しない
    if message.author.id == client.user.id:
        return

    # 指定したユーザーIDと一致したらスタンプを押す
    if message.author.id == TARGET_USER_ID:
        for emoji in REACTIONS:
            try:
                await message.add_reaction(emoji)
            except Exception as e:
                print(f"エラー: {e}")

# GitHubのSecretsからトークンを読み込む
client.run(os.getenv('DISCORD_BOT_TOKEN'))
