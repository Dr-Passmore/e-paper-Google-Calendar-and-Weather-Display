from __future__ import print_function
from googleapiclient.discovery import build
import datetime

class calendar_events:
    # Call the Calendar API
    import google_auth_process

    service = google_auth_process.googlecreds.service

    print('Getting the upcoming 10 events')

    # Pull the next 10 events
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
    events = events_result.get('items', [])
    # added print as part of test
    items = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime')
        print(start, end, event['summary'])

