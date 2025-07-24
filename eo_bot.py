# eo_bot.py
import asyncio
from playwright.async_api import async_playwright
from telegram_sender import send_telegram_message
from strategies import combined_strategy  # استيراد استراتيجيات التحليل

EO_EMAIL = "nushily1@gmail.com"
EO_PASSWORD = "Ya12345678"

async def start_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # تسجيل الدخول
        await page.goto("https://client.expertoption.com/en/login")
        await page.fill('input[name="email"]', EO_EMAIL)
        await page.fill('input[name="password"]', EO_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(10000)

        # الذهاب لسوق SMARTY
        await page.goto("https://client.expertoption.com/en/market/SMARTY")
        await page.wait_for_timeout(5000)

        prices = []

        while True:
            price_element = await page.query_selector('div[class*="price"], div[class*="value"]')
            if not price_element:
                print("لم أجد عنصر السعر، أعيد المحاولة بعد 5 ثواني...")
                await asyncio.sleep(5)
                continue

            price_text = await price_element.inner_text()
            price = float(price_text.replace(",", "").strip())

            # تحديث قائمة الأسعار
            prices.append(price)
            if len(prices) > 30:
                prices.pop(0)

            # استخدام الاستراتيجية المركبة لتحليل الأسعار
            if len(prices) >= 14:
                recommendation = combined_strategy(prices)
            else:
                recommendation = "انتظار"

            message = f"التوصية الحالية: {recommendation}\nالسعر: {price}"
            print(message)
            await send_telegram_message(message)

            await asyncio.sleep(60)

        await browser.close()
