import yfinance as yf
import time
from datetime import datetime

# دالة لجلب السعر (نفس السابقة)
def get_latest_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info['last_price']
        return round(price, 2)
    except:
        return 0.0

print("🎯 نظام القناص (Sniper Bot) جاهز للعمل...")
print("-" * 40)

# 1. نطلب من المستخدم تحديد الهدف
target_symbol = "BTC-USD"  # سنركز على البيتكوين لأنه يعمل الآن
print(f"السعر الحالي للبيتكوين هو: ${get_latest_price(target_symbol)}")

target_price = float(input("أدخل السعر الذي تريد الشراء عنده (Target Price): "))
print(f"✅ تم ضبط الهدف عند ${target_price}. جاري المراقبة...")
print("-" * 40)

# 2. حلقة المراقبة الذكية
while True:
    current_price = get_latest_price(target_symbol)
    now = datetime.now().strftime("%H:%M:%S")
    
    # الفرق بين السعر الحالي والهدف
    diff = current_price - target_price
    
    if current_price <= target_price:
        # 🚨 تحقق الشرط! (السعر نزل إلى هدفك أو أقل)
        print(f"\n🔥🔥 [ALARM] {now} | السعر وصل للهدف! (${current_price})")
        print("🚀 BUY! BUY! BUY!")
        break # نوقف البرنامج لأننا اصطدنا الفرصة
        
    else:
        # لم يتحقق الشرط بعد
        print(f"👀 {now} | BTC: ${current_price} | ما زال بعيداً بـ ${round(diff, 2)}")
    
    time.sleep(3) # تحديث كل 3 ثواني