from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import logging
from waveshare_epd import epd7in5b_V2
epd = epd7in5b_V2.EPD()

class googlecreds:
    
    creds = None
    #Scope allows read and editing access of calendar
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
    #Uses Credentials.json - Requires a URL to be clicked and the approval process to be followed first run. 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logging.info("Putting display to sleep")
            epd.sleep()
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
        
       