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

# Navigate to Destuffing Operation
print('Navigate to Destuffing Operation')
ImportTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportTab,'Import')
ImportTab[Index].click() # Click Import
time.sleep(1)
DestuffingOperationTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(DestuffingOperationTab,'Destuffing Operation')
DestuffingOperationTab[Index].click() # Click Manifest List
time.sleep(1)

# Input M.BL and Job Status as ALL
JobStatus=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
Index=Function.find_index_by_attribute(JobStatus,'value','Preadvice')
JobStatusFields=JobStatus[Index].send_keys(Dictionary.Keys.CONTROL + "a", Dictionary.Keys.DELETE)
driver.execute_script("arguments[0].value='All';",JobStatus[Index])
MBLFields=JobStatus[Index+1]
driver.execute_script("arguments[0].value=arguments[1];",MBLFields,Workspace.M_BL)
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(1)
# Select each line one by one
Line=[]
n=0
for n in range(len(Workspace.H_BL)):
   ###################################
   print('Start to select line:',n)
   start_time = time.time()
   line_element = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
   index_to_add = Function.find_index_by_text(line_element,Workspace.H_BL[n])
   Line.append(line_element[index_to_add])
   driver.execute_script("arguments[0].click();", Line[n])
   time.sleep(1)
   actions = Dictionary.ActionChains(driver)
   actions.double_click(Line[n]).perform()
   time.sleep(1)
   #####################################
   QTY, WGT, CBM=Function.select_qty_wgt_cbm_by_hbl(Workspace.H_BL[n])
   current_datetime = datetime.now()
   future_datetime = current_datetime + timedelta(minutes=10)
   formatted_future_datetime = future_datetime.strftime("%Y-%m-%d %H:%M")
   String='This cargo has been unpacked at: '+str(formatted_future_datetime)
   FieldElement = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
   Index = Function.find_index_by_attribute(FieldElement,'value',Workspace.H_BL[n])
   HBLFields=FieldElement[Index]
   RecvFields=FieldElement[Index+17]
   QtyFields=FieldElement[Index+22]
   WgtFields=FieldElement[Index+24]
   CbmFields=FieldElement[Index+25]
   LocFields=FieldElement[Index+32]
   LocFieldsQty=FieldElement[Index+33]
   CaseMarkFields=FieldElement[Index+39]
   driver.execute_script("arguments[0].value=arguments[1];",QtyFields,QTY)
   driver.execute_script("arguments[0].value=arguments[1];",WgtFields,WGT)
   driver.execute_script("arguments[0].value=arguments[1];",CbmFields,CBM)
   driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",LocFields,Dictionary.random.choice(Workspace.LOC_CD_CG))
   driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",LocFields)
   driver.execute_script("arguments[0].value=arguments[1];",LocFieldsQty,QTY)
   driver.execute_script("arguments[0].value=arguments[1];",CaseMarkFields,String)
   driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",CaseMarkFields) 
   driver.execute_script("arguments[0].value = '';", RecvFields) # Clear Fields Receive Date
   driver.execute_script(f"arguments[0].value = '{formatted_future_datetime}';", RecvFields) # Input Receive Date
   driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",RecvFields)
   time.sleep(1)
   ###########################################################
   ButtonPrint=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-btn-button-center')))
   Index=Function.find_index_by_text(ButtonPrint,'Print')
   Icon=ButtonPrint[Index+8].click()
   time.sleep(2)
   ###########################################################
   ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
   Index=Function.find_index_by_text(ButtonSave,'Save')
   ButtonSave[Index].click() # Click Save
   time.sleep(1)
   ###########################################################
   # Waiting Until Save is Done
   Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_element_located((Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')))
   div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
   driver.execute_script("arguments[0].click();", div_elements[1])
   end_time = time.time()
   elapsed_time = end_time - start_time
   print("Cargo",Workspace.H_BL[n],"has been Unpacked","at",formatted_future_datetime)
   print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
   time.sleep(2)
   n += 1
print ('\n','All cargo has been Unpacked')   
print('Finish Test for Destuffing Operation')
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(1)
