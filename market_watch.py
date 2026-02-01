import yfinance as yf
import time
import requests
import pandas as pd
from datetime import datetime
import config

# --- إعدادات التحكم ---
SYMBOL = "BTC-USD"      # العملة
CHECK_INTERVAL = 60     # فحص كل دقيقة
COOLDOWN_MINUTES = 30   # لا تكرر التنبيه لنفس الحالة قبل 30 دقيقة

# متغيرات لتخزين وقت آخر تنبيه
last_buy_alert = 0
last_sell_alert = 0

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": config.CHAT_ID, "text": msg}
        requests.get(url, params=params)
        print("✅ [Telegram] تم الإرسال.")
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")

def calculate_rsi(symbol, period=14):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d", interval="1h")
        if data.empty: return 50, 0
        
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2), round(data['Close'].iloc[-1], 2)
    except:
        return 50, 0

print(f"🚀 القناص الصامت يعمل... (تنبيه كل {COOLDOWN_MINUTES} دقيقة)")

while True:
    rsi, price = calculate_rsi(SYMBOL)
    current_time = time.time()
    
    # 🟢 استراتيجية الشراء (RSI < 30)
    if rsi <= 30:
        # هل مر وقت كافٍ منذ آخر تنبيه؟
        if (current_time - last_buy_alert) > (COOLDOWN_MINUTES * 60):
            msg = f"🔥 فرصة شراء قوية!\n\nالعملة: {SYMBOL}\nالسعر: ${price}\nRSI: {rsi}\n\nسأصمت لمدة {COOLDOWN_MINUTES} دقيقة."
            send_telegram_message(msg)
            last_buy_alert = current_time # تحديث وقت التنبيه
            print(f"🔔 تم إرسال تنبيه شراء (RSI: {rsi})")
        else:
            print(f"⏳ فرصة شراء مستمرة (RSI: {rsi}) - في وضع الصمت...")

    # 🔴 استراتيجية البيع (RSI > 70)
    elif rsi >= 70:
        if (current_time - last_sell_alert) > (COOLDOWN_MINUTES * 60):
            msg = f"⚠️ خروج / بيع!\n\nالعملة: {SYMBOL}\nالسعر: ${price}\nRSI: {rsi}\n\nسأصمت لمدة {COOLDOWN_MINUTES} دقيقة."
            send_telegram_message(msg)
            last_sell_alert = current_time
            print(f"🔔 تم إرسال تنبيه بيع (RSI: {rsi})")
        else:
            print(f"⏳ تشبع شرائي مستمر (RSI: {rsi}) - في وضع الصمت...")

    else:
        print(f"📉 {datetime.now().strftime('%H:%M')} | {SYMBOL}: ${price} | RSI: {rsi} (محايد)")
    
    time.sleep(CHECK_INTERVAL)