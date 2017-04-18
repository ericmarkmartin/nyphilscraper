from fpdf import FPDF
from PIL import Image


def make_PDF(file, listPages):
    print('Creating PDF')

    cover = Image.open(listPages[0])
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in listPages:
        pdf.add_page()
        print(page)
        pdf.image(page, 0, 0)

    pdf.output(file, 'F')
