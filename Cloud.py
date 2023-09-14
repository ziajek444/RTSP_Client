'''
API for checking space on cloud drive (like google drive).
API for pushing files into cloud drive.
Idea:
    Thread working at every n minutes and checking if there are any files to push
reqs:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
'''

import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from FileManagement import extract_file_name_from_path, extract_base_path_from_path, dir_exists, remove_dir
from simple_logs import log_error, log_debug, log_info, log_critical

TO_CONSOLE = True       # Default False


def upload_files(_files: list, _cloud_dir_id: str, _CLIENT_SECRETS='client_secret_I-D.apps.googleusercontent.com.json'):
    log_debug("start upload_files", to_console=TO_CONSOLE)
    upload_dir = extract_base_path_from_path(_files[0])
    files_to_upload = [extract_file_name_from_path(path) for path in _files]

    # OAuth 2.0 scope that will be authorized.
    # Check https://developers.google.com/drive/scopes for all available scopes.
    OAUTH2_SCOPE = ['https://www.googleapis.com/auth/drive']

    # Location of the client secrets.
    CLIENT_SECRETS = _CLIENT_SECRETS
    TOKEN = "token.json"
    creeds = None

    if not os.path.exists(CLIENT_SECRETS):
        log_critical("missing credentials", to_console=TO_CONSOLE)
        exit(-1)

    if os.path.exists(TOKEN):
        creeds = Credentials.from_authorized_user_file(TOKEN, OAUTH2_SCOPE)

    files_name = list()
    for file_to_upload in files_to_upload:
        if not creeds or not creeds.valid:
            if creeds and creeds.expired and creeds.refresh_token:
                creeds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS, OAUTH2_SCOPE)
                creeds = flow.run_local_server(port=0)
            with open(TOKEN, 'w') as token_file:
                token_file.write(creeds.to_json())
        try:
            service = build("drive", "v3", credentials=creeds)
            koty_folder_id = _cloud_dir_id
            response = service.files().list(
                q=f"mimeType='application/x-7z-compressed' and parents in '{koty_folder_id}'").execute()
            file_data = response['files']
            files_name = [obj["name"] for obj in file_data]

            if file_to_upload not in files_name:
                file_metadata = {
                    "name": file_to_upload,
                    "parents": [koty_folder_id],
                    'kind': 'drive#file'
                }
                full_path = os.path.join(upload_dir, file_to_upload)
                media = MediaFileUpload(full_path,
                                        mimetype='application/x-7z-compressed')
                file = service.files().create(body=file_metadata, media_body=media,
                                              fields='id').execute()
                log_debug(F'File ID: {file.get("id")}', to_console=TO_CONSOLE)
        except HttpError as http_err:
            log_error(http_err, to_console=TO_CONSOLE)
        except Exception as err:
            log_error(err, to_console=TO_CONSOLE)
        finally:
            pass
    log_info("done upload_files", to_console=TO_CONSOLE)

    # check if files exists on drive and rm from local
    response = service.files().list(
        q=f"mimeType='application/x-7z-compressed' and parents in '{koty_folder_id}'").execute()
    file_data = response['files']
    files_name = [obj["name"] for obj in file_data]
    just_uploaded_files = [extract_file_name_from_path(file_path) for file_path in _files]
    for file_from_cloud in files_name:
        if file_from_cloud in just_uploaded_files:
            just_uploaded_files.remove(file_from_cloud)
            log_debug(f"Remove file: {file_from_cloud} if existing")
            if dir_exists(os.path.join(upload_dir, file_from_cloud)):
                log_debug(f"Removing {file_from_cloud}...")
                remove_dir(os.path.join(upload_dir, file_from_cloud))
            if not dir_exists(os.path.join(upload_dir, file_from_cloud)):
                log_debug(f"File {file_from_cloud} removed !")

    log_info("done remove local files", to_console=TO_CONSOLE)
