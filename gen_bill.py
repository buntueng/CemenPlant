# import os
# import tkinter as tk
# from tkinter import  DISABLED, StringVar, font
# from share_library import center_screen, default_window_size
# from os.path import exists

# from fpdf import FPDF
# from pdfrw import PageMerge, PdfReader, PdfWriter
# from datetime import datetime
# from PyPDF2 import PdfFileWriter, PdfFileReader

# software_path = os.path.dirname(os.path.realpath(__file__))
# dir_path = os.path.dirname(os.path.realpath(__file__))
# font_path = dir_path + r'/fonts/THNiramitAS.ttf'
# input_path = dir_path + r'/other_files/bill_template.pdf'
# temp_path = dir_path +r'/bills/temp_bill.pdf'

# ON_PAGE_INDEX = 0
# UNDERNEATH = False  # if True, new content will be placed underneath page (painted first)


# def add_bill(customer_name,address,cemen_formula,cemen_amount):
#     now = datetime.now()
#     current_date = now.strftime("%d/%m/%Y")
#     current_time = now.strftime("%H:%M:%S")
#     cemen_formula_to_display = ""
#     if cemen_formula [-3:] == 'ksc':
#         cemen_formula_to_display = cemen_formula[:-3]
#     else:
#         cemen_formula_to_display = cemen_formula
#     #============================================================
#     pdf_reader = PdfReader(input_path)
#     pdf_writer = PdfWriter()
#     pdf_writer.pagearray = pdf_reader.Root.Pages.Kids
#     # Instantiation of inherited class
#     fpdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
#     fpdf.alias_nb_pages()
#     fpdf.add_page()
#     fpdf.add_font("THNiramit", "", font_path)
#     fpdf.set_font("THNiramit")
#     # add information to form
#     fpdf.text(53, 62, customer_name)                         # customer name
#     fpdf.text(53, 68, address)                               # customer address
#     fpdf.text(87, 78, cemen_formula_to_display)              # cemen formula
#     fpdf.text(55,95,cemen_amount)                            # concrete amount
#     fpdf.text(55,102,current_date)                           # add date
#     fpdf.text(115,102,current_time)                          # add time
#     fpdf.text(53,108,"fff")
#     # add the same information to form
#     fpdf.text(53, 184, customer_name)                         # customer name
#     fpdf.text(53, 190, address)                               # customer address
#     fpdf.text(87, 200, cemen_formula_to_display)              # cemen formula
#     fpdf.text(55,217,cemen_amount)                            # concrete amount
#     fpdf.text(55,223,current_date)                            # add date
#     fpdf.text(115,223,current_time)                           # add time
#     fpdf.text(53,229,"ffff")
#     fpdf.output(temp_path, 'F')
#     #============================================================    
# def merge_bill(output_pdf):
#     bill_template = "/home/plant/Documents/CemenPlant/other_files/bill_template.pdf"
#     #bill_template =input_path
#     input_pdf ="/home/plant/Documents/CemenPlant/bills/temp_bill.pdf"
#     #input_pdf = temp_path
#     watermark_obj = PdfFileReader(bill_template)
#     watermark_page = watermark_obj.getPage(0)

#     pdf_reader = PdfFileReader(input_pdf)
#     pdf_writer = PdfFileWriter()

#     for page in range(pdf_reader.getNumPages()):
#         page = pdf_reader.getPage(page)
#         page.mergePage(watermark_page)
#         pdf_writer.addPage(page)

#     with open(output_pdf, 'wb') as out:
#         pdf_writer.write(out)



import PyPDF2
pdf_file = "./test_code/bill_template.pdf"
watermark = "./test_code/Bill.pdf"
merged_file = "./test_code/merged.pdf"
input_file = open(pdf_file,'rb')
input_pdf = PyPDF2.PdfFileReader(input_file)
watermark_file = open(watermark,'rb')
watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
pdf_page = input_pdf.getPage(0)
watermark_page = watermark_pdf.getPage(0)
pdf_page.mergePage(watermark_page)
output = PyPDF2.PdfFileWriter()
output.addPage(pdf_page)
merged_file = open(merged_file,'wb')
output.write(merged_file)
merged_file.close()
watermark_file.close()
input_file.close()