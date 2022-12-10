from fpdf import FPDF
 
pdf = FPDF()
 
# Add a page
pdf.add_page()
 
pdf.add_font("THNiramit", "", "/home/plant/Documents/CemenPlant/fonts/THNiramitAS.ttf")
pdf.set_font("THNiramit")
#pdf.set_font("Arial", size = 15)
 
# create a cell
pdf.cell(200, 10, txt = "แมว",ln = 1, align = 'C')
 
# add another cell
pdf.cell(200, 10, txt = "A Computer Science portal for geeks.",ln = 2, align = 'C')
 
# save the pdf with name .pdf
pdf.output("./GFG.pdf") 