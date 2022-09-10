from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter

input_path = "/home/yana/Documents/CemenPlant/other_files/bill_template.pdf"

pdf_reader = PdfReader(input_path)
pdf_writer = PdfWriter()
pdf_writer.pagearray = pdf_reader.Root.Pages.Kids
# Instantiation of inherited class
pdf = FPDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.add_font("Arial", "", "/home/yana/Documents/CemenPlant/fonts/THNiramitAS.ttf", uni=True)
pdf.set_font("Arial")
for i in range(1, 41):
    pdf.text(0, 10,"เอ๋")
pdf.output('tuto2.pdf', 'F')
reader = PdfReader('tuto2.pdf')
            # =================================================

PageMerge(pdf_writer.pagearray[0]).add(reader, prepend=False).render()
pdf_writer.write("mergedFile.pdf")