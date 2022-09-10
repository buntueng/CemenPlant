import os
from datetime import datetime
software_path = os.path.dirname(os.path.realpath(__file__))

bbok = "121"
present_time = datetime.now()
current_date_string = present_time.strftime('%d%B%Y')
bill_path1 = os.path.join(software_path,"bills")
bill_path2 = os.path.join(bill_path1 ,current_date_string)

if os.path.isdir(bill_path2):
    pass
else:
    os.makedirs(bill_path2)
output_file_name = bbok +".pdf"
output_path = os.path.join(bill_path2,output_file_name)
print(output_path)