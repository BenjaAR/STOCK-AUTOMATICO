import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------------------------------------------
# Función para verificar si un archivo se descargó correctamente
# ---------------------------------------------------------------------------------------------------
def esperar_descarga(archivo_descargado, tiempo_espera=30):
    """Verifica si un archivo se ha descargado dentro del tiempo de espera dado."""
    tiempo_transcurrido = 0
    while not os.path.exists(archivo_descargado) and tiempo_transcurrido < tiempo_espera:
        time.sleep(1)
        tiempo_transcurrido += 1
    return os.path.exists(archivo_descargado)

# ---------------------------------------------------------------------------------------------------
# Configuración del Navegador (Chrome) y opciones de descarga
# ---------------------------------------------------------------------------------------------------

# Crear objeto de opciones para configurar el navegador Chrome
options = Options()
options.add_argument('--start-maximized')  # Abrir el navegador maximizado
options.add_argument('--disable-extensions')  # Desactivar extensiones de Chrome
options.add_argument('--ignore-certificate-errors')  # Ignorar errores de certificados SSL
options.add_argument('--allow-running-insecure-content')  # Permitir contenido no seguro
options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://192.168.0.56')  # Marcar origen seguro
options.add_argument('--disable-features=InsecureDownloadWarnings')  # Desactivar advertencias de descargas inseguras
options.add_experimental_option("detach", True)  # Mantener la ventana del navegador abierta

# Directorio de descargas (cambiar a la ruta deseada)
download_dir = "/path/to/download"  # Cambiar por el directorio real de descargas
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configuración del directorio de descarga en Chrome
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Directorio de descarga
    "download.prompt_for_download": False,  # No pedir confirmación para las descargas
    "download.directory_upgrade": True,  # Si se cambia el directorio de descarga, actualizar automáticamente
    "safebrowsing.enabled": True  # Habilitar navegación segura
})

# Crear el servicio para ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ---------------------------------------------------------------------------------------------------
# Descarga del Primer Archivo desde el Primer Sitio Web
# ---------------------------------------------------------------------------------------------------

url_1 = "http://192.168.0.56/sareweb2/formulario.php?tabla=VTALRAVE&&menut=10,40,15,00,00&&tipotabla=1"
driver.get(url_1)
time.sleep(3)  # Esperar a que la página cargue
driver.switch_to.frame("sistema")  # Cambiar al frame que contiene el contenido real

# Buscar la imagen de reporte y hacer clic en ella
imagen_reporte = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[img[@src="IMAGES/BOTONES/imprimir.png"]]/img'))
)
imagen_reporte.click()

# Esperar que la ventana emergente esté visible
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="popup-informacion" and @style="display: block;"]'))
)

# Hacer clic en el botón 'GENERAR EXCEL'
boton_excel = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/div/div[10]/div/div[3]/div/table/tbody/tr/td[3]/input'))
)
boton_excel.click()

# Aceptar la alerta de confirmación
WebDriverWait(driver, 10).until(EC.alert_is_present())
alerta = Alert(driver)
alerta.accept()

# Verificar que el primer archivo se haya descargado correctamente
archivo_1 = os.path.join(download_dir, "archivo_1.xlsx")  # Nombre del archivo esperado
if esperar_descarga(archivo_1):
    print("✅ Primer archivo descargado correctamente.")
else:
    print("❌ El primer archivo no se descargó en el tiempo esperado.")

# ---------------------------------------------------------------------------------------------------
# Descarga del Segundo Archivo desde el Segundo Sitio Web
# ---------------------------------------------------------------------------------------------------

url_2 = "http://192.168.0.56/sareweb2/formulario.php?tabla=CSTCSTOC&&menut=10,40,25,00,00&&tipotabla=1"
driver.get(url_2)
time.sleep(3)  # Esperar a que la página cargue
driver.switch_to.frame("sistema")  # Cambiar al frame que contiene el contenido real

# Buscar la imagen de reporte y hacer clic en ella
imagen_reporte = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[img[@src="IMAGES/BOTONES/imprimir.png"]]/img'))
)
imagen_reporte.click()

# Esperar que la ventana emergente esté visible
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="popup-informacion" and @style="display: block;"]'))
)

# Completar el campo "Almacen" con valor 114
almacen_input = driver.find_element(By.ID, "Ficha1[almacen1]")
almacen_input.clear()
almacen_input.send_keys("114")
almacen_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="Ficha1[filtro_cta1]"]/option[2]'))
)
ActionChains(driver).double_click(almacen_option).perform()

# Completar el campo "Division" con valor 183
division_input = driver.find_element(By.ID, "Ficha1[division1]")
division_input.clear()
division_input.send_keys("183")
division_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="Ficha1[filtro_cta1]"]/option[2]'))
)
ActionChains(driver).double_click(division_option).perform()

# Hacer clic en el botón 'GENERAR EXCEL'
boton_excel = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/div/div[10]/div/div[3]/div/table/tbody/tr/td[3]/input'))
)
boton_excel.click()

# Aceptar la alerta de confirmación
WebDriverWait(driver, 20).until(EC.alert_is_present())
alerta = Alert(driver)
alerta.accept()

# Verificar que el segundo archivo se haya descargado correctamente
archivo_2 = os.path.join(download_dir, "archivo_2.xlsx")  # Nombre del archivo esperado
if esperar_descarga(archivo_2):
    print("✅ Segundo archivo descargado correctamente.")
else:
    print("❌ El segundo archivo no se descargó en el tiempo esperado.")

# ---------------------------------------------------------------------------------------------------
# Cerrar el navegador después de las descargas
# ---------------------------------------------------------------------------------------------------
driver.quit()

