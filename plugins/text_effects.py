import requests
from io import BytesIO

def text_maker(effect_url, text):
    try:
        response = requests.post(effect_url, data={'text': text})
        print(f"Text Maker Response Status Code: {response.status_code}")  # Debug print
        print(f"Response Text: {response.text}")  # Print raw response text
        
        if response.status_code == 200:
            if "json" in response.headers.get("Content-Type", ""):
                try:
                    result = response.json()
                    print(f"Response JSON: {result}")  # Debug print
                    return result.get('url')
                except ValueError:
                    print("Error decoding JSON response.")
            else:
                return extract_url_from_response(response.text)
        else:
            print(f"Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return None

def extract_url_from_response(response_text):
    import re
    url_match = re.search(r'(https?://\S+)', response_text)
    return url_match.group(0) if url_match else None

def download_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        print(f"Download Response Status Code: {response.status_code}")  # Debug print
        print(f"Response Content: {response.text[:500]}")  # Print first 500 characters of response body
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"Failed to download image with status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while downloading image: {e}")
    return None

def send_text_effect(bot, message, effect_url, description):
    match = message.text.split(maxsplit=1)[1:]  # Get text after command
    if not match:
        bot.reply_to(message, f'Give me text\nExample: {description}')
        return
    
    text = match[0]
    print(f"Requesting effect for text: {text}")  # Debug print
    image_url = text_maker(effect_url, text)
    
    if image_url:
        print(f"Image URL: {image_url}")  # Debug print
        image = download_image(image_url)
        if image:
            bot.send_photo(message.chat.id, photo=image)
        else:
            bot.reply_to(message, 'Failed to download image.')
    else:
        bot.reply_to(message, 'Failed to generate text effect.')

def text_effect_commands(bot):
    bot.message_handler(commands=['sed'])(lambda message: send_text_effect(
        bot, message,
        'https://en.ephoto360.com/write-text-on-wet-glass-online-589.html',
        'sed text;example'
    ))

    bot.message_handler(commands=['steel'])(lambda message: send_text_effect(
        bot, message,
        'https://en.ephoto360.com/steel-text-effect-66.html',
        'steel text1;text2'
    ))

    bot.message_handler(commands=['metallic'])(lambda message: send_text_effect(
        bot, message,
        'https://textpro.me/create-a-metallic-text-effect-free-online-1041.html',
        'metallic text;example'
    ))

    bot.message_handler(commands=['glitch'])(lambda message: send_text_effect(
        bot, message,
        'https://textpro.me/create-glitch-text-effect-style-tik-tok-983.html',
        'glitch text1;text2'
    ))

    bot.message_handler(commands=['burn'])(lambda message: send_text_effect(
        bot, message,
        'https://photooxy.com/logo-and-text-effects/write-text-on-burn-paper-388.html',
        'burn text;example'
    ))

    bot.message_handler(commands=['8bit'])(lambda message: send_text_effect(
        bot, message,
        'https://photooxy.com/logo-and-text-effects/8-bit-text-on-arcade-rift-175.html',
        '8bit text;example'
    ))