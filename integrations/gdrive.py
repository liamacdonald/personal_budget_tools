import io
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account




def get_gdrive_service():
    # Get the JSON string from the GitHub Secret
    service_account_info = json.loads(os.getenv('GOOGLE_DRIVE_CREDENTIALS'))
    creds = service_account.Credentials.from_service_account_info(service_account_info)

    service = build('drive', 'v3', credentials=creds)
    
    return service


def get_list_of_files_from_gdrive_folder(service , folder_id: str):

    query = f"'{folder_id}' in parents and mimeType = 'text/csv' and trashed = false"
    files = []
    page_token = None
    
    while True:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType)',
            pageToken=page_token
        ).execute()
        
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    
    return files

def download_csv(file_id):
    
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    
    # 3. Stream the download
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    # 4. Load into Pandas
    file_stream.seek(0)
    df = pd.read_csv(file_stream)
    return df


service = get_gdrive_service()
files = get_list_of_files_from_gdrive_folder(service=service, folder_id = '1vvCabAbrqoTc4Mz5m-msZUE4ZJn7Jycd')

df = pd.concat([download_csv(file['id']) for file in files], axis = 0)
print(df.head())