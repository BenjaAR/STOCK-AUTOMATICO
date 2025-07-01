import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# =============================
# Función para iniciar el navegador
# =============================
def iniciar_driver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://192.168.0.56')
    options.add_argument('--disable-features=InsecureDownloadWarnings')
    options.add_experimental_option("detach", True)

    # Crear carpeta STOCK en el escritorio
    download_dir = os.path.join(os.path.expanduser('~'), 'Escritorio', 'STOCK')
    os.makedirs(download_dir, exist_ok=True)

    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "download.allow_insecure_downloads": True
    })

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# =============================
# Función principal
# =============================
def main():
    driver = iniciar_driver()
    try:
        # Llamamos la función de descarga en el archivo ranking_ventas
        from ranking_ventas import descargar_ventas
        descargar_ventas(driver)  # Le pasamos el 'driver' al otro archivo
    finally:
        input("Presiona Enter para cerrar el navegador...")
        driver.quit()

if __name__ == "__main__":
    main()
