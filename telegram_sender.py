# telegram_sender.py
import aiohttp

BOT_TOKEN = "7660484913:AAG1Zr1QgXIchajpnol9wiLELBG8yHTC1rU"
CHAT_ID = "293528381"

async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            return await resp.json()
