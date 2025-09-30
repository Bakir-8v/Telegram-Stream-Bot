from pyrogram import Client, filters
import logging

# إعدادات بسيطة لتسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# ⚠️ المفاتيح الخاصة بك - تم دمجها مباشرةً
API_ID = 24186368
API_HASH = "828bc85c425b3cdf00b53adb1bf4af8c"
BOT_TOKEN = "8017200832:AAGkoi8RkCmBsHQnuCJDq6YOiMwa8jEPobk" 

# تهيئة البوت
app = Client(
    "stream_link_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

# دالة استقبال أمر البداية /start
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "أهلاً بك! أنا بوت استخراج الروابط المباشرة. 🔗\n\n"
        "للحصول على رابط تشغيل مباشر (CDN) لملفاتك، **أرسل لي ملف فيديو أو وثيقة** مباشرة في هذه المحادثة.", 
        quote=True
    )

# دالة معالجة الملفات الواردة (تم استخدام الطريقة المضمونة لـ export_file_link)
@app.on_message(filters.media & filters.private)
async def get_direct_link(client, message):
    initial_message = await message.reply_text("بدء عملية الاستخراج... يرجى الانتظار.", quote=True)
    
    try:
        file_object = None
        
        # تحديد كائن الملف
        if message.video:
            file_object = message.video
        elif message.document and message.document.mime_type.startswith('video'):
             file_object = message.document
        
        if file_object is None:
            await initial_message.edit_text("❌ الرجاء إرسال ملف فيديو أو وثيقة فيديو مدعومة فقط.")
            return

        # **الطريقة النهائية والأكثر ثباتاً:** استخدام export_file_link
        # هذه الدالة تتجاوز مشاكل الـ async_generator وتُعطي رابط CDN مباشر في العادة.
        file_link = await client.export_file_link(file_object)

        if not file_link:
            await initial_message.edit_text(
                "❌ فشل استخراج الرابط المباشر. قد تكون المشكلة في صلاحيات API أو أن الملف محمي."
            )
            return

        # الرد بالرابط المباشر
        await initial_message.edit_text(
            f"**✅ الرابط المباشر جاهز:**\n\n`{file_link}`"
        )
        logging.info(f"Successfully generated link for user: {message.from_user.id}")
            
    except Exception as e:
        # رسالة في حال حدوث خطأ
        logging.error(f"Error processing message: {e}")
        await initial_message.edit_text(f"❌ فشل استخراج الرابط. يرجى مراجعة سجلات Railway. (تفاصيل الخطأ: {str(e)})")

# تشغيل البوت
if __name__ == '__main__':
    print("البوت جاهز للعمل. يتم الآن محاولة الاتصال بتيليجرام...")
    app.run()
