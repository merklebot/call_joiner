from typing import Union
from datetime import datetime, timezone

import google.oauth2.service_account
import googleapiclient.discovery

from call_joiner.config import settings
from call_joiner.logging import log
from call_joiner.models import CalendarEvent


class GoogleCalendar:
    events = set()

    def __init__(self):
        self._service = None

    def connect(self):
        service_account_info = {
            "type": "service_account",
            "project_id": settings.GOOGLE_CALENDAR.CREDENTIALS.PROJECT_ID,
            "private_key_id": settings.GOOGLE_CALENDAR.CREDENTIALS.PRIVATE_KEY_ID,
            "private_key": settings.GOOGLE_CALENDAR.CREDENTIALS.PRIVATE_KEY,
            "client_email": settings.GOOGLE_CALENDAR.CREDENTIALS.CLIENT_EMAIL,
            "client_id": settings.GOOGLE_CALENDAR.CREDENTIALS.CLIENT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": settings.GOOGLE_CALENDAR.CREDENTIALS.CLIENT_X509_CERT_URL,
        }
        creds = google.oauth2.service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/calendar"],
        )
        self._service = googleapiclient.discovery.build(
            "calendar", "v3", credentials=creds
        )
        log.info(f"Connected to {service_account_info['client_email']} account")

    def sync(self):
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events = self._service.events().list(
            calendarId=settings.GOOGLE_CALENDAR.CREDENTIALS.CALENDAR_ID,
            timeMin=now,
            maxResults=2,
            singleEvents=True,
            orderBy="startTime",
        ).execute().get("items", [])

        if not events:
            self.events = set()
            return

        self.events = {CalendarEvent.from_google(e) for e in events}

    @property
    def ongoing_event(self) -> Union[CalendarEvent, None]:
        now = datetime.now().astimezone(timezone.utc)
        for event in self.events:
            if (
                    event.start.astimezone(timezone.utc)
                    < now
                    < event.end.astimezone(timezone.utc)
            ):
                return event
