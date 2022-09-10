import os
software_path = os.path.dirname(os.path.realpath(__file__))
print_pdf = "lp " + software_path  + "/bill_template.pdf"
os.system(print_pdf)
# os.system("lp bill_template.pdf")
#os.system("lp -d YOUR_PRINTER_NAME bill_template.pdf")
