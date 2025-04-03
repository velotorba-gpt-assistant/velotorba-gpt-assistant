import os
import telebot
import openai
import traceback

# Отримуємо токени з оточення Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація ботів
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я готовий допомогти із запитаннями щодо велотоварів.")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    try:
        # Виклик до OpenAI GPT
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ти — уважний консультант магазину ВелоТорба. "
                        "Відповідай українською мовою, давай корисні поради. "
                        "Якщо не знаєш, кажи звернутися до менеджера."
                    )
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )
        reply_text = completion.choices[0].message.content
        bot.send_message(message.chat.id, reply_text)

    except Exception as e:
        # Друкуємо повний traceback у логах Render для відладки
        err_text = traceback.format_exc()
        print("=== ПОМИЛКА GPT ===\n", err_text)
        
        # Відправляємо повідомлення користувачу
        bot.send_message(
            message.chat.id,
            "⚠️ Вибач, сталася помилка. Напиши пізніше."
        )

if __name__ == "__main__":
    bot.polling()
