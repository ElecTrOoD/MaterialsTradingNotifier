from time import sleep

from bs4 import BeautifulSoup
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Parse:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    def __init__(self, url):
        self.url = url
        self.data = None

    def get_data(self):
        try:
            browser = webdriver.Chrome(options=self.options)
            browser.get(self.url)
            element_present = expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'dataTable'))
            WebDriverWait(browser, 15).until(element_present)
            soup = BeautifulSoup(browser.page_source, 'lxml')
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
            return data
        except Exception:
            return self.data

    def run(self):
        self.data = self.get_data()
        while True:
            sleep(15)
            new_data = self.get_data()
            if new_data == self.data:
                continue
            playsound('horn.mp3')
            self.data = new_data


if __name__ == '__main__':
    user_url = input('Enter URL: ')
    parser = Parse(user_url)
    parser.run()
