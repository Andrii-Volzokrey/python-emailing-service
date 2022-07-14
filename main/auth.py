import os
import pickle

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from settings import CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES


def create_service():
    workdir = os.getcwd()
    token_dir = 'tokens'
    pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'
    client_secret_file = os.path.join(workdir, CLIENT_SECRET_FILE)

    if not os.path.exists(os.path.join(workdir, token_dir)):
        os.mkdir(os.path.join(workdir, token_dir))

    cred = None
    if os.path.exists(os.path.join(workdir, token_dir, pickle_file)):
        with open(os.path.join(workdir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open(os.path.join(workdir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_NAME}')
        os.remove(os.path.join(workdir, token_dir, pickle_file))

