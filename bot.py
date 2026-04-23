from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# MASUKKAN TOKEN BOT DI SINI
TOKEN = "8771703967:AAH9-l96ZZ7DQkuvYJwM7ZL9qplpD9j8DQs"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    blocks = [b.strip() for b in text.split("---") if b.strip()]

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]

        resi = lines[0] if len(lines) > 0 else "-"
        isi = lines[1] if len(lines) > 1 else "-"
        nomor = lines[2] if len(lines) > 2 else "-"
        total = lines[3] if len(lines) > 3 else "-"
        
        pesan = f"""Halo! Ini adalah kurir anda dari *JNT Xpress*! Ini ada paket.

Resi: {resi}
Isi paket: {isi}
Nomor: {nomor}
Total: Rp{harga}

Mohon maaf sebelum nya untuk paket COD harap melakukan transfer dahulu ke

*BTN*
*Rek : 100301700002153*
*A/n : Angga Darma Saputra*

Sesuai ketentuan yang berlaku, apabila tidak bersedia melanjutkan, paket akan dikembalikan.
Jika pembayaran telah dilakukan hari ini, paket akan segera diproses untuk pengiriman.

Terima kasih.
"""

        await update.message.reply_text(pesan, parse_mode="Markdown")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
