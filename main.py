import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import re

class Parser_elibrary():

    def __init__(self, rsci, name_authors):
        self.data_res = pd.DataFrame([])
        self.rsci = rsci
        self.name_authors = name_authors

        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.service = Service('chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service)

        self.driver.get("https://elibrary.ru/authors.asp")

    def count_publications(self):
        q_publications = self.driver.find_element(by=By.CLASS_NAME, value='redref').text
        q_publications = re.findall(r'\d+', q_publications)

        total_publications = int(q_publications[0])
        current_publications = int(q_publications[-1])

        return total_publications, current_publications

    def launch_parser(self):

        search_bar_codetype = self.driver.find_element(by=By.ID, value='codetype')  # rinc
        search_bar_codevalue = self.driver.find_element(by=By.ID, value='codevalue')  # rinc

        select = Select(search_bar_codetype)
        select.select_by_value("RSCI")

        search_bar_codevalue.send_keys(str(self.rsci))

        search_button = self.driver.find_element(by=By.CSS_SELECTOR, value='[onclick="author_search()"]').click()

        link_author = self.driver.find_element(by=By.CSS_SELECTOR,
                                               value='[title="Список публикаций данного автора в РИНЦ"]').get_property(
            name='href')
        move_to_link = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value='[title="Список публикаций данного автора в РИНЦ"]').click()

        cp = self.count_publications()
        total_publications, current_publications = cp[0], cp[1]

        while current_publications <= total_publications:
            all_articles_per_page = self.driver.find_element(by=By.ID, value='restab').text
            all_articles_data = all_articles_per_page.split('\n')[1:]

            count = 0

            while True:
                empty_string = len(self.data_res)

                self.data_res.loc[empty_string, 'Название статьи'] = all_articles_data[count + 1]
                self.data_res.loc[empty_string, 'Авторы'] = all_articles_data[count + 2]
                self.data_res.loc[empty_string, 'Издание'] = all_articles_data[count + 3]
                count += 4

                try:
                    all_articles_data[count+1]
                except:
                    break

            if current_publications == total_publications:
                break
            else:
                next_page_button = self.driver.find_element(by=By.CSS_SELECTOR, value='[title="Следующая страница"]').click()
                cp = self.count_publications()
                total_publications, current_publications = cp[0], cp[1]

                time.sleep(1)

        self.data_res.index += 1
        print(self.data_res)

        self.data_res.to_excel(f'{self.name_authors}.xlsx')

# print(f'Введите rsci автора:')
# rsci = int(input())
#
# print(f'Введите Имя Фамилию автора через пробел:')
# name_authors = str(input())

rsci = 1072704
name_authors = 'Marina Shirokova'

pc = Parser_elibrary(rsci, name_authors)
pc.launch_parser()

print('Готово, наслаждайтесь!')
