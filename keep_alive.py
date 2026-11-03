import asyncio
from playwright.async_api import async_playwright

APPS = [
    "https://ahorro-programado-jardin-2025-2026-lpkqxauhd6ubq2tdwgm8up.streamlit.app/",
    "https://ahorro-programado-jardin-2026---2027-jvgnnbjed5rrmeprxhrf4k.streamlit.app/",
    "https://movimientos-bancos-r7znoyvpfp8p9cvjevfptx.streamlit.app/",
    "https://calculadorasueldo-658v3aazzcta5b5x6gk2mk.streamlit.app/",
    "https://calificacion-de-riesgo-ubczu6cszzgwdqpcfmcjv8.streamlit.app/",
    "https://comparacion-ahorros-programados-mjaaaegmw4wzwlupfcohxe.streamlit.app/",
    "https://inversiones-hwebbwqbakg4khbdvsq7qz.streamlit.app/",
    "https://mejor-inversion-ranta-fija-xuju9buunvtqxryohgerwe.streamlit.app/",
    "https://pago-tarjetas-8ygjpcq3wus8pxf7g7arzr.streamlit.app/",
    "https://programado-jardin-2024-2025-h86a7ezvhkp2w6lthjp9k9.streamlit.app/",
    "https://sueldo-a49pjsdwr5bjzgzhn6zxqm.streamlit.app/",
    "https://tablas-pasivas-bancos-y-cooperativas-final-tqgmpqzn2wdbdlelsqx.streamlit.app/",
    "https://tarjetas-de-credito-final-anufhdcyb3bpawg5guslrs.streamlit.app/"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

async def procesar_app(context, url):
    page = await context.new_page()
    try:
        print(f"Visitando: {url}")
        await page.goto(url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        
        # Selector insensible a mayúsculas/minúsculas para capturar cualquier variación del botón
        boton_despertar = page.locator("button:has-text('get this app back up'), button:has-text('Yes, get this app back up!')")
        
        if await boton_despertar.count() > 0 and await boton_despertar.first.is_visible():
            print(f"⚡ App dormida detectada en {url}. Despertando...")
            await boton_despertar.first.click()
            await page.wait_for_timeout(10000)
            print(f"✅ App reactivada: {url}")
        else:
            print(f"🟢 App ya activa: {url}")
            
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
    finally:
        await page.close()

async def despertar_apps():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(user_agent=USER_AGENT)
        
        # Procesa hasta 3 apps simultáneamente para evitar bloqueos y acelerar la ejecución
        semaphore = asyncio.Semaphore(3)

        async def sem_task(url):
            async with semaphore:
                await procesar_app(context, url)

        await asyncio.gather(*(sem_task(url) for url in APPS))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(despertar_apps())