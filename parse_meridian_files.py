import csv
from pathlib import Path

def parse_meridian_csv(file_path: Path):
    """
    """
    parsed_records = []
    with open(file_path , mode = 'r') as file:
        raw_records = csv.DictReader(file)
        for raw_record in raw_records:
            parsed_record = {
                'account_id' : raw_record['Account Number'].strip()[3:] ,
                'transaction_date' : raw_record['Trans Date'].strip() ,
                'posting_date' : raw_record['Posting Date'].strip() ,
                'type' : raw_record['Type'].strip() ,
                'category' : raw_record['Category'].strip(),
                'merchant' : raw_record['Merchant Name'].strip() ,
                'merchant_city' : raw_record['Merchant City'].strip() ,
                'merchant_province' : raw_record['Merchant State'].strip() ,
                'amount' : raw_record['Amount'].strip().replace('$','') ,
                'reference_number' : raw_record['Reference Number'].strip().replace('backslasht') ,
                'transaction_type' : raw_record['Tran Type'].strip() ,
                'mcc_code' : raw_record['MCC Code'].strip() ,
                'mcc_description' : raw_record['MCC Description'].strip()                                                                                    
            }
            parsed_records.append(parsed_record)


parse_meridian_csv(Path('meridian_2025_feb.csv'))

