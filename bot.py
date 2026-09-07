import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
CHANNEL_URL = "https://t.me/clclxptmxm"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Telegram bot is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    message = data.get("message")
    if not message:
        return "ok", 200

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    if chat_id and text.startswith("/start"):
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "📢 안내채널 입장",
                        "url": CHANNEL_URL
                    }
                ]
            ]
        }

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "안녕하세요!\n아래 버튼을 눌러주세요.",
                "reply_markup": keyboard
            },
            timeout=10
        )

    return "ok", 200


def set_webhook():
    render_url = os.environ.get("RENDER_EXTERNAL_URL")

    if render_url:
        webhook_url = f"{render_url}/webhook"

        requests.post(
            f"{TELEGRAM_API}/setWebhook",
            json={
                "url": webhook_url,
                "drop_pending_updates": True
            },
            timeout=10
        )


if __name__ == "__main__":
    set_webhook()

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
