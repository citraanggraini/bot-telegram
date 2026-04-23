tufrom telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re

# GANTI TOKEN KAMU
TOKEN = "8771703967:AAH9-l96ZZ7DQkuvYJwM7ZL9qplpD9j8DQs"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # pisah per baris
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    resi = "-"
    isi = "-"
    total = "-"
    nomor = "-"  # sengaja dikosongkan

    for i, line in enumerate(lines):

        # ambil resi
        if "No Resi" in line:
            try:
                resi = line.split(":")[1].strip()
            except:
                pass

        # ambil isi paket
        if "Barang" in line:
            try:
                isi = lines[i + 1].replace("┗", "").strip()
            except:
                pass

        # ambil harga (hanya Rp saja)
        if "Rp" in line:
            cocok = re.search(r'Rp[\d\.\,]+', line)
            if cocok:
                total = cocok.group()

    pesan = f"""Halo! Ini adalah kurir anda dari *JNT Xpress* Ini ada paket.

*Resi*:{resi}
   
*Isi paket*: {isi}
  
*Nomor*: {nomor}

*Total*: {total}

Mohon maaf sebelum nya untuk paket COD harap melakukan transfer dahulu ke

*BTN*
*Rek : 100301700002153*
*A/n : Angga Darma Saputra*

Sesuai ketentuan yang berlaku, apabila tidak bersedia melanjutkan, paket akan dikembalikan.
Jika pembayaran telah dilakukan hari ini, paket akan segera diproses untuk pengiriman.

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
