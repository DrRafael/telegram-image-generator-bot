import os
import telebot
from config import API_KEY, SECRET_KEY, TOKEN
from logic import Text2ImageAPI

bot = telebot.TeleBot(TOKEN)
api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles /start command with onboarding message."""
    welcome_text = (
        "Hello! Send me any text prompt in English or Russian, "
        "and I will generate an AI image for you using Kandinsky API."
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Processes user text input and replies with generated AI photo."""
    prompt = message.text
    status_msg = bot.reply_to(message, "Generating your image, please wait...")

    try:
        model_id = api.get_model()
        uuid = api.generate(prompt, model_id)
        images = api.check_generation(uuid)

        if images:
            file_path = f"temp_{message.chat.id}.jpg"
            api.save_image(images[0], file_path)

            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)

            # Clean up local temporary file
            if os.path.exists(file_path):
                os.remove(file_path)

            bot.delete_message(message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text("Failed to generate image. Please try again.", message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"An error occurred: {str(e)}", message.chat.id, status_msg.message_id)


if __name__ == "__main__":
    bot.infinity_polling()
