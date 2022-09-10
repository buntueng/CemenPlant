from fpdf import FPDF
import os
from pdfrw import PageMerge, PdfReader, PdfWriter
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))
font_path = dir_path + r'/fonts/THNiramitAS.ttf'
input_path = dir_path + r'/bill_template.pdf'
output_path = dir_path + r'/bill.pdf'

ON_PAGE_INDEX = 0
UNDERNEATH = False  # if True, new content will be placed underneath page (painted first)

def add_content(customer_name,address,cemen_formula,cemen_amount):
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    cemen_formula_to_display = ""
    if cemen_formula [-3:] == 'ksc':
        cemen_formula_to_display = cemen_formula[:-3]
    else:
        cemen_formula_to_display = cemen_formula
    fpdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
    fpdf.add_page()
    fpdf.add_font('niramit', '', font_path, uni=True)
    fpdf.set_font('niramit', '', 14)
    # add information to form
    fpdf.text(53, 62, customer_name)                         # customer name
    fpdf.text(53, 68, address)                               # customer address
    fpdf.text(87, 78, cemen_formula_to_display)              # cemen formula
    fpdf.text(55,94,cemen_amount)                            # concrete amount
    fpdf.text(55,100,current_date)                           # add date
    fpdf.text(115,100,current_time)                          # add time
    # add the same information to form
    fpdf.text(53, 182, customer_name)                         # customer name
    fpdf.text(53, 188, address)                               # customer address
    fpdf.text(87, 198, cemen_formula_to_display)              # cemen formula
    fpdf.text(55,214,cemen_amount)                            # concrete amount
    fpdf.text(55,220,current_date)                            # add date
    fpdf.text(115,220,current_time)                           # add time
    
    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]


customer_name_string = "บรรเทิง ยานะ"
customer_address_string = "นั่นไง"
cemen_formula_string = "210ksc"
amount_string = "2.5"

reader = PdfReader(input_path)
writer = PdfWriter()
writer.pagearray = reader.Root.Pages.Kids
PageMerge(writer.pagearray[ON_PAGE_INDEX]).add(add_content(customer_name=customer_name_string,address=customer_address_string,cemen_formula=cemen_formula_string,cemen_amount=amount_string), prepend=UNDERNEATH).render()
writer.write(output_path)
