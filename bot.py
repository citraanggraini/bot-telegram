import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8771703967:AAEO6jLXBLFNZ9B9aFI5sivcwxe5rtcdBcs"
API_KEY = "69e6273253bfe2f379ff8ee3"

BASE_URL = "https://api.biteship.com/v1"


def format_rupiah(value):
    try:
        n = int(float(value))
        return f"Rp {n:,}".replace(",", ".")
    except Exception:
        return str(value)


def detect_primary_couriers(resi: str):
    r = resi.upper().strip()

    # JZ Lazada = J&T
    if r.startswith("JZ"):
        return ["jnt"]

    # Beberapa pola umum
    if r.startswith(("JT", "JP", "JX")):
        return ["jnt"]

    if r.startswith("JNE"):
        return ["jne"]

    # Angka panjang sering JNE, tapi kita tetap fallback ke kurir lain
    if r.isdigit():
        return ["jne", "jnt", "sicepat", "ninja", "anteraja"]

    # Default fallback
    return ["jnt", "jne", "sicepat", "ninja", "anteraja"]


def request_tracking(resi: str, courier: str):
    url = f"{BASE_URL}/trackings/{resi}/couriers/{courier}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            return None

    return None


def pick_latest_history(data: dict):
    history = data.get("history", [])

    if not history:
        return None

    # Ambil item terakhir sebagai update terbaru
    return history[-1]


def extract_payment_label(data: dict):
    """
    Tracking API tidak selalu memberi info COD/non-COD.
    Kalau ada field yang relevan, kita tampilkan.
    Kalau tidak ada, jujur bilang tidak diketahui.
    """
    cod_info = data.get("cash_on_delivery")
    if isinstance(cod_info, dict):
        amount = cod_info.get("amount")
        if amount not in (None, "", 0, "0"):
            return f"COD ({format_rupiah(amount)})"
        return "COD"

    if cod_info is True:
        return "COD"

    if cod_info is False:
        return "Non COD"

    # Cek kemungkinan field lain
    payment_type = data.get("payment_type") or data.get("payment_method")
    if payment_type:
        p = str(payment_type).lower()
        if "cod" in p:
            return "COD"
        return "Non COD"

    return "Tidak diketahui"


def build_result_text(resi: str, courier: str, data: dict):
    latest = pick_latest_history(data)

    overall_status = data.get("status", "-")
    payment_label = extract_payment_label(data)

    if latest:
        latest_status = latest.get("status", overall_status)
        latest_note = latest.get("note", "-")
        latest_time = latest.get("updated_at", "-")
    else:
        latest_status = overall_status
        latest_note = "-"
        latest_time = "-"

    courier_name = courier.upper()
    if courier == "jnt":
        courier_name = "J&T"
    elif courier == "jne":
        courier_name = "JNE"
    elif courier == "sicepat":
        courier_name = "SiCepat"
    elif courier == "ninja":
        courier_name = "Ninja"
    elif courier == "anteraja":
        courier_name = "Anteraja"

    text = (
        f"📦 Resi: {resi}\n"
        f"🚚 Kurir: {courier_name}\n"
        f"📌 Status: {latest_status}\n"
        f"📝 Keterangan: {latest_note}\n"
        f"💰 Pembayaran: {payment_label}\n"
        f"⏰ Update: {latest_time}"
    )

    return text


def check_tracking(resi: str):
    couriers = detect_primary_couriers(resi)

    for courier in couriers:
        data = request_tracking(resi, courier)
        if isinstance(data, dict):
            return build_result_text(resi, courier, data)

    return (
        "❌ Resi tidak ditemukan.\n\n"
        "Coba pastikan:\n"
        "- nomor resi benar\n"
        "- resi sudah aktif di sistem kurir\n"
        "- resi bukan baru dibuat beberapa menit lalu"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Bot aktif ✅\n\n"
        "Cara pakai:\n"
        "/cek NOMOR_RESI\n\n"
        "Contoh:\n"
        "/cek JZ10828890501\n"
        "/cek 0407372600001822"
    )
    await update.message.reply_text(text)


async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Format salah.\nContoh:\n/cek JZ10828890501"
        )
        return

    resi = context.args[0].strip()

    await update.message.reply_text("🔍 Sedang cek resi...")

    try:
        result = check_tracking(resi)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi error:\n{e}")


def main():
    if not TOKEN:
        raise ValueError("TOKEN belum diisi di Railway Variables")
    if not API_KEY:
        raise ValueError("API_KEY belum diisi di Railway Variables")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cek", cek))

    app.run_polling()


if __name__ == "__main__":
    main()
