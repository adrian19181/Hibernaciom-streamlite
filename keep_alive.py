import asyncio
from playwright.async_api import async_playwright

# Enlaces directos a tus 8 aplicaciones de Streamlit
APPS = [
    "https://ahorro-programado-jardin-2025-2026-lpkqxauhd6ubq2tdwgm8up.streamlit.app/",
    "https://ahorro-programado-jardin-2026---2027-jvgnnbjed5rrmeprxhrf4k.streamlit.app/",
    "https://calculadorasueldo-658v3aazzcta5b5x6gk2mk.streamlit.app/",
    "https://comparacion-ahorros-programados-mjaaaegmw4wzwlupfcohxe.streamlit.app/",
    "https://pago-tarjetas-8ygjpcq3wus8pxf7g7arzr.streamlit.app/",
    "https://programado-jardin-2024-2025-h86a7ezvhkp2w6lthjp9k9.streamlit.app/",
    "https://sueldo-a49pjsdwr5bjzgzhn6zxqm.streamlit.app/",
    "https://tarjetas-de-credito-final-anufhdcyb3bpawg5guslrs.streamlit.app/"
]

async def despertar_apps():
    async with async_playwright() as p:
        # Se abre un navegador Chromium en modo invisible
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for i, url in enumerate(APPS):
            try:
                print(f"Visitando: {url}")
                await page.goto(url, timeout=60000)
                await page.wait_for_timeout(5000) # 5 segundos para que la página cargue
                
                # Busca exactamente el botón azul de hibernación de Streamlit
                boton_despertar = page.locator("button:has-text('Yes, get this app back up!')")
                
                if await boton_despertar.is_visible():
                    print(f"App dormida detectada en {url}. Despertando...")
                    await boton_despertar.click()
                    await page.wait_for_timeout(15000) # 15 segundos para que el servidor de Streamlit reinicie
                    print("App reactivada con éxito.")
                else:
                    print("La app ya estaba activa.")
                    
            except Exception as e:
                print(f"Error al procesar {url}: {e}")
            
            # Espaciado de 5 minutos (300 segundos) entre aplicaciones
            # La condición evita que espere 5 minutos innecesarios después de la última app
            if i < len(APPS) - 1:
                print("Esperando 5 minutos (300 segundos) antes de la siguiente app...")
                await asyncio.sleep(300)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(despertar_apps())