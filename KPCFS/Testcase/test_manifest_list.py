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
if login_button is not None:
    login_element = driver.find_element(Dictionary.By.XPATH, ".//span[text()='Login']").click()
    print('Log in successfully')
else:
    print("Login button not found")
time.sleep(2)

# Navigate to Manifest List
print('Navigate to Manifest List')
ImportTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportTab,'Import')
ImportTab[Index].click() # Click Import
time.sleep(1)
ManifestListTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ManifestListTab,'Manifest List')
ManifestListTab[Index].click() # Click Manifest List
time.sleep(1)
# Find the Fields text MBL to input
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find('input', attrs={'role': 'textbox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-field x-form-text x-form-text-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'textfield-1159-ariaStatusEl'})
if textbox_input_fields is not None:
    ID_MBL = textbox_input_fields.get('id')
    driver.find_element(Dictionary.By.ID,ID_MBL).send_keys(Workspace.M_BL)
else:
    print("Can not find the fields to input MBL")
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(1)
# Select each line one by one
Line=[]
n=0
for n in range(len(Workspace.H_BL)):
 #######################################
 print('Select the row:',n)
 start_time = time.time()
 line_element = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
 index_to_add = Function.find_index_by_text(line_element,Workspace.H_BL[n])
 Line.append(line_element[index_to_add])
 Line[n].click()
 time.sleep(1) 
 actions = Dictionary.ActionChains(driver)
 actions.double_click(Line[n]).perform()
 #######################################
 Fields= Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
 HBL=Fields[38].get_attribute('value')
 MasterBL=Fields[39].get_attribute('value')
 POL=Fields[41].get_attribute('value')
 POD=Fields[44].get_attribute('value')
 FDEST=Fields[47].get_attribute('value')
 FWD=Fields[50].get_attribute('value')
 CSN=Fields[56].get_attribute('value')
 Payer=Fields[59].get_attribute('value')
 Qty=Fields[62].get_attribute('value')
 PCKG=Fields[63].get_attribute('value')
 WGT=Fields[67].get_attribute('value')
 CBM=Fields[71].get_attribute('value')
 DESC=Fields[72].get_attribute('value')
 Cargotype=Fields[73].get_attribute('value')
 Cargocode=Fields[76].get_attribute('value')
 Casemark=Fields[84].get_attribute('value')
 print("HBL:",HBL,'|',"M.BL:",MasterBL,'|',"POL:",POL,'|',"POD:",POD,'|',"FDEST:",FDEST,'|',"Request Agent:",FWD,'|',"Consignee:",CSN,'|',"Payer:",Payer)
 print("Qty:",Qty,PCKG,'|',"Weight:",WGT,'|',"CBM:",CBM,'|',"Cargo Code:",Cargocode,Cargotype)
 print("Good desc:",DESC)
 print("Case mark:",Casemark)
 #######################################
 time.sleep(1)
 div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
 Function.find_icon_close_X(driver,div_elements)
 ########################################
 time.sleep(1)
 ButtonOK=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonOK,'OK')
 driver.execute_script("arguments[0].click();", ButtonOK[Index])  #Click OK
 end_time = time.time()
 elapsed_time = end_time - start_time
 print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
 n += 1

SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click() 
print('Back to Manifest List')
time.sleep(1)
driver.quit()
print('Close Window')













