from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# font_location = 'C:/Users/ASUS/Documents/git_project/CemenPlant/test_code/fonts/THNiramitAS.ttf'
# pdf_location = 'C:/Users/ASUS/Desktop/'
font_location = 'C:/Users/ASUS/Documents/git_project/CemenPlant/test_code/fonts/THNiramitAS.ttf'
pdf_location = 'C:/Users/ASUS/Desktop/'
pdfmetrics.registerFont(TTFont('TH',font_location))
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFont('TH', 10)
can.drawString(100, 100, "สบายดีป่าว บ้าไปแล้วววววววววว")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
or_file = pdf_location + "origin.pdf"
existing_pdf = PdfFileReader(open(or_file, "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
de_file = pdf_location + "destination.pdf"
outputStream = open(de_file, "wb")
output.write(outputStream)
outputStream.close()