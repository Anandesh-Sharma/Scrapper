import os
import re
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from tabula import read_pdf
import minecart
import PyPDF2
import requests
# import cv2
from IPython.display import Image, display
from PIL import Image

url = "https://api.postalpincode.in/pincode/"


# for extracting images
# file , d is length of file
def extract(file, d):
    j = 0
    adhar_front = ''
    adhar_back = ''
    pan = ''
    selfie = ''
    pdffile = open(file, 'rb')
    doc = minecart.Document(pdffile)
    global k
    if (d > 19):
        for i in range(d - 2, d):
            page = doc.get_page(i)
            if (j == 0 and i == 18):
                adhar_front = page.images[0].as_pil()
                j += 1
            if (j == 1 and i == 18):
                adhar_back = page.images[1].as_pil()
                j += 1
            if (j == 2 and i == 19):
                pan = page.images[0].as_pil()
                j = j + 1
            if (j == 3 and i == 19):
                selfie = page.images[1].as_pil()
                j += 1
    else:
        page = doc.get_page(d - 1)
        if (j == 0):
            pan = page.images[0].as_pil()
            j += 1
        if (j == 1):
            selfie = page.images[1].as_pil()
            j += 1
    return adhar_front, adhar_back, pan, selfie


# for variation in pdf page 2
def pagedata1(file):
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(1)
    k = pageObj.extractText()
    data1 = k.find('Permanent Address') + 17
    data12 = k.find('City')
    data2 = k.find("Pincode")
    data3 = k.find("Occupation Type") + 15
    data4 = k.find("Proof of Identity")
    data5 = k.find("Proof of Address")
    data13 = k.find("Name of Business")
    data6 = k.find("Monthly Income")
    data7 = k.find("Bank Details")
    data8 = k.find("Name of the Bank")
    data9 = k.find("Account Number")
    data15 = k.find("Account Holder Name")
    data10 = k.find("IFSC Code")
    data11 = k.find("MICR Code")
    data14 = k.find("Customer's Undertaking1")
    pincode = k[data2 + 7:data2 + 13]
    address = k[data1:data12]
    occupation = k[data3:data4]
    proof_of_identity = k[data4 + 17:data5]
    proof_of_address = k[data5 + 16:data13]
    monthly_income = k[data6 + 14:data7]
    bank = k[data8 + 16:data9]
    account_number = k[data9 + 14:data15]
    ifsc = k[data10 + 9:data11]
    micr = k[data11 + 9:data14]
    pdfFileObj.close()
    return address, occupation, pincode, proof_of_identity, proof_of_address, monthly_income, bank, ifsc, micr, account_number


# for extractinng city and state from 16 page pdf
def pagedata(file):
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(1)
    k = pageObj.extractText()
    t = k[20:]
    data17 = t.find('State')
    data16 = t.find('Country')
    data12 = k.find('City')
    data2 = k.find("Pincode")
    city = k[data12 + 4:data2]
    state = t[data17 + 5:data16]
    pdfFileObj.close()
    return city, state


# repayment date calculation
def a_r_date(file, tenure, size):
    tenure = int(tenure)
    dateFormat = "%Y-%m-%d"
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if size > 16:
        pageObj = pdfReader.getPage(16)
    else:
        pageObj = pdfReader.getPage(13)
    k = pageObj.extractText()
    data1 = k.find('application form dated ') + 23
    date = k[data1:data1 + 11]
    date = date.strftime(dateFormat)
    enddate = pd.to_datetime(date) + pd.DateOffset(days=tenure)

    r = enddate.strftime(dateFormat)

    return date, r


