import minecart
from PIL import Image
from tabula import read_pdf
import requests
import re
import os

url = "https://api.postalpincode.in/pincode/"

# Extracts images from the pdf
# targeting last 2 pages the pdf if file is of 20 pages
# else pictures must be in the last image


def extract_images(file, d):
    j = 0
    adhar_front = ""
    adhar_back = ""
    pan = ""
    selfie = ""
    pdffile = open(file, "rb")
    doc = minecart.Document(pdffile)

    if d > 19:
        for i in range(d - 2, d):
            page = doc.get_page(i)
            if j == 0 and i == 18:
                adhar_front = page.images[0].as_pil()
                j += 1
            if j == 1 and i == 18:
                adhar_back = page.images[1].as_pil()
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
    return adhar_front, adhar_back, pan, selfie


def fun(file):

    account_type, name, father_name, mother_name, date_of_birth = '', '', '', '', ''
    gender, marital_status, occupation, nationality = '', '', '', ''
    resident_status, proof_of_identity, pan, proof_of_address = '', '', '', ''
    address_type, address, pin_code, city, state, current_address = '', '', '', '', '', ''
    curr_pin_code, curr_city, curr_state, phone_number, email = '', '', '', '', ''
    name_related_person, phone_related_person, loan_id = '', '', ''
    prospect_no, lender, platform, loan_amount, interest_rate = '', '', '', '', ''
    loan_purpose, fees, processing_fees, onboarding_fees = '', '', '', ''
    service_charges, full_prepayment_charges, part_prepayment_charges = '', '', ''
    default_charges, nach_dishonor, facility, facility_type = '', '', '', ''
    max_sanctioned, purpose, date_of_repayment = '', '', ''
    emi_amount, repayment, risk_category, bank = '', '', '', ''
    account_number, ifsc, bank_account_type, micr = '', '', '', ''
    Kreditbee_ID, monthly_income, tenure = '', '', ''
    application_date = ''

    for i in [1, 2]:
    # for the tables on page 1 and two of the agreement
        if i == 1:
            df = read_pdf(file, output_format="json", pages=i, encoding='utf-8')
            # print(df)
            account_type = df[0]["data"][0][1]["text"]
            name = df[0]["data"][1][1]["text"]
            father_name = df[0]["data"][2][1]["text"]
            mother_name = df[0]["data"][3][1]["text"]
            date_of_birth = df[0]["data"][4][1]["text"]
            gender = df[0]["data"][5][1]["text"]
            marital_status = df[0]["data"][6][1]["text"]
            occupation = df[0]["data"][7][1]["text"]
            nationality = df[0]["data"][8][1]["text"]
            resident_status = df[0]["data"][9][1]["text"]
            proof_of_identity = df[0]["data"][10][1]["text"]
            pan = df[0]["data"][11][1]["text"]
            proof_of_address = df[0]["data"][12][1]["text"]
            address_type = df[0]["data"][13][1]["text"]
            # print(address_type)
            if address_type:
                address = df[0]['data'][14][1]['text'] + df[0]['data'][15][1]['text'] + df[0]['data'][16][1][
                        'text'] + df[0]['data'][17][1]['text']
            # Extracting pincode from address and making api call to find out
            pin_code = address[-6:]
            print(pin_code)

            loc_inf = requests.get(url=url + str(pin_code)).json()[0]["PostOffice"][0]
            city, state = loc_inf["District"], loc_inf["State"]

            if address_type == "PERMANENT":
                current_address = address
                # print("Address is pemanent")
            else:
                current_address = df[0]['data'][18][1]['text'] + df[0]['data'][19][1]['text'] + \
                                  df[0]['data'][20][1]['text'] + df[0]['data'][21][1]['text']
                current_address = str(current_address)

            curr_pin_code = current_address[-6:]
            print(curr_pin_code)

            loc_inf = requests.get(url=url + str(curr_pin_code)).json()[0]["PostOffice"][0]
            curr_city, curr_state = loc_inf["District"], loc_inf["State"]
            phone_number = df[0]["data"][22][1]["text"]
            email = df[0]["data"][23][1]["text"]
            bank = df[0]["data"][24][1]["text"]
            account_number = df[0]["data"][25][1]["text"]
            ifsc = df[0]["data"][26][1]["text"]
            name_related_person = df[0]["data"][27][1]["text"]
            phone_related_person = df[0]["data"][28][1]["text"]

        elif i == 2:
            df = read_pdf(file, output_format="json", encoding='utf-8', pages=i)
            loan_id = df[0]["data"][1][2]["text"]
            prospect_no = df[0]["data"][3][2]["text"]
            lender = "Krazybee Sevice pvt. Ltd."
            platform = df[1]["data"][2][1]["text"]
            loan_amount = df[1]["data"][3][1]["text"]
            interest_rate = df[1]["data"][4][1]["text"]
            loan_purpose = df[1]["data"][5][1]["text"]
            fees = df[1]["data"][6][1]["text"]
            processing_fees = df[1]["data"][7][1]["text"]
            a = df[1]["data"][8][0]["text"]
            if a != "Onboarding Fees:":
                service_charges = df[1]["data"][8][1]["text"]
                full_prepayment_charges = df[1]["data"][9][1]["text"]
                part_prepayment_charges = df[1]["data"][10][1]["text"]
                default_charges = df[1]["data"][11][1]["text"]
                nach_dishonor = df[1]["data"][15][1]["text"]
            else:
                onboarding_fees = df[1]["data"][8][1]["text"]
                service_charges = df[1]["data"][9][1]["text"]
                full_prepayment_charges = df[1]["data"][10][1]["text"]
                part_prepayment_charges = df[1]["data"][11][1]["text"]
                default_charges = df[1]["data"][12][1]["text"]
                nach_dishonor = df[1]["data"][16][1]["text"]
            
            print(file)
            print(address )
            
            


mypath = "/home/mr-robot/Desktop/Scrapper/data/"

for pdf in os.listdir(mypath):
    fun(mypath + pdf)
    

