import os
from config import VK_URL, SAVE_FOLDER
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import stdout

AUDIO_REQUEST = VK_URL + '/audio?id={user_id}&offset={offset}'
FRIENDS_REQUEST = VK_URL + '/friends?offset={offset}'


def erase_print(*args):
    print(end='\r')
    print(*args, end='')
    stdout.flush()


class VKDownloader:
    def __init__(self, email_phone=None, password=None):
        self.driver = webdriver.PhantomJS()
        self.email_phone = email_phone
        self.password = password
        self.friends = []
        self.own_folder = 'Guest'

    def login(self):
        while True:
            self.driver.get(VK_URL)
            while not self.email_phone:
                self.email_phone = input('Enter email or phone: ').strip()

            while not self.password:
                self.password = getpass('Enter password: ')

            email_element = self.driver.find_element_by_css_selector('input[name="email"]')
            pass_element = self.driver.find_element_by_css_selector('input[name="pass"]')

            email_element.send_keys(self.email_phone)
            pass_element.send_keys(self.password)

            login_button = self.driver.find_element_by_css_selector('input[type="submit"]')
            login_button.click()

            try:
                profile_block = WebDriverWait(self.driver, 2) \
                    .until(EC.presence_of_element_located((By.CLASS_NAME, 'op_owner')))
                name = profile_block.get_attribute('data-name')
                self.own_folder = os.path.join(SAVE_FOLDER, name)
                break
            except:
                print('Wrong email (phone) of password')
                self.email_phone = None
                self.password = None

    def get_friends(self):
        offset = 0
        self.friends = []
        while True:
            self.driver.get(FRIENDS_REQUEST.format(offset=offset))
            friend_blocks = self.driver.find_elements_by_class_name('si_owner')
            if len(friend_blocks) == 0:
                break
            offset += len(friend_blocks)
            self.friends.extend((block.get_attribute('href'), block.text) for block in friend_blocks)

    def fetch_friends_music(self):
        if not os.path.exists(self.own_folder):
            os.makedirs(self.own_folder)
        os.chdir(self.own_folder)
        for i, (url, name) in enumerate(self.friends, start=1):
            message = 'Processing {0}/{1} friend: {2}'.format(i, len(self.friends), name)
            with open('{}.txt'.format(name), 'w') as output:
                music = self.fetch_users_music(url, message)
                print('\n'.join('{} - {}'.format(performer, title) for performer, title in music),
                      file=output)
        erase_print('Finished!')

    def fetch_users_music(self, url, message):
        self.driver.get(url)
        music = []
        erase_print(message)
        try:
            audio_block = self.driver.find_element_by_css_selector('a.pm_item[href^="/audios"]')
            audio_url = audio_block.get_attribute('href')
            user_id = audio_url.split('audios')[-1]
            offset = 0
            count = None
            while True:
                self.driver.get(AUDIO_REQUEST.format(user_id=user_id, offset=offset))
                if count is None:
                    count_block = self.driver.find_element_by_class_name('audioPage__count')
                    count = int(count_block.text.split()[0])
                erase_print(message, '-', '{}%'.format(100 * offset // count))
                audio_rows = self.driver.find_elements_by_css_selector('.audios_block .ai_label')
                if len(audio_rows) == 0:
                    break
                offset += len(audio_rows)
                for row in audio_rows:
                    artist = row.find_element_by_class_name('ai_artist').text
                    title = row.find_element_by_class_name('ai_title').text
                    music.append((artist, title))
        finally:
            return music
