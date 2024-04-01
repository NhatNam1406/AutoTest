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
if login_button is not None:
    login_element = driver.find_element(Dictionary.By.XPATH, ".//span[text()='Login']").click()
    print('Log in successfully')
else:
    print("Login button not found")
time.sleep(2)

# Navigate to Import Work Order
print('Navigate to Import Work Order')
ImportTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportTab,'Import')
ImportTab[Index].click() # Click Import
time.sleep(1)
ImportWorkOrderTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportWorkOrderTab,'Import Work Order')
ImportWorkOrderTab[Index].click() # Click Import Work Order
time.sleep(1)

# Find the Fields text MBL to input
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find('input', attrs={'role': 'combobox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-empty-field-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'combo-1186-ariaStatusEl'})
if textbox_input_fields is not None:
    ID_MBL = textbox_input_fields.get('id')
    driver.find_element(Dictionary.By.ID,ID_MBL).send_keys(Workspace.M_BL)
else:
    print("Can not find the fields to input MBL")
# Click Search
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(1)
print('Search Work No Complete')
# Select the line
Line=[]
n=0
for n in range(len(Workspace.M_BL_list)):
 start_time = time.time()
 #######################################
 print('Select the row:',n)
 start_time = time.time()
 line_element = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
 index_to_add = Function.find_index_by_text(line_element,Workspace.M_BL_list[n])
 Line.append(line_element[index_to_add])
 Line[n].click()
 time.sleep(1) 
 actions = Dictionary.ActionChains(driver)
 actions.double_click(Line[n]).perform()
 #######################################
 Fields=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
 Workno=Fields[51].get_attribute('value')
 Workdate=Fields[53].get_attribute('value')
 Workcode=Fields[55].get_attribute('value')
 Status=Fields[54]
 driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",Status,'Approved')
 driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Status)
 Status=Fields[54].get_attribute('value')
 print("Work no:",Workno,"get approval")
 print("Work code:",Workcode)
 print("Expect Work Date:",Workdate)
 #######################################
 time.sleep(1)
 ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonSave,'Save')
 driver.execute_script("arguments[0].click();", ButtonSave[Index]) 
 #######################################
 time.sleep(1)
 div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
 Function.find_icon_close_X(driver,div_elements)
 ##########################################
 end_time = time.time()
 elapsed_time = end_time - start_time
 print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
 n += 1
time.sleep(1)
driver.quit()
print('Close Window')








