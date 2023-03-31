import os
from PyPDF2 import PdfReader
import fpdf
from PyPDF2 import PdfFileMerger


def generate(ext):
    file=open(f"E:\\ANACONDA\\Scripts\\New Folder\\GeM-Bidding-{ext}.pdf","rb") 
    reader=PdfReader(file)
    pages=reader.numPages
    f,l=-1,-1
    add=''
    for page_num in range(1,pages):
        page=reader.pages[pages-page_num]
        text=page.extract_text()
        if l==-1:
            l=text.find("Disclaimer")
            if f==-1:
                add=text[:l]
                f=text.find("Buyer Added Bid Specific Terms and Conditions")
                if f!=-1:
                    #print(l,f)
                    add=text[f+45:l]
                    break
        if f==-1:
            f=text.find("Buyer Added Bid Specific Terms and Conditions")
            if f!=-1 and l!=-1:
                add=text[f+45:]+add
            
        if f!=-1 and l!=-1:
            break
    try:
        os.remove("TEMP_ATC_CERT.pdf")
    except:
        pass
    try:
        os.remove("REQ.pdf")
    except:
        pass
    txt=  " M/S SAINDIA RESOURCES PRIVATE LIMITED \nHEAD OFFICE ADDRESS : 493, Sector-9, Faridabad : 121006 (HR.)\nTELE PHONE/MOBILE : 0129-4020493, 9654513919, 98739 32836,7905269141\nE-mail ID : saindiaresources20@yahoo.com\n"
    pdf=fpdf.FPDF()
    pdf.add_font('Calibri','','C:\\Windows\\Fonts\\Calibri.ttf')
    pdf.add_page()
    image_path="HEAD.JPG"
    pdf.set_compression(False)
    pdf.set_font('Calibri',size=12)
    pdf.image(image_path, x=10, y=0, w=100)
    
    pdf.ln(30)
    pdf.write(txt=txt)
    pdf.ln(10)
    pdf.cell(txt="We Accept The following ATC:")
    pdf.set_font("Calibri",size=9)
    pdf.ln(5)
    pdf.write(txt=add)
    pdf.ln(3)
    pdf.cell(txt="We also agree with the SOW described in the bid document.")
    pdf.ln(10)
    pdf.image("STAMP_SAI.PNG",x=20)
    pdf.ln(5)
    pdf.set_font_size(12)
    pdf.cell(txt="Required/Additional Documents attached for transparency!")
    #pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
    pdf.output("TEMP_ATC_CERT.pdf")
    
    merger=PdfFileMerger(strict=True)
    merger.append("TEMP_ATC_CERT.pdf")
    merger.append("ATC_TAIL.pdf")
    merger.write("E:\\ANACONDA\\Scripts\\New Folder\\REQ_ATC.pdf")
