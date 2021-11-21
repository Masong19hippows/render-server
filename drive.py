import pickle
import io
import os
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

 
# Defines scopes used in the drive api
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
mydir = os.path.dirname(__file__)

if os.path.exists(mydir + '/creds/token.pickle'):
    with open(mydir + '/creds/token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(mydir + '/creds/credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(mydir + '/creds/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)


# Gets the newly updated folder form google drive
def get_folders():
    # Call the Drive v3 API
    results = service.files().list(q="('1YbpTyVhZgKofR2j9AqFmq55p1poyUtBn' in parents)" + "and" + "(mimeType='application/vnd.google-apps.folder')",
    fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


# Downloads the uploaded folder from google drive to render it
def download(dir, id):

    items = service.files().list(q=f"('{id}' in parents)" + "and" + "trashed=false", fields="nextPageToken, files(name, id, mimeType)").execute().get("files", [])
    for item in items:
        if item['mimeType'] == "application/vnd.google-apps.folder":
            new_dir = os.path.join(dir, item['name'])
            os.system(f"mkdir -p {new_dir}")
            download(new_dir, item['id'])

        else:
            request = service.files().get_media(fileId=item['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                with open(dir+"/"+item['name'], 'wb') as f:
                    shutil.copyfileobj(fh, f)
                    print("Download %d%%." % int(status.progress() * 100))


# Uploads a directory to google drive
def upload(dir, folder_id):
    # Creating the first directory to put files in
    file_metadata = {
                'name': [os.path.basename(os.path.normpath(dir))],
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
                }
    folder_id = service.files().create(body=file_metadata, fields='id').execute().get('id')

    # Looping though the local files and directories while uploading contents to google dirve folder
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isdir(os.path.join(dir, file)):     
            file_metadata = {
                'name': [file],
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
                }
            file = service.files().create(body=file_metadata, fields='id').execute()
            upload(path, file.get('id'))
        else:
            file_metadata = {
                'name': [file],
                'parents': [folder_id]
                }
            media = MediaFileUpload(path, resumable=True)
            service.files().create(body=file_metadata, media_body=media,fields='id').execute()