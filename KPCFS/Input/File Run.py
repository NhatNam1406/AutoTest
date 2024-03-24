import subprocess
import time
import os
from selenium.common.exceptions import TimeoutException

test_directory = r"C:\Users\TSB\Downloads\AutoTest\KPCFS\Testcase"
report_directory = r"C:\Users\TSB\Downloads\AutoTest\KPCFS\Output"  # Directory to save reports
Errorcase=0
# Create the Reports directory if it doesn't exist
if not os.path.exists(report_directory):
    os.makedirs(report_directory)

# List of Python files you want to run sequentially
test_files  = ["test_upload_excel.py", "test_manifest_list.py", "test_import_work_order.py","test_work_order_list.py", "test_gate_control.py", "test_plat_control.py","test_destuffing_operation.py","test_import_load_order.py"]
#test_files  = ["test_upload_excel.py","test_work_order_list.py","test_gate_control.py","test_plat_control.py"]
#test_files  = ["test_destuffing_operation.py"]

for file in test_files:
    full_path = os.path.join(test_directory, file)
    report_path = os.path.join(report_directory, file.replace('.py', '_report.txt'))  # Path to save report
    
    start_time = time.time()  # Start time
    
    print('Test Case:', file)
    with open(report_path, 'w') as report_file:
        process = subprocess.Popen(["python", full_path], stdout=report_file, stderr=subprocess.STDOUT)
        process.wait()

    if process.returncode != 0:  # Check if subprocess returned non-zero return code
        print(f"Error occurred while executing {file}. Return code: {process.returncode}")
        Errorcase+=1
        break
    else:
     end_time = time.time()  # End time
     elapsed_time = end_time - start_time  # Elapsed time
     print(f"Time consumed for {file}: {elapsed_time:.2f} seconds")
if(Errorcase==0):
 print("All tests executed. Reports saved in:", report_directory)