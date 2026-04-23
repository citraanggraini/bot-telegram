from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "GANTI_DENGAN_TOKEN_BARU"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    blocks = [b.strip() for b in text.split("---") if b.strip()]

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]

        resi = lines[0] if len(lines) > 0 else "-"
        isi = lines[1] if len(lines) > 1 else "-"
        nomor = lines[2] if len(lines) > 2 else "-"
        total = lines[3] if len(lines) > 3 else "-"

        pesan = f"""Halo 👋

Berikut informasi paket Anda:

📦 Resi: {resi}
📄 Isi paket: {isi}
📱 Nomor: {nomor}
💰 Total: {total}

Terima kasih.
"""

        await update.message.reply_text(pesan)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
