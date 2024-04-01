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

# Navigate to Gate Control
print('Navigate to Gate Control')
OperationTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(OperationTab,'Operation')
OperationTab[Index].click() # Click Operation
time.sleep(1)
GateControlTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(GateControlTab,'Gate Control')
GateControlTab[Index].click() # Click Gate Control
time.sleep(1)
# Delete Search Time
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields   = soup.find('input', attrs={'role': 'combobox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-field x-form-text x-form-text-default', 'tabindex': '1', 'title': 'Expected date format Y-m-d.', 'aria-describedby': 'datefield-1157-ariaStatusEl datefield-1157-ariaHelpEl'})
textbox_input_fields_1 = soup.find('input', attrs={'role': 'combobox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-field x-form-text x-form-text-default', 'tabindex': '1', 'title': 'Expected date format Y-m-d.', 'aria-describedby': 'datefield-1158-ariaStatusEl datefield-1158-ariaHelpEl'})
if (textbox_input_fields is not None) and (textbox_input_fields_1 is not None):
    ID_GID = textbox_input_fields.get('id')
    ID_GOD = textbox_input_fields_1.get('id')
    Indate=driver.find_element(Dictionary.By.ID,ID_GID)
    Outdate=driver.find_element(Dictionary.By.ID,ID_GOD)
    Indate.send_keys(Dictionary.Keys.CONTROL + "a", Dictionary.Keys.DELETE)
    Outdate.send_keys(Dictionary.Keys.CONTROL + "a", Dictionary.Keys.DELETE)
    print('Clear Time Successfully')
else:
    print("Can not find the fields to delete the Gate In or Gate Out Date")
time.sleep(1)
# Input M.BL
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find('input', attrs={'role': 'textbox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-field x-form-text x-form-text-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'textfield-1161-ariaStatusEl'})
if textbox_input_fields is not None:
    ID_MBL = textbox_input_fields.get('id')
    driver.find_element(Dictionary.By.ID,ID_MBL).send_keys(Workspace.M_BL)
    print('Input M.BL Complete')
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
for n in range(len(Workspace.List_Ctnr)):
 #######################################
 print('Select the row:',n)
 start_time = time.time()
 line_element = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
 index_to_add = Function.find_index_by_text(line_element,Workspace.List_Ctnr[n])
 # Collect Data from UI before click
 Container_no=line_element[index_to_add].text 
 Sztp=line_element[index_to_add+3].text
 Payer=line_element[index_to_add+5].text
 Work_code=line_element[index_to_add+7].text
 Work_no=line_element[index_to_add+18].text
 Line.append(line_element[index_to_add])
 Line[n].click()
 time.sleep(1) 
 actions = Dictionary.ActionChains(driver)
 actions.double_click(Line[n]).perform()
 time.sleep(1)
 #######################################
 current_datetime = datetime.now()
 formatted_datetime        = current_datetime.strftime("%Y-%m-%d %H:%M")
 page_source = driver.page_source
 soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
 textbox_input_fields = soup.find('input', attrs={'role': 'combobox', 'title': 'Expected date format Y-m-d H:i.'})
 if (textbox_input_fields is not None):
    ID_GID = textbox_input_fields.get('id')
    ContainerIndate=driver.find_element(Dictionary.By.ID,ID_GID)
    driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",ContainerIndate,formatted_datetime)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", ContainerIndate)
 else:
    print("Can not find the fields to input the Gate In Date")
 time.sleep(1)
 ########################################
 PlatForm=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
 Index=Function.find_index_by_attribute(PlatForm,'value','C')
 if (Index is not None):
    Position=Dictionary.random.choice(Workspace.LOC_CD)
    Platno=PlatForm[Index+2]
    driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",Platno,Position)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Platno)
 else:
    print("Can not find the fields to input the Plat No")
 time.sleep(1)
 ########################################
 ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonSave,'Save')
 ButtonSave[Index].click() # Click Save   
 print("The Container No:",Container_no,"gate in at",formatted_datetime,"at platform",Position)
 print("Sztp:",Sztp,"Payer:",Payer,"Work Code:",Work_code,"Work No:",Work_no)
 time.sleep(1)
 ########################################
 div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
 Function.find_icon_close_X(driver,div_elements)
 end_time = time.time()
 elapsed_time = end_time - start_time
 print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
 n += 1
print('All Container has been Gate In')
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(2)

