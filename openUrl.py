import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from urllib.parse import urlparse

# ==============================
# CONFIGURACIÓN
# ==============================

# 🔹 Dominios a excluir (puedes agregar o quitar según necesites)
DOMINIOS_EXCLUIDOS = [
    # Redes sociales
    "facebook.com", "fb.com", "instagram.com", "threads.net",
    "twitter.com", "x.com", "t.co", "linkedin.com",
    "tiktok.com", "snapchat.com", "pinterest.com", "tumblr.com",
    "reddit.com", "discord.com", "discord.gg",
    "whatsapp.com", "telegram.org", "messenger.com",
    "wechat.com", "weibo.com", "line.me", "vk.com",

    # Buscadores
    "google.com", "google.es", "google.co", "googleusercontent.com",
    "bing.com", "yahoo.com", "duckduckgo.com",
    "baidu.com", "ask.com", "aol.com", "yandex.ru",

    # Empresas tecnológicas
    "microsoft.com", "live.com", "office.com", "outlook.com",
    "windows.com", "azure.com", "xbox.com",
    "apple.com", "icloud.com", "mac.com", "me.com",
    "amazon.com", "aws.amazon.com", "primevideo.com", "audible.com",
    "adobe.com", "dropbox.com", "slack.com", "zoom.us",
    "notion.so", "asana.com", "trello.com", "figma.com",
    "canva.com", "spotify.com", "netflix.com", "hbo.com", "disneyplus.com",

    # Navegadores y software
    "mozilla.org", "firefox.com", "chrome.com", "opera.com",
    "brave.com", "safari.com", "edge.com", "vivaldi.com", "torproject.org",

    # Plataformas de video
    "youtube.com", "youtu.be", "vimeo.com", "twitch.tv",
    "dailymotion.com", "rumble.com", "bitchute.com",

    # IA y educación
    "openai.com", "chat.openai.com", "anthropic.com", "claude.ai",
    "perplexity.ai", "deepmind.com", "coursera.org", "edx.org",
    "udemy.com", "khanacademy.org", "wikipedia.org",

    # Bancos y pagos
    "paypal.com", "stripe.com", "squareup.com", "wise.com",
    "revolut.com", "binance.com", "coinbase.com", "mercadopago.com",

    # Publicidad y analítica
    "doubleclick.net", "googletagmanager.com", "google-analytics.com",
    "ads.google.com", "adservice.google.com",
    "meta.com", "pixel.facebook.com", "analytics.yahoo.com"
]

# ==============================
# FUNCIONES PRINCIPALES
# ==============================

def obtener_html(url):
    """Intenta obtener el HTML con requests; si hay contenido dinámico, usa Selenium."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        # Detecta si hay JS
        if "<script" in response.text or "javascript" in response.text.lower():
            print("⚙️ Página con JavaScript detectada, usando Selenium...")
            return obtener_html_selenium(url)
        return response.text
    except Exception as e:
        print(f"⚠️ Error con requests: {e}, intentando con Selenium...")
        return obtener_html_selenium(url)


def obtener_html_selenium(url):
    """Usa Selenium para obtener el HTML renderizado (cuando hay JavaScript)."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html


def es_enlace_valido(url):
    """Verifica que el enlace sea válido y no pertenezca a dominios excluidos."""
    try:
        dominio = urlparse(url).netloc.lower()
        return url.startswith("http") and not any(excluido in dominio for excluido in DOMINIOS_EXCLUIDOS)
    except:
        return False


def extraer_enlaces(url):
    print(f"\n🔍 Analizando: {url}")
    html = obtener_html(url)
    soup = BeautifulSoup(html, "html.parser")

    enlaces = set()
    for a in soup.find_all("a", href=True):
        link = a["href"]
        if es_enlace_valido(link):
            enlaces.add(link)

    print(f"✅ Se encontraron {len(enlaces)} enlaces válidos (sin dominios excluidos).")
    return list(enlaces)


def exportar_excel(enlaces, archivo):
    """Exporta la lista de enlaces a un archivo Excel."""
    df = pd.DataFrame(enlaces, columns=["Enlaces"])
    df.to_excel(archivo, index=False)
    print(f"📁 Enlaces guardados en: {archivo}")


# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================

if __name__ == "__main__":
    print("🌐 EXTRACTOR DE ENLACES CON FILTRO DE DOMINIOS\n")
    URL = input("👉 Ingresa la URL que deseas analizar: ").strip()

    if not URL.startswith("http"):
        URL = "https://" + URL

    enlaces = extraer_enlaces(URL)
    if enlaces:
        exportar_excel(enlaces, "enlaces_extraidos.xlsx")
    else:
        print("⚠️ No se encontraron enlaces válidos.")
