from datetime import datetime

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    id: str
    title: str
    start: datetime
    end: datetime
    attendees: frozenset[str] = frozenset()
    description: str = ""
    conference_link: str = ""

    class Config:
        frozen = True

    @classmethod
    def from_google(cls, google_calendar_event):
        start = google_calendar_event.get("start", {}).get("dateTime", None)
        end = google_calendar_event.get("end", {}).get("dateTime", None)
        attendees = google_calendar_event.get("attendees", set())
        conference_entry_points = google_calendar_event.get(
            "conferenceData", {}
        ).get(
            "entryPoints", []
        )
        video_entry_point = next((
            ep for ep in conference_entry_points if
            ep.get("entryPointType", "") == "video"
        ), {})

        return cls(
            id=google_calendar_event["id"],
            title=google_calendar_event["summary"],
            start=datetime.fromisoformat(start) if start else None,
            end=datetime.fromisoformat(end) if end else None,
            attendees=frozenset(a["email"] for a in attendees) if attendees else set(),
            conference_link=video_entry_point.get("uri", ""),
            description=google_calendar_event.get("description", ""),
        )
