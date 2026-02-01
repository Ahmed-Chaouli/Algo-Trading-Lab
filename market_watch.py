import yfinance as yf
import time
import requests
import pandas as pd  # مكتبة تحليل البيانات
import config

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
        # جلب بيانات آخر 100 شمعة (ساعة)
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d", interval="1h") # شمعة كل ساعة
        
        if data.empty: return 50
        
        # معادلة RSI الرياضية
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi.iloc[-1], 2), round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"⚠️ خطأ في الحساب: {e}")
        return 50, 0

print("🚀 قناص RSI الذكي يعمل...")
symbol = "BTC-USD"

while True:
    
    rsi, price = calculate_rsi(symbol)
    status = "محايد 😐"
    
    if rsi <= 30:
        status = "فرصة شراء قوية 🟢"
        msg = f"🚨 تنبيه شراء!\n\nالعملة: {symbol}\nالسعر: ${price}\nRSI: {rsi}\nالوضع: منطقة تشبع بيعي (Oversold)"
        send_telegram_message(msg)
    
    elif rsi >= 70:
        status = "فرصة بيع (خطر) 🔴"
        msg = f"🚨 تنبيه بيع!\n\nالعملة: {symbol}\nالسعر: ${price}\nRSI: {rsi}\nالوضع: منطقة تشبع شرائي (Overbought)"
        send_telegram_message(msg)

    print(f"📉 BTC: ${price} | RSI: {rsi} | الحالة: {status}")
    
    time.sleep(60) # فحص كل دقيقة