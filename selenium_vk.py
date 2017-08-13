import os
import time
from config import VK_URL, VK_FRIENDS, SAVE_FOLDER
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import stdout

SCROLL_SCRIPT = 'window.scrollTo(0, document.body.scrollHeight);'
DELAY = 0.1
MAX_NO_CHANGES = 20


class VKDownloader:
    def __init__(self, email_phone=None, password=None):
        self.driver = webdriver.PhantomJS()
        self.email_phone = email_phone
        self.password = password
        self.friends = []
        self.own_folder = 'Guest'

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

        try:
            profile_block = WebDriverWait(self.driver, 10) \
                .until(EC.presence_of_element_located((By.ID, "l_pr")))
            profile_url = profile_block.find_element_by_tag_name('a').get_attribute('href')
            self.driver.get(profile_url)
            name = self.driver.find_element_by_class_name('page_name').text
            self.own_folder = os.path.join(SAVE_FOLDER, name)
        finally:
            pass

    def get_friends(self):
        self.driver.get(VK_FRIENDS)
        self._scroll()
        tags = self.driver.find_elements_by_css_selector('.friends_field_title > a')
        self.friends = [(title.get_attribute('href'), title.text) for title in tags]

    def fetch_friends_music(self):
        if not os.path.exists(self.own_folder):
            os.makedirs(self.own_folder)
        os.chdir(self.own_folder)
        for url, name in self.friends:
            print(end='\r')
            print('Processing', name, end='')
            stdout.flush()
            with open('{}.txt'.format(name), 'w') as output:
                music = self.fetch_users_music(url)
                print('\n'.join('{} - {}'.format(performer, title) for performer, title in music),
                      file=output)
        print(end='\r')
        print('Finished!')

    def fetch_users_music(self, url):
        self.driver.get(url)
        music = []
        try:
            audio_block = self.driver.find_element_by_id('profile_audios')
            audio_url = audio_block.find_element_by_tag_name('a').get_attribute('href')
            self.driver.get(audio_url)
            self._scroll()
            audio_rows = self.driver.find_elements_by_class_name('audio_row__performer_title')
            for row in audio_rows:
                performer = row.find_element_by_tag_name('a').text
                title = row.find_element_by_class_name('audio_row__title_inner').text
                music.append((performer, title))
        finally:
            return music

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
