import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_driver():
    """Inicializa Selenium con configuración sin interfaz (headless)."""
    opciones = Options()
    opciones.add_argument("--headless=new")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--log-level=3")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opciones)


def obtener_html(url, driver):
    """Obtiene el HTML ya renderizado con JS usando Selenium."""
    try:
        driver.get(url)
        time.sleep(2)
        return driver.page_source
    except Exception as e:
        print(f"❌ Error al cargar {url}: {e}")
        return None


def extraer_enlaces(url_inicial):
    """Extrae todos los enlaces únicos por dominio raíz."""
    driver = iniciar_driver()
    enlaces_visitados = set()
    dominios_guardados = set()
    paginas_por_visitar = [url_inicial]

    while paginas_por_visitar:
        pagina_actual = paginas_por_visitar.pop(0)
        print(f"🔎 Visitando: {pagina_actual}")

        try:
            html = obtener_html(pagina_actual, driver)
            if not html:
                resp = requests.get(pagina_actual, timeout=10)
                html = resp.text if resp.status_code == 200 else None
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")

            for a in soup.find_all("a", href=True):
                link = urljoin(pagina_actual, a["href"])
                dominio = urlparse(link).netloc  # ejemplo: "www.co.delaware.in.us"

                # ✅ solo guardar el primer enlace de cada dominio raíz
                if dominio and dominio not in dominios_guardados:
                    dominios_guardados.add(dominio)
                    enlaces_visitados.add(link)
                    print(f"  ➜ Guardado (nuevo dominio): {link}")

                    # Detectar posibles enlaces de paginación
                    if "page" in link or "p=" in link or link.endswith(tuple("0123456789")):
                        paginas_por_visitar.append(link)

            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Error procesando {pagina_actual}: {e}")

    driver.quit()
    return enlaces_visitados


if __name__ == "__main__":
    url_inicial = input("🌐 Ingresa la URL inicial: ").strip()
    todos_los_enlaces = extraer_enlaces(url_inicial)

    # --- Guardar resultados en Excel ---
    df = pd.DataFrame(list(todos_los_enlaces), columns=["Enlaces únicos por dominio raíz"])
    nombre_excel = "enlaces_unicos.xlsx"
    df.to_excel(nombre_excel, index=False)

    print(f"\n✅ Total de dominios únicos encontrados: {len(todos_los_enlaces)}")
    print(f"📊 Archivo Excel generado: {nombre_excel}")
