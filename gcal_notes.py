#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#]

# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Google Calendar Events Weeknotes
"""

import httplib2
import os
import re
import json
from cgi import escape

from datetime import datetime, timedelta
from dateutil import parser

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


from basic_config import config_keys
from secure_config import google_api_service_account_keys


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
credentials_dict = google_api_service_account_keys
api_credentials = client.SignedJwtAssertionCredentials(credentials_dict['client_email'],
                                                       credentials_dict['private_key'].encode(),
                                                       SCOPES)

api_http = api_credentials.authorize(httplib2.Http())
api = discovery.build('calendar', 'v3', http=api_http)

now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
later = (datetime.utcnow() + timedelta(days=config_keys['google_calendar_lookahead'])).isoformat() + 'Z' # 'Z' indicates UTC time

def get_events_between(now=now,later=later):
    eventsResult = api.events().list(
        calendarId=config_keys['google_calendar_id'], timeMin=now, timeMax=later, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    return eventsResult.get('items', [])

def html_format_event(event):
    date = event['start'].get('dateTime')
    if date is None:
        date = parser.parse(event['start'].get('date')).date()
        time = None
    else:
        date = parser.parse(date)
        time = date.timetz()
        date = date.date()

    edate = event['end'].get('dateTime')
    if edate is None:
        edate = parser.parse(event['end'].get('date')).date()
        etime = None
    else:
        edate = parser.parse(edate)
        etime = edate.timetz()
        edate = edate.date()

    title = event['summary']
    description = event['description'].encode('utf-8')
    links = re.findall('link:(.*)', description)

    if len(links)>0:
        event_str="<a href={link} title=\"{description}\"><b>{title}</b></a>".format(link=links[0], description=description, title=title)
    else:
        event_str="<b title=\"{description}\">{title}</b>".format(description=description, title=title)


    if time is None:
        content = "<tr><td>{date:%a\t %d/%m}</td><td>{title}</td><td colspan=2>{end_str:}</td></tr>".format(
            date = date, end_str = "All of %d days"%(edate-date).days,
            title = event_str)
    else:
        content = "<tr><td>{date:%a\t %d/%m}</td><td>{title}</td><td>{time:%H:%M}</td><td>{etime:%H:%M}</td></tr>".format(
                date = date, time = time, etime=etime,
                title = event_str)
    return content

def html_format_events(events):
    header = '<div id="gcal-events"><h2>Events</h2> <p>What\'s happening in the space in the next fortnight</p>\n<i>Mouse over for event descriptions</i>'
    content = ""
    footer = "</div>"
    if not events:
        content+="No events this week!"
    else:
        content+="<table><th>Date</th><th>Event</th><th colspan=2>Times</th>"
        footer= "</table>"+footer

    for event in events:
        content+= html_format_event(event)

    return (header+content+footer).decode("utf8")


def html_weeknotes():
    return html_format_events(get_events_between(now,later))

if __name__ == "__main__":
    print html_weeknotes()
