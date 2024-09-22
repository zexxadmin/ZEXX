# plugins/menu.py
def menu_command(bot, message):
    menu_message = """
ZEXX MENU 🎏
/menu - Shows Menu
/check [server] [uid] - Info About FF account
/help - About Commands
/rmbg - Removes background from image
/tiktok [video link] - Downloads TikTok video without watermark

More Commands Are coming soon ….
"""
    bot.reply_to(message, menu_message)