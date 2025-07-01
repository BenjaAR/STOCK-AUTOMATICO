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


# Configuración del navegador
options = Options()
options.add_argument('--start-maximized')  # Iniciar el navegador en pantalla completa
options.add_argument('--disable-extensions')  # Desactivar extensiones del navegador
options.add_experimental_option("detach", True)  # Mantener el navegador abierto

# Configuración para permitir descargas sin bloqueos
download_dir = "/path/to/download"  # Cambia esto por el directorio de descarga deseado
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Directorio de descarga
    "download.prompt_for_download": False,  # No preguntar por cada descarga
    "download.directory_upgrade": True,  # Permite que se actualice la carpeta de descargas
    "safebrowsing.enabled": False,  # Desactivar el filtro de navegación segura
    "download.allow_insecure_downloads": True  # Permitir descargas inseguras
})


# Crear el servicio para ChromeDriver
service = webdriver.chrome.service.Service(ChromeDriverManager().install())

# Inicializar el WebDriver con el servicio y las opciones
driver = webdriver.Chrome(service=service, options=options)

#################################################################
# AUTOMATIZACIÓN
#################################################################

# Abrir la página específica
url = "http://192.168.0.56/sareweb2/formulario.php?tabla=CSTCSTOC&&menut=10,40,25,00,00&&tipotabla=1"
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
    print("✅ Imagen de reporte encontrada, haciendo clic...")
    # Hacer clic en la imagen para abrir la ventana emergente
    imagen_reporte.click()
    print("✅ Clic en la imagen realizado correctamente, ventana emergente abierta.")

    # Esperar hasta que el div de la ventana emergente cambie a display: block;
    print("🔍 Esperando a que la ventana emergente se haga visible...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="popup-informacion" and @style="display: block;"]'))
    )
    print("✅ Ventana emergente detectada y visibilizada.")

    # ------------------------------------------------------------
    # 2. Completar el campo "Almacen" con valor 114 y seleccionar la opción
    # ------------------------------------------------------------
    print("🔍 Completando el campo 'Almacen'...")

    # Llenar el campo "Almacen" con valor 114
    almacen_input = driver.find_element(By.ID, "Ficha1[almacen1]")
    almacen_input.clear()  # Limpiar el campo
    almacen_input.send_keys("114")  # Ingresar el valor 114
    print("✅ Campo 'Almacen' completado con el valor 114.")

    # Esperar a que se muestre el dropdown
    time.sleep(1)

    # Doble clic sobre la opción "114" para seleccionarla
    almacen_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="Ficha1[filtro_cta1]"]/option[2]'))
    )
    ActionChains(driver).double_click(almacen_option).perform()
    print("✅ Opción '114' seleccionada mediante doble clic.")

    # Esperar un momento para asegurarse de que el select se cierre
    time.sleep(1)

    # Verificar si el dropdown se cerró
    select_visible = driver.find_elements(By.NAME, "Ficha1[filtro_cta1]")
    if not select_visible or not select_visible[0].is_displayed():
        print("✅ El select de 'almacen' se cerró correctamente.")
    else:
        print("⚠️ El select de 'almacen' aún está visible.")

    # ------------------------------------------------------------
    # 3. Completar el campo "Division" con valor 185 y seleccionar la opción
    # ------------------------------------------------------------
    print("🔍 Completando el campo 'Division'...")

    # Llenar el campo "Division" con valor 185
    division_input = driver.find_element(By.ID, "Ficha1[division1]")
    division_input.clear()  # Limpiar el campo
    division_input.send_keys("185")  # Ingresar el valor 185
    print("✅ Campo 'Division' completado con el valor 185.")

    # Esperar a que se muestre el dropdown
    time.sleep(1)

    # Doble clic sobre la opción "185" para seleccionarla
    division_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="Ficha1[filtro_cta1]"]/option[2]'))
    )
    ActionChains(driver).double_click(division_option).perform()
    print("✅ Opción '185' seleccionada mediante doble clic.")

    # Esperar un momento para asegurarse de que el select se cierre
    time.sleep(1)

    # Verificar si el dropdown de 'Division' se cerró
    select_visible = driver.find_elements(By.NAME, "Ficha1[filtro_cta1]")
    if not select_visible or not select_visible[0].is_displayed():
        print("✅ El select de 'division' se cerró correctamente.")
    else:
        print("⚠️ El select de 'division' aún está visible.")

    # ------------------------------------------------------------
    # 4. Buscar el botón 'GENERAR EXCEL' dentro de la ventana emergente y hacer clic
    # ------------------------------------------------------------
    print("🔍 Buscando el botón 'GENERAR EXCEL'...")

    # Esperar hasta que el botón 'GENERAR EXCEL' esté presente y sea clickeable
    boton_excel = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/div/div[10]/div/div[3]/div/table/tbody/tr/td[3]/input'))
    )
    print("✅ Botón 'GENERAR EXCEL' encontrado, haciendo clic...")

    # Hacer clic en el botón 'GENERAR EXCEL'
    boton_excel.click()

    # ------------------------------------------------------------
    # 5. Manejar la ventana emergente de confirmación
    # ------------------------------------------------------------
    print("🔍 Esperando la alerta de confirmación...")

    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # Esperamos la alerta de confirmación
        print("✅ Alerta de confirmación encontrada.")
        
        alerta = Alert(driver)
        alerta.accept()  # Aceptamos la alerta
        print("✅ Alerta de confirmación aceptada.")
        
    except Exception as e:
        print("❌ No se detectó la alerta de confirmación o hubo un error:", e)

    # ------------------------------------------------------------
    # 6. Esperar que la descarga se complete
    # ------------------------------------------------------------
    print("🔍 Esperando que la descarga se complete...")
    time.sleep(10)  # Ajusta este tiempo según la velocidad de descarga

except Exception as e:
    print(f"❌ Error: {e}")

# Mantener la ventana abierta para inspeccionar el contenido
input("Presiona Enter para cerrar el navegador...")

# Cerrar el navegador
driver.quit()
