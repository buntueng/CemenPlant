from PyPDF2 import PdfFileWriter, PdfFileReader

def merge_file(output_pdf):
    bill_template = "/home/yana/Documents/CemenPlant/other_files/bill_template.pdf"
    input_pdf='tuto2.pdf'
    watermark_obj = PdfFileReader(bill_template)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)

if __name__ == '__main__':
    merge_file(output_pdf='Merged.pdf')