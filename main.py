from playwright.async_api import async_playwright
import asyncio
import requests

TELEGRAM_BOT_TOKEN = "7660484913:AAG1Zr1QgXIchajpnol9wiLELBG8yHTC1rU"
TELEGRAM_CHAT_ID = "293528381"

EO_EMAIL = "nushily1@gmail.com"
EO_PASSWORD = "Ya12345678"

async def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # تسجيل الدخول
        await page.goto("https://client.expertoption.com/en/login")
        await page.fill('input[name="email"]', EO_EMAIL)
        await page.fill('input[name="password"]', EO_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(10000)  # انتظار تحميل الحساب

        # الذهاب لسوق SMARTY
        await page.goto("https://client.expertoption.com/en/market/SMARTY")
        await page.wait_for_timeout(5000)

        previous_price = None

        while True:
            # قراءة السعر (تحتاج تعديل محدد CSS الصحيح للسعر)
            price_element = await page.query_selector('.price-class')  # عدل هنا بالمحدد الصحيح
            if not price_element:
                await asyncio.sleep(5)
                continue

            price_text = await price_element.inner_text()
            price = float(price_text.replace(",", "").strip())

            recommendation = "انتظار"
            if previous_price:
                if price > previous_price:
                    recommendation = "شراء (BUY)"
                elif price < previous_price:
                    recommendation = "بيع (SELL)"

            message = f"التوصية الحالية: {recommendation}\nالسعر: {price}"
            await send_telegram_message(message)

            previous_price = price
            await asyncio.sleep(60)

asyncio.run(run())
