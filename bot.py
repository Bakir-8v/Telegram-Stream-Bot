from pyrogram import Client, filters
import logging
import os
logging.basicConfig(level=logging.INFO)

# 🚀 المفاتيح المدمجة مباشرة في الكود
API_ID = 26238667
API_HASH = "d37f76cd40cb005e6b47b88c59cc69d9"
BOT_TOKEN = "8334862751:AAFmBZeoS0xAZ1ZIPXFQgB0P-GNLvZYnHRQ" 

app = Client(
    "sketchwareX_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("أهلاً بك! أرسل لي ملف فيديو لاستخراج رابط CDN.", quote=True)

@app.on_message(filters.media & filters.private)
async def simple_link_extract(client, message):
    initial_message = await message.reply_text("بدء عملية الاستخراج...", quote=True)
    try:
        # تحديد كائن الملف
        if message.video:
            file_obj = message.video
        elif message.document and message.document.mime_type.startswith('video'):
             file_obj = message.document
        else:
            await initial_message.edit_text("❌ الرجاء إرسال فيديو أو وثيقة فيديو.")
            return

        # استخدام export_file_link (الطريقة الأكثر مباشرة)
        file_link = await client.export_file_link(file_obj) 

        if not file_link:
            await initial_message.edit_text("❌ فشل استخراج الرابط المباشر. يرجى التأكد من أن الملف غير محمي.")
            return
            
        await initial_message.edit_text(f"**✅ الرابط المباشر جاهز:**\n\n`{file_link}`")
    except Exception as e:
        await initial_message.edit_text(f"❌ فشل الاستخراج. (الخطأ: {str(e)})")

if __name__ == '__main__':
    print("البوت جاهز للعمل...")
    app.run()
