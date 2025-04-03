import telebot
import openai
import os

# Отримуємо токени з оточення
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Ти — чемний консультант магазину ВелоТорба. "
                    "Відповідай українською, без води, просто і по суті."
                )},
                {"role": "user", "content": message.text}
            ]
        )
        bot.send_message(message.chat.id, response["choices"][0]["message"]["content"])
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Вибач, сталася помилка. Напиши пізніше.")

bot.polling()
