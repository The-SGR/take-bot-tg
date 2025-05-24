import telebot #весело да
from configuration import * # Н И К О Л А Й

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id,"День добрый!\nНапиши сюда свой тейк и мы его, возможно, опубликуем!")

@bot.message_handler(commands=['github'])
def github_msg(message):
    bot.send_message(message.chat.id, "https://github.com/The-SGR/take-bot-tg")

@bot.message_handler(func=lambda message: True, content_types=["text", "animation", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def forward_msg(message):
    user_id = message.from_user.id

    if user_id not in admins:
        for admin in admins:
            try:
                bot.forward_message(
                    chat_id=admin,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
            except Exception as e:
                print(f"Ошибка: {e}")




if __name__ == "__main__":
    print("[!] Бот онлайн")
    bot.infinity_polling()