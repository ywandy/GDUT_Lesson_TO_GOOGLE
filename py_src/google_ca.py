from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
from httplib2 import socks


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GDUT_TO_GOOGLE_CALENDAR'


def get_credentials(fg):
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, fg)
        print('Storing credentials to ' + credential_path)
    return credentials

def test_google():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    print("success")
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    t_s = datetime.time(18, 30, 0)
    d_s = datetime.date(2017, 9, 4)
    dt_c_s = datetime.datetime.combine(d_s, t_s).isoformat("T")

    t_e = datetime.time(19, 30, 0)
    d_e = datetime.date(2017, 9, 4)
    dt_c_e = datetime.datetime.combine(d_e, t_e).isoformat("T")

    test_body = {
        "summary": "test just for",
        "location": "gdut",
        "start": {
            "timeZone": "Asia/Shanghai",
            "dateTime": dt_c_s,
        },
        "end": {
            "timeZone": "Asia/Shanghai",
            "dateTime": dt_c_e,
        },
        "description": "test",
    }
    print(service.events().insert(calendarId='primary',body=test_body).execute())
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def Add_Lesson(google_service,cal_id,title,startdatetime,descript,adv):
    time_tmp = datetime.timedelta(hours=2)
    enddatetime = time_tmp+startdatetime
    test_body = {
        "summary": title,
        "start": {
            "timeZone": "Asia/Shanghai",
            "dateTime": startdatetime.isoformat("T"),
        },
        "end": {
            "timeZone": "Asia/Shanghai",
            "dateTime": enddatetime.isoformat("T"),
        },
        "reminders": {
            "overrides": [
                {
                    "minutes": adv,
                    "method": "popup",
                },
            ],
            "useDefault": False,
        },
        "description": descript,
    }
    google_service.events().insert(calendarId=cal_id, body=test_body).execute()


def init_google(fg):
    credentials = get_credentials(fg)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service



