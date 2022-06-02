import sys
import time

from art import text2art
from bs4 import BeautifulSoup
from playsound import playsound
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Notifier:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def __init__(self, url):
        self.url = url
        self.requests = 0
        self.updates = 0
        self.errors = 0
        self.last_update = 'never'
        self.last_system = ''

    def check_updates(self):
        self.requests += 1
        try:
            element_present = expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'dataTable'))

            browser = webdriver.Chrome(options=self.options)
            browser.get(self.url)
            WebDriverWait(browser, 15).until(element_present)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            browser.quit()

            columns = soup.find_all('tr')[1].find_all('td')
            updated = columns[6].get_text()
            new_system = columns[2].get_text()[:-2],

            if updated == 'now' and new_system != self.last_system:
                self.last_system = new_system
                return True
            return False

        except SessionNotCreatedException as e:
            print(e.msg)
            sys.exit(1)
        except Exception as e:
            self.errors += 1
            return False

    def run(self):
        while True:
            print(f'\r[INFO] Check if the offers have been updated... Requests: {self.requests}, '
                  f'updates: {self.updates}, errors: {self.errors}. Last update: {self.last_update}', end='')

            time.sleep(30)
            if not self.check_updates():
                continue

            playsound('horn.mp3')
            self.updates += 1
            self.last_update = time.strftime('%H:%M')


if __name__ == '__main__':
    print(text2art('EDMN', font='block'))
    while True:
        user_url = input('\nEnter URL: ')
        if 'https://inara.cz/market-materials/' in user_url:
            print('[INFO] Link is valid. Starting tracking offers...\n')
            break
        else:
            print('[ERROR] Invalid link')

    ed_notifier = Notifier(user_url)
    ed_notifier.run()
