import os
import random
from flask import Flask, request
from threading import Thread

from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "inn5bot")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):
    await update.message.reply_text(
        "💣 Bienvenue sur Inn5bot !\n\n"
        "Commandes :\n"
        "/mines — choisir 5 cases\n"
        "/proba — voir les probabilités"
    )


async def mines(update: Update, context):
    cases = list(range(1, 26))
    choix = random.sample(cases, 5)

    await update.message.reply_text(
        "🎯 Mes 5 choix aléatoires :\n\n"
        f"➡️ {choix[0]}\n"
        f"➡️ {choix[1]}\n"
        f"➡️ {choix[2]}\n"
        f"➡️ {choix[3]}\n"
        f"➡️ {choix[4]}\n\n"
        "⚠️ Choix aléatoires : le bot ne connaît pas "
        "l'emplacement réel des bombes."
    )


async def proba(update: Update, context):
    await update.message.reply_text(
        "📊 Mines 5×5 avec 3 bombes\n\n"
        "1 case : 88,00 %\n"
        "2 cases : 77,00 %\n"
        "3 cases : 66,96 %\n"
        "4 cases : 57,83 %\n"
        "5 cases : 49,57 %\n\n"
        "⚠️ Ces probabilités ne garantissent aucun bénéfice."
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("mines", mines))
telegram_app.add_handler(CommandHandler("proba", proba))


@app.get("/")
def home():
    return "Inn5bot fonctionne !"


@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"


def run_flask():
    app.run(host="0.0.0.0", port=PORT)


async def setup():
    await telegram_app.initialize()
    await telegram_app.start()

    webhook_url = os.environ["WEBHOOK_URL"]

    await telegram_app.bot.set_webhook(
        url=f"{webhook_url}/webhook/{WEBHOOK_SECRET}"
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(setup())

    Thread(target=run_flask).start()

    try:
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
