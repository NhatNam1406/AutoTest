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

# Navigate to Work Order List
print('Navigate to Work Order List')
BillingTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(BillingTab,'Billing')
BillingTab[Index].click() # Click Billing
time.sleep(1)
WorkOrderListTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(WorkOrderListTab,'Work Order List')
WorkOrderListTab[Index].click() # Click Import
time.sleep(1) 
 
# Find the Fields text MBL to input
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find('input', attrs={'role': 'textbox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-text-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'textfield-1129-ariaStatusEl'})
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
n=0
while(n<1):
 start_time = time.time()
 #######################################
 print('\n','Select the row:',n)
 start_time = time.time()
 Function.check_first_hbl_textbox(driver,Workspace.H_BL[n],Workspace.H_BL)
 #######################################
 print('Tick The Work Successfully')
 time.sleep(1)
 ButtonInvoice=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonInvoice,'Invoice')
 ButtonInvoice[Index].click() # Click Invoice
 print('Open The Invoice Details')
 time.sleep(1)
 page_source = driver.page_source
 soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
 textbox_input_fields = soup.find('input', attrs={'role': 'combobox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-empty-field-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'combo-1145-ariaStatusEl'})
 if textbox_input_fields is not None:
    ID_Template = textbox_input_fields.get('id')
    InvoiceTemplate=driver.find_element(Dictionary.By.ID,ID_Template)
    InvoiceTemplate.send_keys('IMPORT')
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", InvoiceTemplate)
    print("Select the Invoice Template IMPORT")
 else:
    print("Can not find the fields to input Invoice Template")
 time.sleep(1)
 ButtonGenerate=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonGenerate,'Generate Invoice')
 ButtonGenerate[Index].click() # Click Generate
 print('Generate Draft Invoice')
 time.sleep(4)
 ##################################################
 # Collect UI fields show in log
 Fields=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
 Draftinvoice=Fields[39].get_attribute('value')
 Payer=Fields[40].get_attribute('value')
 Paymenttype=Fields[45].get_attribute('value')
 Netamt=Fields[57].get_attribute('value')
 Vatamt=Fields[60].get_attribute('value')
 Amt=Fields[61].get_attribute('value')
 print("The draft invoice",Draftinvoice,"has been created")
 print("Payer:",Payer,'|',"Payment type:",Paymenttype)
 print("Net amount:",Netamt,'|',"Vat amount:",Vatamt,'|',"Total amount:",Amt)
 ###################################################
 try:
     ButtonPrint=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
     Index=Function.find_index_by_text(ButtonPrint,'Print')
     driver.execute_script("arguments[0].click();",ButtonPrint[Index])
     time.sleep(3)
     driver.switch_to.window(driver.window_handles[-1])
     time.sleep(4)
 finally:
     driver.close()
     driver.switch_to.window(driver.window_handles[0])
 time.sleep(1)
 ###################################################
 # Issue the invoice
 ButtonIssue=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
 Index=Function.find_index_by_text(ButtonIssue,'Issue Invoice')
 driver.execute_script("arguments[0].click();",ButtonIssue[Index])
 print('Issue Invoice')
 time.sleep(4)
  ##################################################
 # Collect UI fields show in log
 Fields=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
 Invoiceno=Fields[39].get_attribute('value')
 Payer=Fields[40].get_attribute('value')
 Paymenttype=Fields[45].get_attribute('value')
 Netamt=Fields[57].get_attribute('value')
 Vatamt=Fields[60].get_attribute('value')
 Amt=Fields[61].get_attribute('value')
 print("The invoice",Invoiceno,"has been issue")
 print("Payer:",Payer,'|',"Payment type:",Paymenttype)
 print("Net amount:",Netamt,'|',"Vat amount:",Vatamt,'|',"Total amount:",Amt)
 print("\n")
 ###################################################
 try:
     ButtonPrint=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
     Index=Function.find_index_by_text(ButtonPrint,'Print')
     driver.execute_script("arguments[0].click();",ButtonPrint[Index])
     time.sleep(3)
     driver.switch_to.window(driver.window_handles[-1])
     time.sleep(3)
 finally:
     driver.close()
     driver.switch_to.window(driver.window_handles[0])
 n+=1
time.sleep(1)
driver.quit()
print('Close Window')











