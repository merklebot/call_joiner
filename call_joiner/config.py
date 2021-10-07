from pydantic import BaseSettings


class GoogleCalendarCredentials(BaseSettings):
    PROJECT_ID: str
    PRIVATE_KEY_ID: str
    PRIVATE_KEY: str
    CLIENT_EMAIL: str
    CLIENT_ID: str
    CLIENT_X509_CERT_URL: str
    CALENDAR_ID: str

    class Config:
        env_prefix = "GOOGLE_CALENDAR_CREDS_"
        case_sensitive = True


class GoogleCalendar(BaseSettings):
    NOTIFICATIONS_WEBHOOK_ENDPOINT: str
    WEBHOOK_EXPIRATION_SECONDS: str
    CREDENTIALS: GoogleCalendarCredentials

    class Config:
        env_prefix = "GOOGLE_CALENDAR_"
        case_sensitive = True


class Settings(BaseSettings):
    CHROMIUM_DRIVER: str
    GOOGLE_CALENDAR: GoogleCalendar

    class Config:
        case_sensitive = True


settings = Settings(
    GOOGLE_CALENDAR=GoogleCalendar(
        CREDENTIALS=GoogleCalendarCredentials()
    )
)
