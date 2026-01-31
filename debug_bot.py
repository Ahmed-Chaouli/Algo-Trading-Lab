import requests
import config

print("🔍 جاري فحص الاتصال مع تليجرام...")
# طباعة جزء صغير من التوكين للتأكد أنه مقروء
print(f"🔑 مفتاح البوت: {config.TELEGRAM_TOKEN[:10]}...") 
print(f"🆔 رقم الشات: {config.CHAT_ID}")

# المحاولة 1: إرسال رسالة تجريبية
print("\n📡 جاري محاولة الإرسال...")
url_send = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
params = {"chat_id": config.CHAT_ID, "text": "🔔 تجربة اتصال من المهندس أحمد"}

try:
    response = requests.get(url_send, params=params)
    result = response.json()
    
    if response.status_code == 200:
        print("\n✅ نجاح! تليجرام قبل الرسالة. (تحقق من هاتفك الآن)")
    else:
        print(f"\n❌ فشل الإرسال! السيرفر رفض الطلب.")
        print(f"⚠️ رمز الخطأ: {response.status_code}")
        print(f"📝 رسالة الرفض: {result}")
        
        # المحاولة 2: البحث عن الآيدي الصحيح تلقائياً
        print("\n🔎 جاري البحث عن الآيدي الصحيح في التحديثات...")
        url_updates = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getUpdates"
        up_res = requests.get(url_updates).json()
        
        if "result" in up_res and len(up_res["result"]) > 0:
            # محاولة استخراج آخر شخص تحدث مع البوت
            last_msg = up_res["result"][-1]
            if "message" in last_msg:
                correct_id = last_msg["message"]["chat"]["id"]
                sender = last_msg["message"]["from"]["first_name"]
                print(f"💡 وجدنا رسالة من: {sender}")
                print(f"✅ الآيدي الصحيح هو: {correct_id}")
                print("👉 انسخ هذا الرقم وضعه في ملف config.py بدلاً من الرقم القديم.")
            else:
                 print("⚠️ وجدنا نشاطاً لكنه ليس رسالة نصية.")
        else:
            print("⚠️ البوت لا يرى أي رسائل منك.")
            print("👉 الحل: افتح البوت في هاتفك، واضغط Start، وارسل كلمة Hello، ثم شغل هذا الكود مرة أخرى.")

except Exception as e:
    print(f"🔥 خطأ برمجي: {e}")