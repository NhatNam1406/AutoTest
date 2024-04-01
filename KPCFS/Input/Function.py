import sys
sys.path.append(r'C:\Users\nhatn\Downloads\Python\KPCFS-AutoTest\KPCFS\Input')
import Function
import Dictionary
import Workspace
from selenium import webdriver
import os
import time
from datetime import datetime, timedelta
import cx_Oracle
from datetime import datetime
import random
import string

def Timeslot_in_free_storage(A,B):
    A = datetime.strptime(A, "%Y-%m-%d %H:%M")
    B = datetime.strptime(B, "%Y-%m-%d %H:%M")
    days_difference = (B - A).days
    random_days = random.randint(0, days_difference)
    random_date = A + timedelta(days=random_days)
    random_date_str = random_date.strftime("%Y-%m-%d %H:%M")
    return random_date_str

def Timeslot_storage(A, B):
    A = datetime.strptime(A, "%Y-%m-%d %H:%M")
    B = datetime.strptime(B, "%Y-%m-%d %H:%M")
    B_plus_4_days = B + timedelta(days=4)
    days_difference = (B_plus_4_days - B).days
    random_days = random.randint(1, days_difference)  
    random_date = B + timedelta(days=random_days)
    random_date_str = random_date.strftime("%Y-%m-%d %H:%M")
    return random_date_str
TimeslotCase = [Timeslot_storage,Timeslot_in_free_storage] # Mix case
#TimeslotCase = [Timeslot_storage,Timeslot_storage]

def generate_random_string(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_truck_number():
    # Define the pattern for the truck number (e.g., "ABC1234")
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))  
    digits = ''.join(random.choices(string.digits, k=4))  
    return f"{letters}{digits}".upper()  

def generate_driver_id():
    # Generate a random driver ID with a pattern (e.g., "DRV12345")
    prefix = "DRV"  # Fixed prefix for driver IDs
    digits = ''.join(random.choices(string.digits, k=5))  # Random 5 digits
    return f"{prefix}{digits}"

def find_index_by_text(elements, target_text, partial_match=False):
    for i, element in enumerate(elements):
        if partial_match:
            if target_text in element.text:
                return i
        else:
            if element.text == target_text:
                return i
    return None

def find_index_by_attribute(elements, attribute_name, target_value):
    for i, element in enumerate(elements):
        if element.get_attribute(attribute_name) == target_value:
            return i
    return None

def find_index_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if key == target_value:
            return value
    return None

def find_icon_close_X(driver,div_elements):
 for div_element in div_elements:
    div_id = div_element.get_attribute('id')
    while True:
        try:
            A= driver.find_element(Dictionary.By.ID,div_id).click()
        except Dictionary.ElementNotInteractableException:
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(Dictionary.By.ID, div_id))
                break
            except Dictionary.NoSuchElementException:
                break
        except Dictionary.ElementClickInterceptedException:
            try: 
                driver.execute_script("arguments[0].click();", driver.find_element(Dictionary.By.ID, div_id))
                break
            finally:
                print("ABCDE")
                break
        except Dictionary.NoSuchElementException:
            break

# Input value HBL_Viewlist want to check and list of H_BL
def check_first_hbl_textbox(driver,HBL_Viewlist,H_BL):
    WOL_Fields=Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-cell-inner')))
    WOL_check =Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-checkcolumn')))
    index_HBL= Function.find_index_by_text(WOL_Fields,HBL_Viewlist)
    index_work_order_seq= index_HBL+5
    index_work_status= index_HBL+6
    if (WOL_Fields[index_HBL].text==HBL_Viewlist)and(int(WOL_Fields[index_work_order_seq].text)==0)and(WOL_Fields[index_work_status].text=='Completed'):
           print(WOL_Fields[index_HBL].text,'|',int(WOL_Fields[index_work_order_seq].text),'|',WOL_Fields[index_work_status].text)
           CompareHBL=WOL_Fields[index_HBL].text
           WOL_check =Dictionary.WebDriverWait(driver, 120).until(Dictionary.EC.presence_of_all_elements_located((Dictionary.By.CLASS_NAME, 'x-grid-checkcolumn')))
           WOL_check_dict = {}
           k = 0
           B = 0
           for check_element in WOL_Fields:
            for hbl_value in H_BL:
              if check_element.text == hbl_value:
                if (check_element.text != B):
                   WOL_check_dict[check_element.text] = k
                   B=check_element.text
                   k += 1
                else: # Xu ly neu dictionary co gia tri key bi trung thi break va lay gia tri dau tien
                    break  
              break
           index_check=Function.find_index_by_value(WOL_check_dict, CompareHBL)
           WOL_check[index_check].click()

def select_qty_wgt_cbm_by_hbl(HBL):
    conn = cx_Oracle.connect( user="CFS_LOCAL",   password="success", dsn="orcl19" )
    cur = conn.cursor()
    SQL_SELECT_QTY="SELECT PCKG_QTY FROM CFS_LOCAL.TB_IM_BL WHERE BL_NO=:BL_NO"
    SQL_SELECT_WGT="SELECT WGT FROM CFS_LOCAL.TB_IM_BL WHERE BL_NO=:BL_NO"
    SQL_SELECT_CBM="SELECT CBM FROM CFS_LOCAL.TB_IM_BL WHERE BL_NO=:BL_NO"
    cur.execute(SQL_SELECT_QTY,BL_NO=HBL)
    QTY=cur.fetchone()
    cur.execute(SQL_SELECT_WGT,BL_NO=HBL)
    WGT=cur.fetchone()
    cur.execute(SQL_SELECT_CBM,BL_NO=HBL)
    CBM=cur.fetchone()
    cur.close()
    conn.close()
    print('HBL:',HBL,'have value Qty:', QTY[0],' Weight:',WGT[0],' CBM:',CBM[0])
    return QTY,WGT,CBM


def is_valid_date_format(date_str):
    try:
        # Attempt to parse the date string using the strptime method
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
