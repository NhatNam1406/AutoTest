import sys
sys.path.append(r'C:\Users\TSB\Downloads\AutoTest\KPCFS\Input')
import Dictionary
####################### SET UP CONNECTION ORACLE DB #######################
# Connect to the Oracle database
conn = Dictionary.cx_Oracle.connect(
    user="CFS_LOCAL",
    password="success",
    dsn="orcl19"  # Service Name
)
# Create a cursor
cur = conn.cursor()
cur.execute("SELECT LOC_CD FROM CFS_LOCAL.TB_CARGO_AREA WHERE LOC_TYPE='VP'")
rows = cur.fetchall()
LOC_CD = [row[0] for row in rows]
cur.execute("SELECT LOC_CD FROM CFS_LOCAL.TB_CARGO_AREA WHERE LOC_TYPE='WL'")
rows = cur.fetchall()
LOC_CD_CG = [row[0] for row in rows]
cur.close()
conn.close()
###########################################################################
# Information of Doc
file_path = r'D:\IFCL-test.xlsx' 
df = Dictionary.pd.read_excel('D:/IFCL-test.xlsx')
column_index = 4
M_BL = df.iloc[2, column_index]
Container_No = df.iloc[2, column_index+1]
M_BL_list = [M_BL]
List_Ctnr = [Container_No]
H_BL = []
# Indicate the H.BL from column Bill of Landing
first_diff_index = None
for index, value in enumerate(df.iloc[2:, column_index], start=2):
    # Check if the value is different from M_BL
    if value != M_BL:
        first_diff_index = index
        break
if first_diff_index is not None:
    for value in df.iloc[first_diff_index:, column_index]:
        # Check if the value is null (NaN)
        if Dictionary.pd.isnull(value):
            # If it's null, stop iterating
            break
        # Otherwise, append the value to the list
        H_BL.append(value) # Save all HBL as a list
else:
    print("The H.BL and M.BL is the same")
# Start from the next row after the initial container number
row_index = 3  
while not Dictionary.pd.isnull(Container_No):
    Container_No = df.iloc[row_index, column_index+1]
    if not Dictionary.pd.isnull(Container_No):
        List_Ctnr.append(Container_No)
    row_index += 1
#############################################################################
## Data input Login
UserID='TSB'
Passpord='SUCCESS99'

