import telebot
from configuration import *
from telebot import apihelper

PROXY_URL = "неа"
apihelper.proxy = {'http': PROXY_URL, 'https': PROXY_URL}

bot = telebot.TeleBot(token)
forwarded_messages = {}

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id,"<b>Добра!</b>\nНапишите сюда свой тейк и мы его, возможно, опубликуем!\n\nЕсли интересен код этого бота — /github", parse_mode='html')

@bot.message_handler(commands=['github'])
def github_msg(message):
    bot.send_message(message.chat.id, "https://github.com/The-SGR/take-bot-tg")

@bot.message_handler(func=lambda m: m.from_user.id in admins and m.reply_to_message)
def admin_reply(message):
    key = (message.chat.id, message.reply_to_message.message_id)
    if key not in forwarded_messages:
        return

    user_chat, user_message_id = forwarded_messages[key]

    bot.send_message(user_chat, f"<b>Ответ от администратора {message.from_user.first_name} (@{message.from_user.username}):</b>\n\n<blockquote>{message.text}</blockquote>", parse_mode="HTML", reply_to_message_id=user_message_id)

    for admin in admins:
        if admin == message.from_user.id:
            continue

        bot.send_message(admin, f"<b>{message.from_user.first_name} ответил пользователю:</b>", parse_mode="HTML")
        bot.copy_message(admin, message.chat.id, message.message_id)

@bot.message_handler(func=lambda message: True, content_types=["text", "animation", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def forward_msg(message):
    user_id = message.from_user.id

    if user_id not in admins:
        bot.reply_to(message, "<b>Сообщение успешно отправлено!</b>", parse_mode='html')
        for admin in admins:
            try:
                username = f"@{message.from_user.username}" if message.from_user.username else "Юзернейм отсутствует"

                bot.send_message(admin, f"<b>Сообщение от:</b> {message.from_user.first_name} ({username})", parse_mode="HTML")
                forwarded = bot.forward_message(chat_id=admin, from_chat_id=message.chat.id, message_id=message.message_id)
                forwarded_messages[(admin, forwarded.message_id)] = (message.chat.id, message.message_id)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    print("[!] Бот онлайн")
    bot.infinity_polling()

#ывлотаоылтвалтоытвлоалотывалотцыолау4ц