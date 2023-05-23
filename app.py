import telebot

from bs4 import BeautifulSoup

import requests

import os

TOKEN = "6164249318:AAGA0IiwiV4Rv31aCzUbLPLVWFUdrRO2Hds"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])

def handle_start(message):

    bot.send_message(message.chat.id, """ *Welcome! 🌟

• Bot for HTML code formatting.

• Send me your code, and I'll format it for you.

• Example: [index.html]

Feel free to ask for help! 👍😊

*""", parse_mode="Markdown")

@bot.message_handler(content_types=['document'])

def handle_document(message):

    if message.document.mime_type == 'text/html':

        file_info = bot.get_file(message.document.file_id)

        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        file_content = downloaded_file.decode('utf-8')

        soup = BeautifulSoup(file_content, 'html.parser')

        formatted_code = soup.prettify()

        temp_file_path = os.path.join(os.getcwd(), 'temp.html') 

        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:

            temp_file.write(formatted_code)

        original_file_size = get_remote_file_size(file_info.file_path)

        modified_file_size = os.path.getsize(temp_file_path) / (1024 * 1024)

        with open(temp_file_path, 'rb') as temp_file:

            bot.send_document(

                message.chat.id,

                temp_file,

                caption=f"*Original File Size: {original_file_size:.2f} MB\nModified File Size: {modified_file_size:.2f} MB*",parse_mode="Markdown"

            )

        os.remove(temp_file_path)

    else:

        error_message = "يرجى إرسال ملف HTML لتنسيقه باستخدام البوت."

        bot.reply_to(message, error_message)

def get_remote_file_size(file_path):

    full_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    response = requests.head(full_url)

    if response.status_code == 200:

        content_length = response.headers.get('content-length')

        if content_length:

            file_size = int(content_length) / (1024 * 1024) 

            return file_size

    return 0
bot.set_webhook("https://telebottestnew.herokuapp.com/")
bot.infinity_polling()

