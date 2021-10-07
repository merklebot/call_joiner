from call_joiner.logging import log
from call_joiner.calendar import GoogleCalendar
from call_joiner.browser import GoogleMeet


class CallJoiner:
    def __init__(self, calendar, event_page):
       ...


if __name__ == "__main__":
    log.info("Starting")

    calendar = GoogleCalendar()
    calendar.connect()
    calendar.load()

    google_meet_user = GoogleMeet()

    CallJoiner(calendar, google_meet).spin()

