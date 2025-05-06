import os
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    prompt = f'Определи уровень пассивной агрессии в этом сообщении и дай короткий совет:\n"{user_text}"'

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
        bot.reply_to(message, answer)
    except Exception as e:
        print("Ошибка OpenAI:", e)
        bot.reply_to(message, "Произошла ошибка при обращении к OpenAI.")

bot.polling()
