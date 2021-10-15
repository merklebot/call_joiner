import time

from selenium.webdriver import Chrome, ChromeOptions

from call_joiner.logging import log
from call_joiner.calendar import GoogleCalendar
from call_joiner.browser import GoogleMeet
from call_joiner.config import settings


class CallJoiner:
    ongoing_call = None

    def __init__(self, calendar: GoogleCalendar, google_meet: GoogleMeet):
        self.calendar = calendar
        self.google_meet = google_meet

    def join_call(self):
        self.google_meet.join_call(self.ongoing_call)

    def spin(self):
        while True:
            self.calendar.sync()
            if event := self.calendar.ongoing_event:
                if event.conference_link != self.ongoing_call:
                    log.info(f"New event {event.title} with conference {event.conference_link}, attendees {list(event.attendees)}")
                    self.ongoing_call = event.conference_link
                    self.google_meet.close_all_tabs()
                    self.join_call()
            elif self.ongoing_call:
                log.info(f"Call {self.ongoing_call} finished")
                self.ongoing_call = None
                self.google_meet.close_all_tabs()
            time.sleep(3)


if __name__ == "__main__":
    log.info("Starting")

    options = ChromeOptions()
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 1,
    })
    webdriver = Chrome(
        executable_path=settings.CHROMIUM_DRIVER,
        options=options,
    )
    google_meet = GoogleMeet(webdriver)

    calendar = GoogleCalendar()
    calendar.connect()
    calendar.sync()

    CallJoiner(calendar, google_meet).spin()
