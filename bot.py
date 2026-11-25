import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==============================================================================
# CONFIGURAZIONE DEL BOT
# ==============================================================================
BOT_TOKEN = "9277326284:AAHsztFjPRlxkJ5vsdeorkHu0nQmHXevgco"
MINI_APP_URL = "https://gaspfe.github.io/Python_work/"
WELCOME_PHOTO = "benvenuto.jpg"
SUPPORT_USERNAME = "Pitoneaustrale"

INFO_TEXT = (
    "ℹ️ *INFORMAZIONI* ℹ️\n\n"
    "Si accettano ordini 24/7.\n\n"
    "Per pacchi persi/sequestrati abbiamo disponibile:\n"
    "RESHIP 100%\n\n"
    "Si effettuano spedizioni con CORRIERE TRACCIATO indifferentemente dal quantitativo di prodotto.\n\n"
    "🚚 CORRIERE 20€💰\n\n"
    "• RESHIP 100% PER NOSTRO ERRORE\n"
    "• NO REFUND PER INDIRIZZO/DESTINATARIO ERRATO (errore acquirente)\n"
    "• NO REFUND PER MANCATO RITIRO\n"
    "• NO REFUND PER RITORNO AL MITTENTE\n"
    "• NO REFUND SE SEGNA CONSEGNATO\n"
    "• NO REFUND CORRIERE/DROP/AMICO LADRO\n"
    "• IN CASO MANCASSE QUALCOSA VERRÀ EFFETTUATO UN RESHIP A CARICO NOSTRO DELLA MERCE MANCANTE SOLO IN PRESENZA DI UN VIDEO SENZA TAGLI DA QUANDO VIENE APERTO IL PACCO ALLA PESA\n"
    "• CODICE TRACKING VIENE FORNITO DOPO 48H PER QUESTIONI DI OPSEC\n"
    "• OGNI SPEDIZIONE VIENE EVASA IN MAX 72H\n"
    "• REFUND SOLO DOPO 30 GIORNI LAVORATIVI"
)
CONTACTS_TEXT = (
    "📞 *CONTATTI UTILI*\n\n"
    "Per qualsiasi problema, dubbio o informazione, puoi scrivere direttamente al nostro supporto ufficiale:\n\n"
    f"👉 Contatta l'admin: @{SUPPORT_USERNAME}"
)
# ==============================================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="ℹ️ Informazioni", callback_data="show_info"),
            InlineKeyboardButton(text="📞 Contatti", callback_data="show_contacts"),
        ],
        [
            InlineKeyboardButton(
                text="🛍️ CATALOGO",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open(WELCOME_PHOTO, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            reply_markup=get_main_keyboard()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "show_info":
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="🛍️ CATALOGO", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton(text="⬅️ Chiudi", callback_data="close_info")]
        ])
        await query.message.reply_text(
            text=INFO_TEXT,
            parse_mode="Markdown",
            reply_markup=back_keyboard
        )
    elif query.data == "show_contacts":
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="💬 Scrivi su Telegram", url=f"https://t.me/{SUPPORT_USERNAME}")],
            [InlineKeyboardButton(text="⬅️ Chiudi", callback_data="close_info")]
        ])
        await query.message.reply_text(
            text=CONTACTS_TEXT,
            parse_mode="Markdown",
            reply_markup=back_keyboard
        )
    elif query.data == "close_info":
        await query.message.delete()

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot avviato! Premi Ctrl+C per fermarlo.")
    app.run_polling()

if __name__ == "__main__":
    main()
