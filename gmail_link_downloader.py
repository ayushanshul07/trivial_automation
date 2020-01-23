#!/usr/local/anaconda3/bin/python

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
import base64
from apiclient import errors
import requests


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service(credentials_json_location):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json_location,SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def search_messages(service, user_id, search_string):
    try:
        search_id = service.users().messages().list(userId=user_id,q=search_string).execute()
        nmessages = search_id["resultSizeEstimate"]
        final_list = []
        if nmessages > 0:
            message_ids = search_id["messages"]
            for ids in message_ids:
                final_list.append(ids["id"])
        else:
            pass
        return final_list
    except errors.HttpError as error:
        print("An error occured: %s") % error

def get_and_read_message(service, user_id, msg_id, msg_labels):
    try:
        message = service.users().messages().get(userId=user_id,id=msg_id,format='raw').execute()
        service.users().messages().modify(userId=user_id, id=msg_id, body=msg_labels).execute()
        msg_raw = base64.urlsafe_b64decode(message["raw"].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)
        content_types = msg_str.get_content_maintype()
        if content_types == "multipart":
            part1, part2 = msg_str.get_payload()
            return part1.get_payload()
        else:
            return msg_str.get_payload()

    except errors.HttpError as error:
        print("An error occured: %s") % error

credentials_json_location = '$LOCATION_TO_CREDENTIALS.JSON_FILE'
folder_to_download        = '$FOLDER_TO_DOWNLOAD_FILE_IN'
allow_from_mail           = '$MAIL_TO_ALLOW'

service = get_service(credentials_json_location) 
message_list = search_messages(service, "me", "from:" + allow_from_mail + "is:unread subject:Download")
if len(message_list) > 0:
    new_labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    url = get_and_read_message(service,"me",message_list[0],new_labels).strip()
    filename =  + message_list[0] + url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
else:
    print("already processed")

