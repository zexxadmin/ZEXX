import telebot
from flask import Flask, send_from_directory
import config
from urllib.parse import quote as url_quote  # Updated import
from flask.cli import get_debug_flag

# Initialize bot and Flask app
bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)

# Load commands from the plugins
import plugins.menu
import plugins.start
import plugins.text_effects
import plugins.account_checker  # Import the account checker plugin

# Commands
@bot.message_handler(commands=['menu'])
def send_menu(message):
    plugins.menu.menu_command(bot, message)

@bot.message_handler(commands=['start'])
def send_start(message):
    plugins.start.start_command(bot, message)

@bot.message_handler(commands=['check'])  # Register the check command
def check_account(message):
    plugins.account_checker.check_account_command(bot, message)

# Register text effect commands
plugins.text_effects.text_effect_commands(bot)

# Start the Flask website
@app.route('/')
def index():
    return "This is the ZEXX bot website with information about the bot."

# Serve static files from the public folder
@app.route('/public/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('public', filename)

# Function to start bot and website
def start():
    bot.polling()  # Start the bot
    app.run(port=3000, host='0.0.0.0')  # Ensure the Flask server is publicly accessible

if __name__ == "__main__":
    start()