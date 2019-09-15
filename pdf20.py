import time
import os
from tabula import read_pdf
import re
import requests
url = "https://api.postalpincode.in/pincode/"


# Libraries that can be used are tabula, PyPdf2 (not efficient), Camelot

def location_info(df):
    a = b = c = d = w = x = y = z = ''

    # find address
    correct_dict = {
        'l': '1',
        'I': '1',
        'i': '1',
        'B': '8',
        'o': '0',
        'O': '0'
    }
    a = df[0]['data'][14][1]['text'] + df[0]['data'][15][1]['text'] + \
        df[0]['data'][16][1]['text'] + df[0]['data'][17][1]['text']

    # extracting pincode; if not work change to regexp code
    b = a[-6:]

    # extracting city and state from pincode (api : postalpincode.in)
    try:
        loc = requests.get(url=url + b).json()[0]['PostOffice'][0]
        c, d = loc['District'], loc['State']

    except KeyError:
        if b == '':
            pass
        elif b:
            for c in b:
                if c in correct_dict:
                    b = b.replace(c, correct_dict[c])
            loc = requests.get(url=url + b).json()[0]['PostOffice'][0]
            c, d = loc['District'], loc['State']
        else:
            pass
    except TypeError:
        print("403 Forbidden - {}".format(b))

    # find current_address
    w = df[0]['data'][18][1]['text'] + df[0]['data'][19][1]['text'] + \
        df[0]['data'][20][1]['text'] + df[0]['data'][21][1]['text']

    x = re.findall(r'\d\d\d\d\d\d', w)
    x = ''.join(x)
    try:
        loc = requests.get(url=url + x).json()[0]['PostOffice'][0]
        y, z = loc['District'], loc['State']
    except KeyError:
        pass
    except TypeError:
        print("403 Forbidden - {}".format(b))

    return a, b, c, d, w, x, y, z


def page_1_2(file):
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
            address, pincode, city, state, current_address, curr_pin_code, curr_city, curr_state = \
                location_info(df)
            phone_number = df[0]['data'][22][1]['text']
            email = df[0]['data'][23][1]['text']
            bank = df[0]['data'][24][1]['text']
            account_number = df[0]['data'][25][1]['text']
            ifsc = df[0]['data'][26][1]['text']
            name_related_person = df[0]['data'][27][1]['text']
            phone_related_person = df[0]['data'][28][1]['text']

            print("Extracting from page 1")

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
            if a != 'Onboarding Fees:':
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

            print("Extracting from page 2")


def page_16_17(file):
    for i in [16, 17]:
        if i == 16:
            df = read_pdf(file, output_format="json", pages=i)
            bank = df[0]['data'][1][1]['text']
            account_number = df[0]['data'][3][1]['text']
            ifsc = df[0]['data'][5][1]['text']
            bank_account_type = df[0]['data'][4][1]['text']
            micr = df[0]['data'][6][1]['text']
            print(bank, account_number, ifsc, bank_account_type, micr)

        elif i == 17:
            df = read_pdf(file, output_format="json", pages=i)
            facility = df[0]['data'][1][1]['text']
            facility_type = df[0]['data'][2][1]['text']
            max_sanctioned = df[0]['data'][3][1]['text']
            purpose = df[0]['data'][4][1]['text']
            tenure = df[0]['data'][5][1]['text']
            emi_amount = df[0]['data'][7][1]['text']
            repayment = df[0]['data'][8][1]['text']
            risk_category = df[0]['data'][9][1]['text']
            print(facility, facility_type, max_sanctioned, purpose, tenure, emi_amount, repayment, risk_category)

# if __name__ == '__main__':
    # main()
    # ts = time.time()
    # pdfs_path = os.getcwd() + '/data/'
    # tables = list()
    # counter = 0
    # for pdf in os.listdir(pdfs_path):
    #     print("processing {}".format(pdf))
    #     page1(pdfs_path + pdf)
    #     page_16_17(pdfs_path + pdf)

    #
    # for table in tables:
    #     print(table)
    #
    # print("Time taken : {}".format(time.time() - ts))
    # page1('data/20181001020401DID180830220312478I8UMKI2KX3QDMD_esign.pdf')
    # df = read_pdf('data/20181001020423DID180831121005497TQKOIQ4OCNTX42_esign', output_format='json', pages=16)
    # loc = requests.get(url=url + '584121').json()[0]['PostOffice'][0]
    # page_16_17('data/20181001020423DID180831121005497TQKOIQ4OCNTX42_esign.pdf')
    # print(loc)
