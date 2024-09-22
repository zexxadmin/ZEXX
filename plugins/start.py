def start_command(bot, message):
    user_first_name = message.from_user.first_name
    start_message = f"""
Hello, {user_first_name}! Welcome to the bot. 🌟

Here are some commands you can use:
/menu - Shows Menu
/help - About Commands

Type /menu to see the available options.
"""
    bot.reply_to(message, start_message)