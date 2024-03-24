import sys
sys.path.append(r'C:\Users\TSB\Downloads\AutoTest\KPCFS\Input')
import Function
import Dictionary
import Workspace
import os
import time
from datetime import datetime, timedelta

####################### SET UP FOR WEB DRIVER #######################
driver = Dictionary.webdriver.Chrome()
#####################################################################

################################ WORK FLOW ####################################
# Open a website
driver.maximize_window()
driver.get('http://localhost:8080/cfs/html/index.html')
time.sleep(2)

# Log in
id=Workspace.UserID
password=Workspace.Passpord
## Find input Text
Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_element_located((Dictionary.By.TAG_NAME, "input")))
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find_all('input', attrs={'role': 'textbox'})
for field in textbox_input_fields:
    if field.get('name') == 'userid':
        driver.find_element(Dictionary.By.NAME, field.get('name')).send_keys(id)
    elif field.get('name') == 'password':
        driver.find_element(Dictionary.By.NAME, field.get('name')).send_keys(password)
## Find the Login Button
login_button = soup.find('span', string='Login')
if login_button:
    login_element = driver.find_element(Dictionary.By.XPATH, ".//span[text()='Login']").click()
    print('Log in successfully')
else:
    print("Login button not found")
time.sleep(2)

# Navigate to Manifest List
ImportTab=Dictionary.WebDriverWait(driver, 50).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportTab,'Import')
ImportTab[Index].click() # Click Import
time.sleep(1)
ManifestListTab=Dictionary.WebDriverWait(driver, 50).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ManifestListTab,'Manifest List')
ManifestListTab[Index].click() # Click Manifest List
time.sleep(1)

# Upload Excel File
UploadExcelButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(UploadExcelButton,'Upload Excel')
UploadExcelButton[Index].click() # Click Button
time.sleep(1)
file_input = driver.find_element(Dictionary.By.XPATH, "//input[@type='file']").send_keys(Workspace.file_path)
time.sleep(1)

SaveButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SaveButton,'Save')
SaveButton[Index].click() # Click Save
time.sleep(1)

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
print('Upload Excel successfully')
print("Document upload at:",formatted_datetime)
time.sleep(1)

page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
close_button = soup.find('div', class_='x-tool-tool-el x-tool-img x-tool-close', role='presentation')
if close_button is not None:
    button_id = close_button.get('id')
    SymbolX=driver.find_element(Dictionary.By.ID, button_id)
    driver.execute_script("arguments[0].click();",SymbolX)
else:
    print("The symbol X can not find")
time.sleep(1)
driver.quit()