# main function for scrapping and calling other
def info(file, size, add):
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

    
    if size > 15:

        for i in [1, 2]:

            if i == 1:
                df = read_pdf(file, output_format="json", pages=i)
                account_type = df[0]['data'][0][1]['text']
                name = df[0]['data'][1][1]['text']
                father_name = df[0]['data'][2][1]['text']
                mother_name = df[0]['data'][3][1]['text']
                date_of_birth = df[0]['data'][4][1]['text']
                gender = df[0]['data'][5][1]['text']
                marital_status = df[0]['data'][6][1]['text']
                occupation = df[0]['data'][7][1]['text']
                nationality = df[0]['data'][8][1]['text']
                resident_status = df[0]['data'][9][1]['text']
                proof_of_identity = df[0]['data'][10][1]['text']
                pan = df[0]['data'][11][1]['text']
                proof_of_address = df[0]['data'][12][1]['text']
                address_type = df[0]['data'][13][1]['text']
                if add:
                    address = df[0]['data'][14][1]['text'] + df[0]['data'][15][1]['text'] + df[0]['data'][16][1][
                        'text'] + df[0]['data'][17][1]['text']
                else:
                    address = df[0]['data'][14][1]['text'] + ' ' + df[0]['data'][15][1]['text'] + ' ' + \
                              df[0]['data'][16][1]['text'] + " " + df[0]['data'][17][1]['text']
                # pincode=df[0]['data'][15][1]['text']
                pin_code = re.findall('\\b\\d+\\b', address)[-1]
                loc_inf = requests.get(url=url + pin_code).json()[0]['PostOffice'][0]
                city, state = loc_inf['District'], loc_inf['State']
                # address = df[0]['data'][14][1]['text']+" "+city+" "+state+" "+pin_code
                current_address = df[0]['data'][18][1]['text'] + " " + df[0]['data'][19][1]['text'] + " " + \
                                  df[0]['data'][20][1]['text'] + " " + df[0]['data'][21][1]['text']

                curr_pin_code = re.findall('\\b\\d+\\b', current_address)[-1]
                loc_inf = requests.get(url=url + curr_pin_code).json()[0]['PostOffice'][0]
                curr_city, curr_state = loc_inf['District'], loc_inf['State']
                phone_number = df[0]['data'][22][1]['text']
                email = df[0]['data'][23][1]['text']
                bank = df[0]['data'][24][1]['text']
                account_number = df[0]['data'][25][1]['text']
                ifsc = df[0]['data'][26][1]['text']
                name_related_person = df[0]['data'][27][1]['text']
                phone_related_person = df[0]['data'][28][1]['text']

            elif i == 2:
                df = read_pdf(file, output_format="json", pages=i)
                # loan info page2
                loan_id = df[0]['data'][1][2]['text']
                prospect_no = df[0]['data'][3][2]['text']
                lender = "Krazybee Sevice pvt. Ltd."
                platform = df[1]['data'][2][1]['text']
                loan_amount = df[1]['data'][3][1]['text']
                interest_rate = df[1]['data'][4][1]['text']
                loan_purpose = df[1]['data'][5][1]['text']
                fees = df[1]['data'][6][1]['text']
                processing_fees = df[1]['data'][7][1]['text']
                a = df[1]['data'][8][0]['text']
                if (a != 'Onboarding Fees:'):
                    service_charges = df[1]['data'][8][1]['text']
                    full_prepayment_charges = df[1]['data'][9][1]['text']
                    part_prepayment_charges = df[1]['data'][10][1]['text']
                    default_charges = df[1]['data'][11][1]['text']
                    nach_dishonor = df[1]['data'][15][1]['text']
                else:
                    onboarding_fees = df[1]['data'][8][1]['text']
                    service_charges = df[1]['data'][9][1]['text']
                    full_prepayment_charges = df[1]['data'][10][1]['text']
                    part_prepayment_charges = df[1]['data'][11][1]['text']
                    default_charges = df[1]['data'][12][1]['text']
                    nach_dishonor = df[1]['data'][16][1]['text']

            if size > 16:
                if i == 16:
                    df = read_pdf(file, output_format="json", pages=i)
                    # bank detail page 16
                    bank = df[0]['data'][1][1]['text']
                    account_number = df[0]['data'][3][1]['text']
                    ifsc = df[0]['data'][5][1]['text']
                    bank_account_type = df[0]['data'][4][1]['text']
                    micr = df[0]['data'][6][1]['text']

                if i == 17:
                    # page17
                    df = read_pdf(file, output_format="json", pages=i)
                    facility = df[0]['data'][1][1]['text']
                    facility_type = df[0]['data'][2][1]['text']
                    max_sanctioned = df[0]['data'][3][1]['text']
                    purpose = df[0]['data'][4][1]['text']
                    tenure = df[0]['data'][5][1]['text']
                    emi_amount = df[0]['data'][7][1]['text']
                    repayment = df[0]['data'][8][1]['text']
                    risk_category = df[0]['data'][9][1]['text']

                    k = re.findall('\\b\\d+\\b', tenure)[-1]
                    # print(k)
                    application_date, repayment_date = a_r_date(file, k, size)
            else:
                df = read_pdf(file, output_format="json", pages=14)
                lender = "Krazybee Sevice pvt. Ltd.1"
                facility = df[0]['data'][1][1]['text']
                max_sanctioned = df[0]['data'][2][1]['text']
                purpose = df[0]['data'][3][1]['text']
                tenure = df[0]['data'][4][1]['text']
                emi_amount = df[0]['data'][6][1]['text']
                repayment = df[0]['data'][7][1]['text']
                risk_category = df[0]['data'][8][1]['text']
                k = re.findall('\\b\\d+\\b', tenure)[-1]
                application_date, repayment_date = a_r_date(file, k, size)

            c = {'account_type': account_type,
                 'name': name,
                 'father_name': father_name,
                 'mother_name': mother_name,
                 'date_of_birth': date_of_birth,
                 'gender': gender,
                 'marital_status': marital_status,
                 'occupation': occupation,
                 'nationality': nationality,
                 'resident_status': resident_status,
                 'proof_of_identity': proof_of_identity,
                 'pan': pan,
                 'proof_of_address': proof_of_address,
                 'address_type': address_type,
                 'address': address,
                 'pin_code': pin_code,
                 'city': city,
                 'state': state,
                 'current_address': current_address,
                 'curr_pin_code': curr_pin_code,
                 'curr_city': curr_city,
                 'curr_state': curr_state,
                 'phone_number': phone_number,
                 'email': email,
                 'name_related_person': name_related_person,
                 'phone_related_person': phone_related_person,
                 'loan_id': loan_id,
                 'prospect_no': prospect_no,
                 'lender': lender,
                 'platform': platform,
                 'loan_amount': loan_amount,
                 'interest_rate': interest_rate,
                 'loan_purpose': loan_purpose,
                 'fees': fees,
                 'processing_fees': processing_fees,
                 'onboarding_fees': onboarding_fees,
                 'service_charges': service_charges,
                 'full_prepayment_charges': full_prepayment_charges,
                 'part_prepayment_charges': part_prepayment_charges,
                 'default_charges': default_charges,
                 'nach_dishonor': nach_dishonor,
                 'facility': facility,
                 'facility_type': facility_type,
                 'max_sanctioned': max_sanctioned,
                 'purpose': purpose,
                 'emi_amount': emi_amount,
                 'repayment': repayment,
                 'risk_category': risk_category,
                 'tenure': tenure,
                 'bank': bank,
                 'account_number': account_number,
                 'ifsc': ifsc,
                 'bank_account_type': bank_account_type,
                 'micr': micr,
                 'monthly_income': monthly_income,
                 'Kreditbee_ID': Kreditbee_ID,
                 'date_of_application': application_date,
                 'repayment_date': repayment_date

                 }
    if size == 8:

        for i in [1, 2, 6]:
            df = read_pdf(file, output_format="json", pages=i)
            if i == 1:
                dateFormat = "%Y-%m-%d"
                name = df[0]['data'][0][1]['text']
                interest_rate = df[0]['data'][2][1]['text']
                tenure = df[0]['data'][3][1]['text']
                loan_amount = df[0]['data'][4][1]['text']
                loan_id = df[0]['data'][5][1]['text']
                applicationdate = df[1]['data'][0][1]['text']
                end = pd.to_datetime(applicationdate) + pd.DateOffset(days=int(tenure))
                application_date = applicationdate.replace("/ ", "-")
                application_date = application_date.split("-")
                application_date = application_date[2] + "-" + application_date[1] + "-" + application_date[0]
                repayment_date = end.strftime(dateFormat)
                lead_id = df[1]['data'][1][1]['text']
                purpose = df[1]['data'][5][1]['text']
                Kreditbee_ID = df[1]['data'][6][1]['text']
                father_name = df[2]['data'][1][1]['text']
                mother_name = df[2]['data'][2][1]['text']
                nationality = df[2]['data'][3][1]['text']
                date_ofbirth = df[2]['data'][4][1]['text']
                date_of_birth = date_ofbirth.replace("/ ", "-")
                date_of_birth = date_of_birth.split("-")
                date_of_birth = date_of_birth[2] + "-" + date_of_birth[1] + "-" + date_of_birth[0]
                gender = df[2]['data'][5][1]['text']
                phone_number = df[2]['data'][6][1]['text']
                email = df[2]['data'][7][1]['text']
                pan = df[2]['data'][8][1]['text']
                print(len(pan))
                current_address = df[2]['data'][9][1]['text']
                curr_pin_code = df[2]['data'][10][3]['text']
                try:
                    loc_inf = requests.get(url=url + curr_pin_code).json()[0]['PostOffice'][0]
                    curr_city, curr_state = loc_inf['District'], loc_inf['State']
                except NoneType:
                    curr_city = df[2]['data'][10][1]['text']
                    curr_state = df[2]['data'][10][3]['text']
            elif i == 2:
                # page2
                lender = "Fullerton"
                address, occupation, pin_code, proof_of_identity, proof_of_address, monthly_income, bank, ifsc, micr, account_number = pagedata1(
                    file)

                try:

                    loc_inf = requests.get(url=url + pin_code).json()[0]['PostOffice'][0]
                    city, state = loc_inf['District'], loc_inf['State']
                except:  # NoneType Error:
                    city, state = pagedata(file)

            else:
                # page6

                max_sanctioned = df[0]['data'][2][1]['text']
                processing_fees = df[0]['data'][6][1]['text']
                emi_amount = df[0]['data'][7][1]['text']
            c = {'account_type': account_type,
                 'name': name,
                 'father_name': father_name,
                 'mother_name': mother_name,
                 'date_of_birth': date_of_birth,
                 'gender': gender,
                 'marital_status': marital_status,
                 'occupation': occupation,
                 'nationality': nationality,
                 'resident_status': resident_status,
                 'proof_of_identity': proof_of_identity,
                 'pan': pan,
                 'proof_of_address': proof_of_address,
                 'address_type': address_type,
                 'address': address,
                 'pin_code': pin_code,
                 'city': city,
                 'state': state,
                 'current_address': current_address,
                 'curr_pin_code': curr_pin_code,
                 'curr_city': curr_city,
                 'curr_state': curr_state,
                 'phone_number': phone_number,
                 'email': email,
                 'name_related_person': name_related_person,
                 'phone_related_person': phone_related_person,
                 'loan_id': loan_id,
                 'prospect_no': prospect_no,
                 'lender': lender,
                 'platform': platform,
                 'loan_amount': loan_amount,
                 'interest_rate': interest_rate,
                 'loan_purpose': loan_purpose,
                 'fees': fees,
                 'processing_fees': processing_fees,
                 'service_charges': service_charges,
                 'full_prepayment_charges': full_prepayment_charges,
                 'part_prepayment_charges': part_prepayment_charges,
                 'default_charges': default_charges,
                 'nach_dishonor': nach_dishonor,
                 'facility': facility,
                 'facility_type': facility_type,
                 'max_sanctioned': max_sanctioned,
                 'purpose': purpose,
                 'emi_amount': emi_amount,
                 'repayment': repayment,
                 'risk_category': risk_category,
                 'bank': bank,
                 'tenure': tenure,
                 'account_number': account_number,
                 'ifsc': ifsc,
                 'bank_account_type': bank_account_type,
                 'micr': micr,
                 'monthly_income': monthly_income,
                 'Kreditbee_ID': Kreditbee_ID,
                 'date_of_application': application_date,

                 'date_of_repayment': repayment_date
                 }

    return c


k = 0
directory = '/home/credicxo/Desktop/8 page/'
for filename in os.listdir(directory):
    # print(filename)

    if filename.endswith('.pdf'):
        pdfFileObj = open(directory + filename, 'rb')
    try:

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        j = pdfReader.numPages
        information = info(directory + filename, j, 0)
        print(information)
        adhar_front, adhar_back, pan, selfie = extract(directory + filename, j)
        image = {'adhar_front': adhar_front, 'adhar_back': adhar_back, 'pani': pan, 'selfie': selfie}
        information.update(image)
        a = requests.post(url='http://94.176.237.27:4000/api/update_information', data=information)
        print(a)
        break
    except TypeError:
        # print(filename)
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        j = pdfReader.numPages
        # filename=str(filename)+str(\\)
        information = info(directory + filename, j, True)
        print(information)
        adhar_front, adhar_back, pani, selfie = extract(directory + filename, j)
        image = {'adhar_front': adhar_front, 'adhar_back': adhar_back, 'pani': pan, 'selfie': selfie}
        information.update(image)
        requests.post(url='http://94.176.237.27:4000/api/update_information', data=information)
        print("req1")
    except OSError:
        pass
    except PyPDF2.utils.PdfReadError:

        pass
