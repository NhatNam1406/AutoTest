import sys
sys.path.append(r'C:\Users\nhatn\Downloads\Python\KPCFS-AutoTest\KPCFS\Input')
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

IndexFind    = None 
uploadStatus = None
saveStatus   = None
while IndexFind is None:
    Fields= Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-component-default')))
    for i in range(len(Workspace.stringx)):
        Index=Function.find_index_by_text(Fields,Workspace.stringx[i]) 
        if (Index is not None):
            string=Fields[Index].text
            IndexFind=Index
        else:
            Index=Function.find_index_by_text(Fields,Workspace.stringx[i],partial_match=True)  # Find with partial match
        if(Index is not None):
            string=Fields[Index].text
            IndexFind=Index  
    if uploadStatus == saveStatus == 'Y' and IndexFind is None:
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
          print("Click Icon Close")
        else:
          print("The symbol X can not find")
          time.sleep(1)
        break
    elif IndexFind is not None:
        OKButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        IndexOK=Function.find_index_by_text(OKButton,'OK')
        driver.execute_script("arguments[0].click();",OKButton[IndexOK])
        print('Upload Excel not successfully')
        print(string)
        driver.quit()      
    if IndexFind is None and uploadStatus is None:
        UploadExcelButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index=Function.find_index_by_text(UploadExcelButton,'Upload Excel')
        UploadExcelButton[Index].click() # Click Button
        time.sleep(1)
        file_input = driver.find_element(Dictionary.By.XPATH, "//input[@type='file']").send_keys(Workspace.file_path)
        print("Select Excel File Success")
        time.sleep(1)
        uploadStatus = 'Y'
    elif IndexFind is None and saveStatus is None and uploadStatus == 'Y':
        SaveButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index=Function.find_index_by_text(SaveButton,'Save')
        driver.execute_script("arguments[0].click();",SaveButton[Index])
        print("Click Button Save success")
        time.sleep(1)
        saveStatus = 'Y'


driver.quit()












