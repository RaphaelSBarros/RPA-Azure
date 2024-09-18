import sys
sys.path.insert(0, "c:/Users/P927/OneDrive/Área de Trabalho/RPA - Azure")

from module import *

queries={
  "alianza": r"https://dev.azure.com/LatamFabricaDeSoftware/Alianza/_queries/query/d4ad2c44-446d-4dac-a7ca-b3f1e7f457f8/",
  "checkbuy_brasil": r"https://dev.azure.com/LatamFabricaDeSoftware/Checkbuy%20Brasil/_queries/query/3690bf2e-a83d-4e00-917a-d2b926b5c735/",
  "datasul_dimensional": r"https://dev.azure.com/LatamFabricaDeSoftware/Datasul_Dimensional/_queries/query/06328401-00e1-45af-a0f9-f6b190b61940/",
  "datasul_nortel": r"https://dev.azure.com/LatamFabricaDeSoftware/Datasul_Nortel/_queries/query/3252191f-e5f3-4300-93f0-5ac0d319d87e/",
  "portal_compras": r"https://dev.azure.com/LatamFabricaDeSoftware/Portal%20de%20Compras/_queries/query/ca53158f-1dc7-4e1a-b211-11a5e5c03d07/",
  "sphere_nortel": r"https://dev.azure.com/LatamFabricaDeSoftware/Sphere%20-%20Nortel/_queries/query/a2e1fa31-407a-4943-b9eb-8e75ac493dc2/",
}

def open_browser():
  user = os.getlogin()
  options = webdriver.ChromeOptions()
  options.add_argument(f"--user-data-dir=C:/Users/{user}/AppData/Local/Google/Chrome/Bot Data")
  options.add_argument(r'--profile-directory=Default')
  driver = webdriver.Chrome(options=options)
  driver.get('https://dev.azure.com/LatamFabricaDeSoftware')
  return driver

def send_info(driver, xpath, keys):
  try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.send_keys(keys)
  except:
    return True
  
def click_button(driver, xpath):
  try:
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()
  except:
    return "Não foi possível clicar no botão"
  
def start_download_process(driver):
  c = input('Fazer login antes de continuar')
  for client, query in queries.items():
    driver.get(query)
    time.sleep(3)
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')
    
    click_button(driver, "//button[@aria-label='More actions']")
    c=0
    while c < 5:
      try:
        x, y = pyautogui.locateCenterOnScreen(f'images/download_button.png')
        pyautogui.click(x, y)
      except pyautogui.ImageNotFoundException:
        print('Elemento não encontrado na tela.')
        c+=1
      except:
        print("Deu outro erro")
      else:
        break
  time.sleep(5)
  driver.quit()
  
driver = open_browser()
start_download_process(driver)