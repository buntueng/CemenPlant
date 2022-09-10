from fpdf import FPDF
import os
import subprocess


dir_path = os.path.dirname(os.path.realpath(__file__))
font_path = dir_path + r'/fonts/THNiramitAS.ttf'
output_path = dir_path + r'/bill_template.pdf'
bottom_offset = 10

pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
pdf.add_page()


pdf.add_font('niramit', '', font_path, uni=True)
#========= bill header =====
pdf.set_font('niramit', '', 20)
pdf.multi_cell(0, 10, 'ใบส่งของ (ต้นฉบับ)' + '\n' +'ห้างหุ้นส่วนจำกัดปานปริญ',border=True,ln=True,align='C')

#======== detail =============
pdf.set_font('niramit', '', 16)
pdf.cell(0, 10, 'แน่นอนจริงเชียว')
pdf.ln(20)


pdf.output(output_path, 'F')
subprocess.Popen(output_path,shell=True)