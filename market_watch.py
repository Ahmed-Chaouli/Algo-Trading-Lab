import yfinance as yf
import time
import requests  # تم التصحيح هنا
from datetime import datetime
import config

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": config.CHAT_ID, "text": msg}
        requests.get(url, params=params)
        print("✅ [Telegram] تم إرسال الرسالة بنجاح!")
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")

def get_price(symbol):
    try:
        return round(yf.Ticker(symbol).fast_info['last_price'], 2)
    except:
        return 0.0

print("🚀 قناص التليجرام جاهز...")
symbol = "BTC-USD"
current = get_price(symbol)
print(f"💰 السعر الحالي للبيتكوين: ${current}")

# نضع هدفاً سهلاً للتجربة (أعلى من السعر الحالي)
target = float(input("أدخل سعراً للتنبيه (ضع سعراً أعلى من الحالي لتجرب فوراً): "))

while True:
    price = get_price(symbol)
    now = datetime.now().strftime("%H:%M:%S")
    print(f"⏳ {now} | BTC: ${price} | الهدف: {target}")
    
    if price <= target:
        message = f"🚨 تنبيه عاجل!\n\nالسعر وصل: ${price}\nالوقت: {now}\n\nتحرك الآن!"
        send_telegram_message(message)
        break
    
    time.sleep(3)