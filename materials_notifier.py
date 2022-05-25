import sys
from time import sleep

from art import text2art
from bs4 import BeautifulSoup
from playsound import playsound
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Parse:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    def __init__(self, url):
        self.url = url
        self.count = 0
        self.data = None

    def get_data(self):
        try:
            browser = webdriver.Chrome(options=self.options)
            browser.get(self.url)
            element_present = expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'dataTable'))
            WebDriverWait(browser, 15).until(element_present)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            browser.quit()
            data = []
            for row in soup.find_all('tr')[1:11]:
                columns = row.find_all('td')
                data.append({
                    'material': columns[1].get_text(),
                    'system': columns[2].get_text()[:-2],
                    'amount': columns[3].get_text(),
                    'distance': columns[5].get_text(),
                })
            return sorted(data)
        except SessionNotCreatedException as e:
            print(e.msg)
            sys.exit(1)
        except Exception:
            return self.data

    def run(self):
        self.data = self.get_data()
        while True:
            sleep(30)
            self.count += 1
            print(f'\r[INFO] Check if the offers have been updated... Count: {self.count}', end='')
            new_data = self.get_data()
            if new_data == self.data:
                continue
            playsound('horn.mp3')
            self.data = new_data


if __name__ == '__main__':
    print(text2art('ED MN', font='block'))
    while True:
        user_url = input('\nEnter URL: ')
        if 'https://inara.cz/market-materials/' in user_url:
            print('[INFO] Link is valid. Starting tracking offers...\n')
            break
        else:
            print('[ERROR] Invalid link')
    parser = Parse(user_url)
    parser.run()
