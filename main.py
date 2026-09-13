import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💣 Bienvenue sur Inn5bot !\n\n"
        "Commandes :\n"
        "/mines — choisir 5 cases\n"
        "/proba — voir les probabilités"
    )

async def mines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cases = list(range(1, 26))
    choix = random.sample(cases, 5)

    await update.message.reply_text(
        "🎯 Mes 5 choix aléatoires :\n\n"
        f"➡️ {choix[0]}\n"
        f"➡️ {choix[1]}\n"
        f"➡️ {choix[2]}\n"
        f"➡️ {choix[3]}\n"
        f"➡️ {choix[4]}\n\n"
        "⚠️ Ce sont des choix aléatoires. "
        "Le bot ne peut pas connaître les vraies bombes."
    )

async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Mines 5×5 avec 3 bombes\n\n"
        "1 case : 88,00 % de survie\n"
        "2 cases : 77,00 %\n"
        "3 cases : 66,96 %\n"
        "4 cases : 57,83 %\n"
        "5 cases : 49,57 %\n\n"
        "⚠️ Les probabilités ne garantissent aucun bénéfice."
    )

def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mines", mines))
    app.add_handler(CommandHandler("proba", proba))

    app.run_polling()

if __name__ == "__main__":
    main()
