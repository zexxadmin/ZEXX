import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

# Setup a retry strategy for requests
session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Function to escape Markdown V2 special characters
def escape_markdown(text):
    escape_chars = r'_*[\]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Convert timestamp to a readable date format
def format_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%m/%d/%Y %I:%M %p')
    except ValueError:
        return 'N/A'

def check_account_command(bot, message):
    try:
        args = message.text.split()[1:]

        # Check if both region and uid are provided
        if len(args) != 2:
            bot.send_message(message.chat.id, "Invalid command usage. Use /check [region] [user id].\n\nExample: /check IND 1633864660")
            return

        region = args[0]
        uid = args[1]

        url = f"https://free-ff-api-src-5plp.onrender.com/api/v1/account?region={region}&uid={uid}"
        
        # Use session to send request with a timeout and retry logic
        response = session.get(url, timeout=60)

        if response.status_code == 200:
            data = response.json()

            # Extract key information from the data
            basic_info = data.get('basicInfo', {})
            clan_info = data.get('clanBasicInfo', {})
            captain_info = data.get('captainBasicInfo', {})
            pet_info = data.get('petInfo', {})
            social_info = data.get('socialInfo', {})
            credit_score_info = data.get('creditScoreInfo', {})

            # Escape special characters in user inputs and outputs to avoid Markdown issues
            nickname = escape_markdown(basic_info.get('nickname', 'N/A'))
            clan_name = escape_markdown(clan_info.get('clanName', 'N/A'))
            captain_name = escape_markdown(captain_info.get('nickname', 'N/A'))
            pet_name = escape_markdown(pet_info.get('name', 'N/A'))
            signature = escape_markdown(social_info.get('signature', 'N/A'))

            # Format the message with Markdown V2
            account_info = f"""
            REAPER PLAYER INFO - FF BOT

            ┌📰 PLAYER ACTIVITY
            ├─Login At: {format_timestamp(basic_info.get('lastLoginAt', '0'))}
            └─Created At: {format_timestamp(basic_info.get('createAt', '0'))}

            ┌🎏 BASIC INFO
            ├─Nickname: {nickname}
            ├─UID: {basic_info.get('uid', 'N/A')}
            ├─Region: {basic_info.get('region', 'N/A')}
            ├─Level: {basic_info.get('level', 'N/A')}
            ├─Badge Count: {basic_info.get('badgeCnt', 'N/A')}
            ├─Liked: {basic_info.get('liked', 'N/A')}
            ├─Avatar: {basic_info.get('headPic', 'N/A')}
            ├─Banner: {basic_info.get('bannerId', 'N/A')}
            └─Exp: {basic_info.get('exp', 'N/A')}

            ┌🗾 PLAYER RANKS
            ├─BR Rank Point: {basic_info.get('rank', 'N/A')}
            ├─BR Rank Score: {basic_info.get('rankingPoints', 'N/A')}
            ├─CS Rank Point: {basic_info.get('csRank', 'N/A')}
            ├─CS Rank Score: {basic_info.get('csRankingPoints', 'N/A')}
            ├─BR Rank: {basic_info.get('rank', 'N/A')}
            └─CS Rank: {basic_info.get('csRank', 'N/A')}

            ┌🌹 SOCIAL INFO
            ├─Time Active: {social_info.get('timeActive', 'N/A')}
            ├─Language: {social_info.get('language', 'N/A')}
            ├─Prefer Mode: {social_info.get('brPregameShowChoices', 'N/A')}
            ├─Title: {social_info.get('title', 'N/A')}
            └─Signature: {signature}

            ┌🎐 GUILD INFO
            ├─Guild Name: {clan_name}
            ├─Guild ID: {clan_info.get('clanId', 'N/A')}
            ├─Guild Level: {clan_info.get('clanLevel', 'N/A')}
            ├─Members: {clan_info.get('memberNum', 'N/A')}
            ├─Guild Capacity: {clan_info.get('capacity', 'N/A')}
            ├─Leader Name: {captain_name}
            └─Leader UID: {captain_info.get('accountId', 'N/A')}
            """

            # Escape Markdown special characters
            account_info = escape_markdown(account_info)

            bot.send_message(message.chat.id, account_info, parse_mode='MarkdownV2')

        else:
            bot.send_message(message.chat.id, f"API error: {response.status_code}. Please try again later.")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")