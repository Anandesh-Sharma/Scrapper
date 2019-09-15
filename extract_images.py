import minecart
import os
from PIL import Image


# Using minecart here for image extractinon there which depends on pdfminer 3x latest
# pdfminer version is pdfminer 6x which is not supported by minecart
# There are several other libraries also which can be use like PyPDF2, PyMUdf

def extract_images(file):
    cmd = "pdfinfo '%s' | grep 'Pages' | awk '{print $2}'" % file
    d = int(os.popen(cmd).read().strip())
    j = 0
    pdffile = open(file, "rb")
    doc = minecart.Document(pdffile)
    image_dict = {
        'aadhar_font': '',
        'aadhar_back': '',
        'pan': '',
        'selfie': ''
    }
    aadhar_front = aadhar_back = pan = selfie = ''
    if d > 19:
        for i in range(d - 2, d):
            page = doc.get_page(i)
            if j == 0 and i == 18:
                aadhar_front = page.images[0].as_pil()
                j += 1
            if j == 1 and i == 18:
                aadhar_back = page.images[1].as_pil()
                j += 1
            if j == 2 and i == 19:
                pan = page.images[0].as_pil()
                j = j + 1
            if j == 3 and i == 19:
                selfie = page.images[1].as_pil()
                j += 1
    else:
        page = doc.get_page(d - 1)
        if j == 0:
            pan = page.images[0].as_pil()
            j += 1
        if j == 1:
            selfie = page.images[1].as_pil()
            j += 1
    # test case
    if aadhar_front and aadhar_back and pan and selfie:
        print("Extracting images")


def main():
    # needed to be changed if you want to get data from different location
    pdfs_path = os.getcwd() + '/data/'
    test_counter = 0
    # listing pdfs in pdfs_path
    for pdf in os.listdir(pdfs_path):
        file = pdfs_path + '/' + pdf
        # using pdfinfo command to get the no.of pages in the pdf
        cmd = "pdfinfo '%s' | grep 'Pages' | awk '{print $2}'" % file
        # calling exract_images with complete pdf path and the no.of pages
        extract_images(file, int(os.popen(cmd).read().strip()))
        if test_counter == 5:
            break
        test_counter += 1

# Testing function
if __name__ == '__main__':
    main()
