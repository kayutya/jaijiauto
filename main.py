import discord
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- Renderの強制終了を防ぐためのダミーサーバー ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active")

def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    httpd.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()

# --- ボット本体 ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 先ほど送ってくれたIDをセットしました
TARGET_USER_ID = 1172772592534568971 

is_active = False

@client.event
async def on_ready():
    print(f'準備完了: {client.user}')

@client.event
async def on_message(message):
    global is_active
    
    if message.author.id == client.user.id:
        return

    # コマンド判定
    if message.content == "!on":
        is_active = True
        await message.channel.send("ガイジが騒ぎ出しました。スタンプを押します。")
        return
    
    if message.content == "!off":
        is_active = False
        await message.channel.send("ガイジは休憩に入りました。")
        return

    # スタンプ実行（指定のIDのユーザーが喋った時のみ）
    if is_active and message.author.id == TARGET_USER_ID:
        emojis = ["♿", "🇬", "🇦", "🇮", "🇯"]
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except Exception as e:
                print(f"Error: {e}")

# Renderの環境変数からトークンを読み込む
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
