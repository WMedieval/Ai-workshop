#!/usr/bin/env python3
"""
google_calendar.py – BauMind AI Google Calendar integracija
"""

import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

def authenticate_google():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
    
    return build("calendar", "v3", credentials=creds)

def add_event(summary, description, date, time="09:00", duration_hours=2):
    try:
        service = authenticate_google()
        start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration_hours)
        
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_datetime.isoformat(), "timeZone": "Europe/Vienna"},
            "end": {"dateTime": end_datetime.isoformat(), "timeZone": "Europe/Vienna"},
        }
        
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"✅ Događaj dodat: {event.get('htmlLink')}")
        return event
    except HttpError as error:
        print(f"❌ Greška: {error}")
        return None

def get_upcoming_events(days=7):
    try:
        service = authenticate_google()
        now = datetime.utcnow().isoformat() + "Z"
        week_later = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"
        
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=week_later,
            maxResults=20,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        return [{
            "summary": e["summary"],
            "start": e["start"]["dateTime"] if "dateTime" in e["start"] else e["start"]["date"],
            "description": e.get("description", "")
        } for e in events]
    except HttpError as error:
        print(f"❌ Greška: {error}")
        return []

if __name__ == "__main__":
    print("📅 BauMind AI – Google Calendar")
    print("=" * 40)
    events = get_upcoming_events(14)
    print("📅 PREDSTOJEĆI DOGAĐAJI:")
    for e in events:
        print(f"   • {e['summary']} – {e['start'][:10]}")
