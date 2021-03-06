import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver import Remote as WebDriver
from selenium.webdriver.support import expected_conditions as EC

from call_joiner.config import settings


class GoogleMeet:
    def __init__(self, webdriver: WebDriver):
        self.webdriver = webdriver

    def quit(self):
        self.webdriver.quit()

    def close_all_tabs(self):
        self.webdriver.execute_script("window.open('')")
        for tab in self.webdriver.window_handles[:-1]:
            self.webdriver.switch_to.window(tab)
            self.webdriver.close()
        self.webdriver.switch_to.window(self.webdriver.window_handles[0])

    def join_call(self, url: str):
        try:
            self.webdriver.get("https://accounts.google.com/ServiceLogin")
            email_input = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_input.send_keys(settings.GOOGLE_MEET_CREDS.EMAIL)
            next_button = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='identifierNext']/div/button"))
            )
            next_button.click()
            time.sleep(2)
            password_input = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_input.send_keys(settings.GOOGLE_MEET_CREDS.PASSWORD)
            next_button = self.webdriver.find_element_by_xpath(
                "//*[@id='passwordNext']/div/button"
            )
            next_button.click()
        except TimeoutException:
            pass

        t1 = time.time()
        while time.time() - t1 < 60:
            try:
                self.webdriver.get(url)
                time.sleep(3)
                self.webdriver.refresh()
                time.sleep(3)
                join_button = WebDriverWait(self.webdriver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[text()='Join now']"))
                )
                join_button.click()
                break
            except (ElementNotInteractableException, TimeoutException):
                pass
