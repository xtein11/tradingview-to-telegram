from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Твои данные Telegram
BOT_TOKEN = "7960236842:AAHh8VL9Q9cUVa_H1rlDqWHRtoDE2iCsC2Q"
CHAT_ID = -1002959148032

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Основные поля
        ticker = data.get("ticker", "UNKNOWN")
        price = data.get("price", "N/A")
        action = data.get("strategy", {}).get("order_action", "N/A").upper()
        take_profit = data.get("strategy", {}).get("take_profit", "N/A")
        stop_loss = data.get("strategy", {}).get("stop_loss", "N/A")
        strength = data.get("strategy", {}).get("signal_strength", "medium").lower()

        # Эмодзи
        action_emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "⚡"
        strength_emoji = {"high": "🔥", "medium": "⚡", "low": "💧"}.get(strength, "⚡")

        # Формируем карточку
        message_lines = [
            f"{action_emoji} {strength_emoji} *TradingView Сигнал*",
            "─────────────────────────",
            f"*Действие:* {action}",
            f"*Актив:* {ticker}",
            f"*Цена входа:* {price}"
        ]

        if take_profit != "N/A":
            message_lines.append(f"🎯 *Take Profit:* {take_profit}")
        if stop_loss != "N/A":
            message_lines.append(f"🛑 *Stop Loss:* {stop_loss}")

        message_lines.append("─────────────────────────")
        message_text = "\n".join(message_lines)

        # Отправка в Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        r = requests.post(url, json=payload)

        return jsonify({"status": "success", "telegram_response": r.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
