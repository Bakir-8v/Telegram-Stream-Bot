from pyrogram import Client, filters
import logging
from pyrogram.types import Message

# إعدادات بسيطة لتسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# 🚀 المفاتيح المدمجة مباشرة في الكود
API_ID = 26238667
API_HASH = "d37f76cd40cb005e6b47b88c59cc69d9"
BOT_TOKEN = "8334862751:AAFmBZeoS0xAZ1ZIPXFQgB0P-GNLvZYnHRQ" 


# تهيئة البوت
app = Client(
    "sketchwareX_bot", 
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

# دالة معالجة الملفات الواردة (باستخدام get_messages المضمونة)
@app.on_message(filters.media & filters.private)
async def get_direct_link(client: Client, message: Message):
    initial_message = await message.reply_text("بدء عملية الاستخراج... يرجى الانتظار.", quote=True)
    
    try:
        file_object = None
        
        if message.video:
            file_object = message.video
        elif message.document and message.document.mime_type.startswith('video'):
             file_object = message.document
        
        if file_object is None:
            await initial_message.edit_text("❌ الرجاء إرسال ملف فيديو أو وثيقة فيديو مدعومة فقط.")
            return

        # 1. استرجاع كائن الرسالة مرة أخرى بطريقة أكثر ضماناً
        full_message = await client.get_messages(
            chat_id=message.chat.id,
            message_ids=message.id
        )
        
        # 2. استخدام download_media على كائن الرسالة الكامل
        file_link = await client.download_media(full_message, in_memory=True)

        if not isinstance(file_link, str) or not file_link.startswith('/'):
            await initial_message.edit_text(
                "❌ فشل استخراج الرابط المباشر. يرجى التأكد من أن الملف غير محمي."
            )
            return

        # الرد بالرابط المباشر
        await initial_message.edit_text(
            f"**✅ الرابط المباشر جاهز:**\n\n`{file_link}`"
        )
        logging.info(f"Successfully generated link for user: {message.from_user.id}")
            
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await initial_message.edit_text(f"❌ فشل استخراج الرابط. (تفاصيل الخطأ: {str(e)})")

# تشغيل البوت
if __name__ == '__main__':
    print("البوت جاهز للعمل. يتم الآن محاولة الاتصال بتيليجرام...")
    app.run()
