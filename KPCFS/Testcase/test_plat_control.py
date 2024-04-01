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

# Navigate to Plat Control
print('Navigate to Plat Control')
OperationTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(OperationTab,'Operation')
OperationTab[Index].click() # Click Operation
time.sleep(1)
PlatControlTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(PlatControlTab,'Plat Control')
PlatControlTab[Index].click() # Click Plat Control
time.sleep(1)

# Input M.BL
CFSWorkingArea=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
Index=Function.find_index_by_attribute(CFSWorkingArea,'value','CFS Working Area')
if Index is not None:
    FieldsMBL=CFSWorkingArea[Index+2]
    FieldsMBL.send_keys(Workspace.M_BL)
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
 ########################################
 print('Select the row:',n)
 start_time = time.time()
 line_element = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
 index_to_add = Function.find_index_by_text(line_element,Workspace.List_Ctnr[n])
 # Collect Data from UI before click
 Conatainer_No= line_element[index_to_add].text
 Sztp= line_element[index_to_add+1].text
 Line.append(line_element[index_to_add])
 Line[n].click()
 time.sleep(1)
 actions = Dictionary.ActionChains(driver)
 actions.double_click(Line[n]).perform()
 time.sleep(1)
 #######################################
 # Caculate Current Date and Future Date then Format them
 current_datetime = datetime.now()
 future_datetime = current_datetime + timedelta(minutes=2)
 formatted_datetime        = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
 formatted_future_datetime = future_datetime.strftime("%Y-%m-%d %H:%M:%S")
 ########################################
 ContainerNoFields= Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
 Index=Function.find_index_by_attribute(ContainerNoFields,'value',Workspace.List_Ctnr[n])
 SealtimeField  = ContainerNoFields[Index+5]
 StarttimeField  = ContainerNoFields[Index+7]
 driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",SealtimeField,formatted_datetime)
 driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", SealtimeField)
 print("Seal Culting Time Container: ",Conatainer_No,"with Sztp:",Sztp,"is :", formatted_datetime) 
 time.sleep(1)
 driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",StarttimeField,formatted_future_datetime)
 driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", StarttimeField)
 print("Start Time Container: ",Conatainer_No,"with Sztp:",Sztp,"is :", formatted_future_datetime) 
 time.sleep(1)
 ########################################
 ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonSave,'Save')
 ButtonSave[Index].click() # Click Save  
 time.sleep(1)
 ########################################
 div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
 Function.find_icon_close_X(driver,div_elements)
 print('Line ',n,"is completed")
 end_time = time.time()
 elapsed_time = end_time - start_time
 print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
 time.sleep(1)
 n += 1
################################
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search again
print("All Container Start to Destuffing")
time.sleep(2)

