import asyncio
import random
import json
from datetime import datetime
from playwright.async_api import async_playwright

# --- 1. İNSANSI HAREKETLER ---
async def insansi_hareket_yap(page):
    try:
        for _ in range(random.randint(3, 6)):
            x, y = random.randint(50, 800), random.randint(50, 800)
            await page.mouse.move(x, y, steps=random.randint(15, 30))
            await asyncio.sleep(random.uniform(0.1, 0.4))
        if random.random() < 0.2:
            await page.mouse.wheel(0, -300) 
            await asyncio.sleep(random.uniform(0.5, 1.2))
    except:
        pass

# --- 2. ANA BOT MOTORU ---
async def hayalet_gorev_baslat(account_data, target_username):
    rapor_verisi = []
    async with async_playwright() as p:
        print("🚀 Kodcum Ajans - Hayalet Motor v2.0 Başlatıldı...")
        
        browser = await p.chromium.launch(
            headless=True,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--single-process",
                "--no-zygote"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        await context.set_extra_http_headers({
            "Authorization": account_data['bearer'],
            "x-csrf-token": account_data['csrf']
        })

        page = await context.new_page()

        try:
            print("🏠 X Ana sayfasına uğranıyor...")
            await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(random.uniform(4.0, 7.0))
            
            print(f"🕵️ Hedef: {target_username} profiline sızılıyor...")
            await page.goto(f"https://x.com/{target_username}", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(random.uniform(2.0, 4.0))
        except Exception as e:
            print(f"❌ Erişim Hatası: {e}")
            await browser.close()
            return

        tweet_sayaci = 0
        while tweet_sayaci < 10:
            articles = await page.query_selector_all('article')
            
            for article in articles:
                if tweet_sayaci >= 10: break
                
                # Hata veren kısım burasıydı, tek satıra çekildi:
                is_ads = await article.query_selector('text="Promoted"') or await article.query_selector('text="Sponsorlu"')
                
                if is_ads:
                    durma_suresi = round(random.uniform(3.15, 7.45), 2)
                    print(f"📢 [REKLAM] Yakalandı! {durma_suresi} sn etkileşim yapılıyor...")
                    
                    parca = durma_suresi / 3
                    for _ in range(3):
                        await insansi_hareket_yap(page)
                        await asyncio.sleep(parca)
                    
                    tweet_sayaci += 1
                    rapor_verisi.append({
                        "id": tweet_sayaci,
                        "hedef": target_username,
                        "sure": durma_suresi,
                        "zaman": datetime.now().strftime("%H:%M:%S")
                    })
                    print(f"✅ Başarılı: {tweet_sayaci}/10")

            scroll_mesafesi = random.randint(1000, 1500)
            await page.mouse.wheel(0, scroll_mesafesi)
            print(f"📜 {scroll_mesafesi} birim aşağı inildi...")
            await asyncio.sleep(random.uniform(2.5, 4.5))

        with open("gorev_raporu.json", "w", encoding="utf-8") as f:
            json.dump(rapor_verisi, f, ensure_ascii=False, indent=4)
        
        print("🎯 Görev Tamam! Rapor 'gorev_raporu.json' dosyasına yazıldı.")
        await browser.close()

# --- ÇALIŞTIRMA ---
if __name__ == "__main__":
    test_hesap = {
        "bearer": "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA", 
        "csrf": "2b3fa664a6e969152aa7387eea4e25d74022a974a09ffc24fed4581f11ee9958cd4fcc2f423c6756eedef7da5f5853eb40ef07dcf0c768c4f5c91ceb51e58910d4db8aefba9a29be1f87b3f530cdb0ec"
    }
    asyncio.run(hayalet_gorev_baslat(test_hesap, "microp0099"))
# Botun sonuna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
report_full_path = os.path.join(parent_dir, "gorev_raporu.json")

with open(report_full_path, "w", encoding="utf-8") as f:
    json.dump(rapor_verisi, f, ensure_ascii=False, indent=4)
import os
if os.path.exists("bot.lock"):
    os.remove("bot.lock")
    print("Sistem kilidi kaldırıldı, yeni görevlere hazır.")
