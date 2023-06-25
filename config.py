import os

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
own_chat_id = os.getenv('OWN_CHAT_ID')
admin = int(os.getenv('ADMIN'))
company_name = os.getenv('COMPANY_NAME')