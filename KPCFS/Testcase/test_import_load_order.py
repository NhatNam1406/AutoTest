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

# Navigate to Import Load Order
print('Navigate to Import Load Order')
start_time = time.time()
ImportTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportTab,'Import')
ImportTab[Index].click() # Click Import
time.sleep(1)
ImportoadOrderTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
Index=Function.find_index_by_text(ImportoadOrderTab,'Import Load Order')
ImportoadOrderTab[Index].click() # Click Manifest List
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
time.sleep(1)
# Input M.BL
start_time = time.time()
page_source = driver.page_source
soup = Dictionary.BeautifulSoup(page_source, 'html.parser')
textbox_input_fields = soup.find('input', attrs={'role': 'textbox', 'data-ref': 'inputEl', 'type': 'text', 'size': '1', 'class': 'x-form-empty-field-default', 'tabindex': '1', 'style': 'background-color: rgb(240, 248, 255);', 'aria-describedby': 'textfield-1148-ariaStatusEl'})
if textbox_input_fields is not None:
    ID_MBL = textbox_input_fields.get('id')
    driver.find_element(Dictionary.By.ID,ID_MBL).send_keys(Workspace.M_BL)
    print('Input M.BL Complete')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
else:
    print("Can not find the fields to input MBL")
time.sleep(1)
# Clear Received Date Period
start_time = time.time()
Fields = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-form-text-default')))
indices = [index for index, element in enumerate(Fields) if index > 6 and Function.is_valid_date_format(element.get_attribute('value'))]
for i in range(len(indices)):
  driver.execute_script("arguments[0].value=null;",Fields[indices[i]])
  driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Fields[indices[i]])
