import functions_framework
import csv
from pathlib import Path
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd


def parse_meridian_csv_to_list_of_dicts(file_path: Path):
    """
    Parses a Meridian CSV file and returns a list of dictionaries.
    """
    parsed_records = []
    with open(file_path, mode='r') as file:
        # The user provided headers with tabs, so we assume a tab-separated file.
        raw_records = csv.DictReader(file, delimiter='\t')
        for raw_record in raw_records:
            try:
                parsed_record = {
                    'account_number': raw_record['Account Number'].strip(),
                    'cardholder_name': raw_record['Cardholder Name'].strip(),
                    'transaction_date': raw_record['Trans Date'].strip(),
                    'posting_date': raw_record['Posting Date'].strip(),
                    'transaction_type': raw_record['Type'].strip(),
                    'category': raw_record['Category'].strip(),
                    'merchant_name': raw_record['Merchant Name'].strip(),
                    'amount': raw_record['Amount'].strip().replace('$', ''),
                    'reference_number': int(raw_record['Reference Number'].strip()),
                    'mcc_code': int(raw_record['MCC Code'].strip()),
                    'mcc_description': raw_record['MCC Description'].strip()
                }
                parsed_records.append(parsed_record)
            except (KeyError, ValueError) as e:
                print(f"Skipping row due to error: {e}. Row: {raw_record}")

    return parsed_records

def parse_meridian_csv_to_df(file_path: Path):
    """
    Parses a Meridian CSV file and returns a list of dataframe with parsed column names
    """

    # with open(file_path, mode='r') as file:
    # The user provided headers with tabs, so we assume a tab-separated file.
    df = pd.read_csv(file_path , sep='\t')
    df.rename({
                'Account Number' : 'account_number', 
                'Cardholder Name' : 'cardholder_name',
                'Trans Date' : 'transaction_date',
                'Posting Date' : 'posting_date',
                'Type' : 'transaction_type',
                'Category' : 'category',
                'Merchant Name' : 'merchant_name',
                'Amount' : 'amount' ,
                'Reference Number' : 'reference_number' ,
                'MCC Code' : 'mcc_code' ,
                'MCC Description' : 'mcc_description'
            } ,
        inplace=True
    )

    return df


def write_to_bigquery(data, table_id):
    """
    Writes data to a BigQuery table.
    """
    client = bigquery.Client()
    errors = client.insert_rows_json(table_id, data)
    if errors == []:
        print("New rows have been added.")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

def write_csv_with_all_transactions(transaction_list: list[dict] , csv_path: Path):
     google-api-python-client

