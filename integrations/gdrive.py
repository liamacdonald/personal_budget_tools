import io
import pandas as pd
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import os
import json
from google.oauth2 import service_account




def get_gdrive_service():
    # Get the JSON string from the GitHub Secret
    service_account_info = json.loads(os.getenv('GOOGLE_DRIVE_CREDENTIALS'))
    breakpoint()
    creds = service_account.Credentials.from_service_account_info(service_account_info)

    build('drive', 'v3', credentials=creds)
    service = get_gdrive_service()
    return service


def download_csv(file_id):
    
    
    # 2. Create the request
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

# Usage

service = get_gdrive_service()
results = (
    service.files()
    .list(pageSize=10, fields="nextPageToken, files(id, name)")
    .execute()
)
items = results.get("files", [])
print(items)
