from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


#############################
# Configuración del navegador
#############################

# Crear un objeto de opciones para configurar el navegador Chrome
options = Options()
# Abrir el navegador maximizado
options.add_argument('--start-maximized')
# Desactivar extensiones de Chrome
options.add_argument('--disable-extensions')
# Ignorar errores de certificados SSL
options.add_argument('--ignore-certificate-errors')
# Permitir contenido no seguro en algunas URLs específicas
options.add_argument('--allow-running-insecure-content')
# Marcar un origen como seguro, aunque no lo sea
options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://192.168.0.56')
# Desactivar advertencias de descargas inseguras
options.add_argument('--disable-features=InsecureDownloadWarnings')
# Mantener la ventana del navegador abierta después de ejecutar el script
options.add_experimental_option("detach", True)

# Configuración del directorio para las descargas
download_dir = "/path/to/download"  # ← Cámbialo por tu ruta real
# Crear el directorio de descargas si no existe
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configurar el navegador para gestionar las descargas automáticamente
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Directorio de descarga
    "download.prompt_for_download": False,  # No pedir confirmación para las descargas
    "download.directory_upgrade": True,  # Si se cambia el directorio de descarga, actualizar automáticamente
    "safebrowsing.enabled": True  # Habilitar la navegación segura
})

# Crear el servicio para ChromeDriver utilizando el manejador automático
service = Service(ChromeDriverManager().install())

# Inicializar el WebDriver con el servicio y las opciones configuradas
driver = webdriver.Chrome(service=service, options=options)



#########################
# Interacciones con la página
#########################

# Abrir la página específica
url = "http://192.168.0.56/sareweb2/formulario.php?tabla=VTALRAVE&&menut=10,40,15,00,00&&tipotabla=1"
driver.get(url)

# Esperamos que la página cargue correctamente
time.sleep(3)  # Espera para asegurar que la página esté completamente cargada

# Cambiar al frame que contiene el contenido real
driver.switch_to.frame("sistema")

# ------------------------------------------------------------
# 1. Buscar el enlace que contiene la imagen y hacer clic
# ------------------------------------------------------------
print("🔍 Buscando la imagen que abrirá la ventana emergente...")

try:
    # Esperar hasta que la imagen con el enlace esté presente en la página
    imagen_reporte = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[img[@src="IMAGES/BOTONES/imprimir.png"]]/img'))
    )

    # Hacer clic en la imagen para abrir la ventana emergente
    imagen_reporte.click()
    print("✅ Clic en la imagen realizado correctamente, ventana emergente abierta.")

    # Esperar hasta que el div de la ventana emergente cambie a display: block;
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="popup-informacion" and @style="display: block;"]'))
    )

    print("✅ Ventana emergente detectada y visibilizada.")

    # ------------------------------------------------------------
    # 2. Buscar el botón 'GENERAR EXCEL' dentro de la ventana emergente y hacer clic
    # ------------------------------------------------------------
    print("🔍 Buscando el botón 'GENERAR EXCEL'...")

    # Esperar hasta que el botón 'GENERAR EXCEL' esté presente y sea clickeable
    boton_excel = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/div/div[10]/div/div[3]/div/table/tbody/tr/td[3]/input'))
    )

    # Hacer clic en el botón 'GENERAR EXCEL'
    boton_excel.click()
    print("✅ Se realizó clic en el botón 'GENERAR EXCEL'.")

    # ------------------------------------------------------------
    # 3. Manejar la ventana emergente de confirmación
    # ------------------------------------------------------------
    print("🔍 Esperando y aceptando la ventana emergente...")

    # Esperar hasta que la alerta sea visible
    WebDriverWait(driver, 10).until(EC.alert_is_present())

    # Cambiar a la alerta y aceptar
    alerta = Alert(driver)  # Aquí se inicializa la alerta correctamente
    alerta.accept()  # Aceptar la alerta
    print("✅ Se aceptó la ventana emergente.")

except Exception as e:
    print(f"❌ Error: {e}")

# Mantener la ventana abierta para inspeccionar el contenido
input("Presiona Enter para cerrar el navegador...")

# Cerrar el navegador
driver.quit()