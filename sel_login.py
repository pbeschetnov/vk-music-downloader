import time
from config import VK_URL, VK_FRIENDS
from getpass import getpass
from selenium import webdriver


SCROLL_SCRIPT = 'window.scrollTo(0, document.body.scrollHeight);'
DELAY = 0.1
MAX_NO_CHANGES = 10


class VKDownloader:
    def __init__(self, email_phone=None, password=None):
        self.driver = webdriver.PhantomJS()
        self.email_phone = email_phone
        self.password = password

    def login(self):
        self.driver.get(VK_URL)
        while not self.email_phone:
            self.email_phone = input('Enter email or phone: ').strip()

        while not self.password:
            self.password = getpass('Enter password: ')

        email_element = self.driver.find_element_by_id('index_email')
        pass_element = self.driver.find_element_by_id('index_pass')

        email_element.send_keys(self.email_phone)
        pass_element.send_keys(self.password)

        login_button = self.driver.find_element_by_id('index_login_button')
        login_button.click()
        time.sleep(DELAY)

    def get_friends(self):
        self.driver.get(VK_FRIENDS)
        self._scroll()
        friends = self.driver.find_elements_by_css_selector('.friends_field_title > a')
        friends = [(title.get_attribute('href'), title.text) for title in friends]
        print(len(friends))
        for friend in friends:
            print(friend)

    def _scroll(self):
        prev_len = len(self.driver.page_source)
        no_changes = 0

        while no_changes < MAX_NO_CHANGES:
            self.driver.execute_script(SCROLL_SCRIPT)
            time.sleep(DELAY)
            if prev_len < len(self.driver.page_source):
                prev_len = len(self.driver.page_source)
                no_changes = 0
            else:
                no_changes += 1
