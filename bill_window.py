from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm,cm
from reportlab.platypus.tables import Table
import os
import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf

temp_pdf_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\temp_files\\temp_receipt.pdf"


def generate_pdf():
    c = canvas.Canvas(temp_pdf_file_path,pagesize=A4)
    c.setFont("TH Niramit AS", 30)
    c.drawString(100,750,"สวัสดีจร้าาา")
    c.setFont("TH Niramit AS", 12)
    c.drawString(200,750,"สบายดี")

    data=[(1,2),(3,4)]
    table = Table(data, colWidths=270, rowHeights=79)
    table.wrapOn(c,270,79)
    table.drawOn(c, 20, 20)
    c.save()


  
# ===== main program ===========
main_window = tk.Tk()
main_window.geometry("550x750")
pdfmetrics.registerFont(TTFont('TH Niramit AS', 'TH Niramit AS.ttf'))

top_frame = tk.Frame(master=main_window)
left_frame = tk.Frame(master=main_window)
right_frame = tk.Frame(master=main_window)
bottom_frame = tk.Frame(master=main_window)

# top_frame.grid(row=0,column=0,columnspan=2)
# left_frame.grid(row=1,column=0)
# right_frame.grid(row=1,column=1)
# bottom_frame.grid(row=2,column=0,columnspan=2)

top_frame.pack()
left_frame.pack()
right_frame.pack()
bottom_frame.pack()

#pdf_show_widget.img_object_li.clear()
pdf_area = pdf.ShowPdf().pdf_view(right_frame, pdf_location = temp_pdf_file_path,    width = 50, height = 100)
  
pdf_area.pack()

main_window.mainloop()