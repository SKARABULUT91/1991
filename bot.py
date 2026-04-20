import asyncio
import random
from playwright.async_api import async_playwright

# --- AYARLAR ---
TARGET_URL = "https://x.com/ahmet_kullanici_adi" # Ahmet'in profil linki
WAIT_SESSIONS = [3, 4, 2, 6, 5] # Senin istediğin bekleme saniyeleri

async def insansi_hareket(page):
    """Mouse titretme ve klavye etkileşimi simülasyonu"""
    # Mouse'u rastgele küçük piksellerde titret
    for _ in range(random.randint(2, 5)):
        x, y = random.randint(100, 200), random.randint(100, 200)
        await page.mouse.move(x, y, steps=10)
        await asyncio.sleep(random.uniform(0.1, 0.4))
    
    # Klavye ile sayfayı hafif oynat (İnsan okuma taklidi)
    if random.choice([True, False]):
        await page.keyboard.press("ArrowDown")
        await asyncio.sleep(0.1)
        await page.keyboard.press("ArrowUp")

async def hayalet_bot_baslat(account_data):
    async with async_playwright() as p:
        # Tarayıcıyı başlat (headless=False yaparak ne yaptığını izleyebilirsin)
        browser = await p.chromium.launch(headless=False) 
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        )

        # Dashboard'dan gelen Premium Header'ları enjekte et
        await context.set_extra_http_headers({
            "Authorization": account_data['bearer'],
            "x-csrf-token": account_data['csrf']
        })

        # Çerezleri (Cookies) ekle (Eğer dashboard'dan json geliyorsa)
        # await context.add_cookies(account_data['cookies'])

        page = await context.new_page()
        await page.goto(TARGET_URL)
        print(f"🚀 {TARGET_URL} adresine giriş yapıldı.")

        tweet_sayaci = 0
        while tweet_sayaci < 10:
            # Sayfadaki içerikleri (Tweet/Reklam) bul
            articles = await page.query_selector_all('article')
            
            for article in articles:
                if tweet_sayaci >= 10: break
                
                # Reklam tespiti (Promoted/Sponsorlu)
                is_ads = await article.query_selector('text="Promoted"') or \
                         await article.query_selector('text="Sponsorlu"')
                
                if is_ads:
                    # Reklamın üzerine kaydır
                    await article.scroll_into_view_if_needed()
                    
                    # Belirlediğin saniyelerden birini rastgele seç
                    durma_suresi = random.choice(WAIT_SESSIONS)
                    print(f"📢 Reklam yakalandı! {durma_suresi} saniye 'insan' gibi inceleniyor...")
                    
                    # Bekleme esnasında titretme yap
                    for _ in range(durma_suresi):
                        await insansi_hareket(page)
                        await asyncio.sleep(1)
                    
                    tweet_sayaci += 1
                    print(f"✅ Etkileşim Tamamlandı: {tweet_sayaci}/10")
                
            # Yeni içerikler için aşağı kaydır
            await page.mouse.wheel(0, 700)
            await asyncio.sleep(2)

        print("🎯 Görev başarıyla tamamlandı. Tarayıcı kapatılıyor.")
        await browser.close()

# --- ÇALIŞTIRMA ---
# Bu veriler normalde Perfect Project Craft dashboard'undan gelecek
test_data = {
    "bearer": "AAAAA... (Parser'dan gelen)",
    "csrf": "ct0_degeri... (Parser'dan gelen)"
}

if __name__ == "__main__":
    asyncio.run(hayalet_bot_baslat(test_data))