end_time = time.time()
elapsed_time = end_time - start_time
print('Clearing Receive Date success')
print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
time.sleep(1)
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()  # Click Search
time.sleep(1)
# Select each line
line_element = Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
index_Status= Function.find_index_by_text(line_element,'Remained')
Status=line_element[index_Status].text
if (Status == 'Remained'):
 start_time = time.time()
 Line=[]
 Payment_type=[]
 n=0
 for n in range(len(Workspace.H_BL)):
  ###########################################
  print('Start to book line:',n)
  line_element = Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
  index_to_add = Function.find_index_by_text(line_element,Workspace.H_BL[n])
  Line.append(line_element[index_to_add])
  Line[n].click()
  actions = Dictionary.ActionChains(driver)
  actions.double_click(Line[n]).perform()
  time.sleep(1)
  ############################################
  # Collect data in UI
  class UI_DATA:
   def __init__(self,list):
    if (len(list)==93):
      self.H_BL=list[43].get_attribute('value')
      self.M_BL=list[44].get_attribute('value')
      self.Stock_No=list[45].get_attribute('value')
      self.Work_No=list[46].get_attribute('value')
      self.Recv_Date=list[49].get_attribute('value')
      self.Free_time=list[77].get_attribute('value')
      self.Payment_type=list[78].get_attribute('value')
      self.Time_slot=list[50]
      self.Qty=list[51].get_attribute('value')
      self.Pckg=list[52].get_attribute('value') 
      self.Out_Wgt=list[56].get_attribute('value')
      self.Out_Cbm=list[57].get_attribute('value')
      self.BOE=list[58]
      self.Bill_Dest=list[75].get_attribute('value')
      self.Devl_remark=list[89]
    else:
      print('Wrong index')
  Fields=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
  Date_Line=UI_DATA(Fields) 
  print("M.BL:",Date_Line.M_BL,'|',"H.BL:",Date_Line.H_BL,'|',"Stock No:",Date_Line.Stock_No,'|',"Work No:",Date_Line.Work_No)
  print("Receive Date:",Date_Line.Recv_Date) 
  print("Free Time:",Date_Line.Free_time)
  time.sleep(1)
  #############################################
  i=Dictionary.random.randint(0, 1)
  Random_Date=Function.TimeslotCase[i](Date_Line.Recv_Date,Date_Line.Free_time) 
  driver.execute_script("arguments[0].value=null;",Date_Line.Time_slot)
  driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Time_slot, Random_Date)
  driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Date_Line.Time_slot)
  print("Timeslot:",Random_Date)
  if(i==0):
    print("Test case Timeslot in Free Expire Date")
  else:
    print("Test case Timeslot have a Storage Charge")
  print("Qty:",Date_Line.Qty,Date_Line.Pckg,'|',"Weight:",Date_Line.Out_Wgt,'|',"CBM:",Date_Line.Out_Cbm)
  Payment_type.append(Date_Line.Payment_type)
  print("Billing Dest:",Date_Line.Bill_Dest,'|',"Payment type:",Payment_type[n])
  BOE=Function.generate_random_string(6)
  driver.execute_script("arguments[0].value = arguments[1];", Date_Line.BOE, BOE)
  driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Date_Line.BOE)
  Remark=str("This cargo has been book in: " + Random_Date)
  driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Devl_remark, Remark)
  driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Date_Line.Devl_remark)
  print("BOE:",BOE)
  print("Delivery Remark:",Remark,'\n')
  time.sleep(1) 
  ##########################################
  ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
  Index=Function.find_index_by_text(ButtonSave,'Save')
  driver.execute_script("arguments[0].click();",ButtonSave[Index]) # Click Save 
  time.sleep(2)
  # Waiting Until Save is Done
  Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_element_located((Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')))
  div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
  driver.execute_script("arguments[0].click();", div_elements[1])
  time.sleep(1)
 ###########################################
 n += 1
 end_time = time.time()
 elapsed_time = end_time - start_time
 print('All line has been book success')
 print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
time.sleep(1)
# Search Again
SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
Index=Function.find_index_by_text(SearchButton,'Search')
SearchButton[Index].click()
time.sleep(1)
#############################################################
# Set Status Booked
line_element = Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
index_Status= Function.find_index_by_text(line_element,'Booked')
Status=line_element[index_Status].text
if (Status == 'Booked'):
  start_time = time.time()
  Line=[]
  Payment_Status=[]
  n=0
  print("Lenght of HBL:",len(Workspace.H_BL))
  while n <len(Workspace.H_BL):
    ####################################
    print('Start to delivery line:',n)
    line_element = Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
    index_to_add = Function.find_index_by_text(line_element,Workspace.H_BL[n])
    time.sleep(1)
    index_to_payment = index_to_add + 4
    Payment_Status.append(line_element[index_to_payment].text)
    Line.append(line_element[index_to_add])
    Payment=Payment_Status[n]
    print("Payment Status:",Payment)
    ####################################
    if(Payment=='Paid')or(Payment_type[n]=='Credit'):
     Line[n].click()
     actions = Dictionary.ActionChains(driver)
     actions.double_click(Line[n]).perform()
     time.sleep(1)
     #####################################
     class DELIVERY_DATA:
      def __init__(self,list):
       if (len(list)==93):
         self.H_BL=list[43].get_attribute('value')
         self.M_BL=list[44].get_attribute('value')
         self.Stock_No=list[45].get_attribute('value')
         self.Work_No=list[46].get_attribute('value')
         self.Time_slot=list[50].get_attribute('value')
         self.Pckg=list[52].get_attribute('value')
         self.Out_Wgt=list[56].get_attribute('value')
         self.Out_Cbm=list[57].get_attribute('value')
         self.Qty=list[51].get_attribute('value')
         self.Over_date=list[79].get_attribute('value')
         self.BOE=list[58]
         self.Truck_No=list[59]
         self.Visit_code=list[60]
         self.Driver_ID=list[61]
         self.Actual_Qty=list[62]
         self.Delivery_Time=list[63]
       else:
         print('Wrong index')
     Fields=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
     Date_Line=DELIVERY_DATA(Fields)
     ##################################
     # Input Data in UI
     Truck_No=Function.generate_truck_number()
     driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Truck_No, Truck_No)
     Driver_ID=Function.generate_driver_id()
     driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Driver_ID, Driver_ID)
     driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Actual_Qty, Date_Line.Qty)
     driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Date_Line.Actual_Qty)
     driver.execute_script("arguments[0].value = arguments[1];", Date_Line.Delivery_Time, Date_Line.Time_slot)
     driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", Date_Line.Delivery_Time)
     print("Truck No:",Truck_No,'|',"Driver ID:",Driver_ID)
     print("Out Qty:",Date_Line.Qty,'|',"Actual Delivery Date:",Date_Line.Time_slot,'|',"Over Date:",Date_Line.Over_date,'\n') 
     time.sleep(1)
     ##################################
     ButtonSave=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
     Index=Function.find_index_by_text(ButtonSave,'Save')
     driver.execute_script("arguments[0].click();",ButtonSave[Index]) # Click Save 
     time.sleep(2)
     # Waiting Until Save is Done
     Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_element_located((Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')))
     div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
     driver.execute_script("arguments[0].click();", div_elements[1])
     time.sleep(1)
     ##################################
     n+=1
    elif (Payment =='UnPaid')and(Payment_type[n]=='Cash'):
      ############################################
      line_element = Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
      index_to_add = Function.find_index_by_text(line_element,Workspace.H_BL[n])
      HBL_Viewlist=line_element[index_to_add].text
      MBL_Viewlist=line_element[index_to_add+1].text
      BillingTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
      Index=Function.find_index_by_text(BillingTab,'Billing')
      driver.execute_script("arguments[0].click();",BillingTab[Index]) # Click Blling
      time.sleep(1)
      WorkOrderListTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
      Index=Function.find_index_by_text(WorkOrderListTab,'Work Order List')
      WorkOrderListTab[Index].click() # Click Work Order List
      time.sleep(1)
     #############################################
      Fields=Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
      indices = [index for index, element in enumerate(Fields) if index > 6 and Function.is_valid_date_format(element.get_attribute('value'))]
      largest_index = max(indices, default=None)
      Index=largest_index+14
      if Index is not None:
        FieldsMBL=Fields[Index]
        FieldsMBL.send_keys(Workspace.M_BL)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",FieldsMBL)
      else:
        print("Can not find the fields to input MBL")
      time.sleep(1)
     #############################################
      SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
      Index=Function.find_index_by_text(SearchButton,'Search')
      SearchButton[Index].click()  # Click Search
      time.sleep(1)
     #############################################
      A=HBL_Viewlist
      a=0
      while (A==HBL_Viewlist):  
        WOL_Fields=Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
        WOL_check =Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-checkcolumn')))
        index_HBL= Function.find_index_by_text(WOL_Fields,A)
        index_work_order_seq= index_HBL+5
        index_work_status= index_HBL+6
        if (WOL_Fields[index_HBL].text==HBL_Viewlist)and(int(WOL_Fields[index_work_order_seq].text)!=0)and(WOL_Fields[index_work_status].text=='Completed'):
           A=0 # Set up A != HBL_Viewlist to break the loop while
           print(WOL_Fields[index_HBL].text,'|',int(WOL_Fields[index_work_order_seq].text),'|',WOL_Fields[index_work_status].text)
           CompareHBL=WOL_Fields[index_HBL].text
           WOL_check =Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-checkcolumn')))
           WOL_check_dict = {}
           k = 0
           for check_element in WOL_Fields: # Compare value HBL in UI with H_BL list in excel file and change the index from k=0
            for hbl_value in Workspace.H_BL:
              if check_element.text == hbl_value:
                WOL_check_dict[check_element.text] = k
                k += 1
                break
           index_check=Function.find_index_by_value(WOL_check_dict, CompareHBL)
           WOL_check[index_check].click()
        else:
           a=a+1
        print("Begin to Collect Extra Storage or Handling Charges")
        ############################################# Generate the invoice ####################
        InvoiceButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index=Function.find_index_by_text(InvoiceButton,'Invoice')
        driver.execute_script("arguments[0].click();",InvoiceButton[Index]) # Click Search
        time.sleep(1)
        ContainValue = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
        Index=Function.find_index_by_attribute(ContainValue,'value','Forwarder') # Indicate the index of Fields Forwarder
        IndexInvoiceTempalte= Index-2
        IndexDraftInvoice= Index+2
        IndexAmt=Index+24
        driver.execute_script("arguments[0].setAttribute('value', arguments[1]);",ContainValue[IndexInvoiceTempalte],'IMPORT')
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",ContainValue[IndexInvoiceTempalte])
        time.sleep(1)
        GenerateButton =Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index= Function.find_index_by_text(GenerateButton,'Generate Invoice')
        driver.execute_script("arguments[0].click();",GenerateButton[Index])
        time.sleep(1)
        DraftInvoiceNo=ContainValue[IndexDraftInvoice].get_attribute('value')
        DraftAmt= ContainValue[IndexAmt].get_attribute('value')
        print('The Draft Invoice',DraftInvoiceNo,'has been created with amount:',DraftAmt)
        #############################################
        try:          
          PrintButton =Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
          Index= Function.find_index_by_text(PrintButton,'Print')
          time.sleep(4)
          driver.execute_script("arguments[0].click();",PrintButton[Index])
          driver.switch_to.window(driver.window_handles[-1])
          time.sleep(4)
        finally:
          driver.close()
          driver.switch_to.window(driver.window_handles[0])
          time.sleep(1)  
        ##############################################  
        IssueButton =Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index= Function.find_index_by_text(IssueButton,'Issue Invoice')
        driver.execute_script("arguments[0].click();",IssueButton[Index])  
        time.sleep(1)
        ContainValue = Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-form-text-default')))
        Index=Function.find_index_by_attribute(ContainValue,'value','Forwarder') 
        IndexInvoiceNo= Index+2
        IndexAmt=Index+24
        print('The Invoice',ContainValue[IndexInvoiceNo].get_attribute('value'),'has been created with amount:',ContainValue[IndexAmt].get_attribute('value'))
        ###############################################
        try:          
          PrintButton =Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
          Index= Function.find_index_by_text(PrintButton,'Print')
          driver.execute_script("arguments[0].click();",PrintButton[Index])
          driver.switch_to.window(driver.window_handles[-1])
          time.sleep(3)
        finally:
          driver.close()
          driver.switch_to.window(driver.window_handles[0])
          time.sleep(1) 
        ###############################################  
        div_elements = driver.find_elements(Dictionary.By.CSS_SELECTOR, 'div[data-ref="toolEl"].x-tool-tool-el.x-tool-img.x-tool-close[role="presentation"]')
        Function.find_icon_close_X(driver,div_elements)
        time.sleep(1) 
        BillingTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-treelist-item-text')))
        Index=Function.find_index_by_text(BillingTab,'Billing')
        BillingTab[Index].click()
        time.sleep(1)
        IconCloseTab=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-tab-close-btn')))
        Index= Function.find_index_by_text(IconCloseTab,'removable')
        driver.execute_script("arguments[0].click();",IconCloseTab[Index+1])
        time.sleep(1)
        SearchButton=Dictionary.WebDriverWait(driver, 10).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME,'x-btn-inner-default-small')))
        Index= Function.find_index_by_text(SearchButton,'Search')
        driver.execute_script("arguments[0].click();",SearchButton[Index])
       ################################################
        Payment_Status.pop()
        Line.pop()
end_time = time.time()
elapsed_time = end_time - start_time
print('All line has been deliveried success')
print(f"Time consumed  {elapsed_time:.2f} seconds","\n")
time.sleep(1)



     



