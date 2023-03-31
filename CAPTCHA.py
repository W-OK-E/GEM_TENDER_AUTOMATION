from PIL import Image
import pytesseract as pt
pt.pytesseract.tesseract_cmd=r"E:\Tesseract_OCR\tesseract.exe"
def decaptcha(file_name):
    img=Image.open("Captcha.png")
    return(pt.image_to_string(img))