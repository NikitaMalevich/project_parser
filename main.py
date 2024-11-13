import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import re


class Parser_elibrary():

    def __init__(self, rsci):
        self.data_res = pd.DataFrame([])
        self.rsci = rsci

        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.service = Service('chromedriver')
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
        time.sleep(2)

        search_button = self.driver.find_element(by=By.CSS_SELECTOR, value='[onclick="author_search()"]').click()

        try:
            move_to_link = self.driver.find_element(by=By.CSS_SELECTOR,
                                                    value='[title="Список публикаций данного автора в РИНЦ"]').click()
        except:
            print('Автор не найден, проверьте код РИНЦ')
            return

        self.name_authors = self.driver.find_element(by=By.CSS_SELECTOR,
                                                     value='[style="width:540px; margin:0 20px 20px 20px; border:0; padding:0; text-align: center; font-size: 9pt;"]').text

        fin_symb = self.name_authors.find('*')
        self.name_authors = self.name_authors[:fin_symb]

        cp = self.count_publications()
        total_publications, current_publications = cp[0], cp[1]

        while current_publications <= total_publications:
            all_articles_per_page = self.driver.find_element(by=By.ID, value='restab').text
            all_articles_data = all_articles_per_page.split('\n')[1:]

            indices = [index for index, item in enumerate(all_articles_data) if re.match(r'^\d+\.$', item)]

            # for i in indices:
            for i in range(len(indices)):
                try:
                    article_data_i = all_articles_data[indices[i]:indices[i + 1]]
                except:
                    article_data_i = all_articles_data[indices[i]:]

                empty_string = len(self.data_res)
                self.data_res.loc[empty_string, 'Название статьи'] = article_data_i[1]
                self.data_res.loc[empty_string, 'Авторы'] = article_data_i[2]
                self.data_res.loc[empty_string, 'Издание'] = ' '.join(article_data_i[3:])

            if current_publications == total_publications:
                break
            else:
                next_page_button = self.driver.find_element(by=By.CSS_SELECTOR,
                                                            value='[title="Следующая страница"]').click()
                cp = self.count_publications()
                total_publications, current_publications = cp[0], cp[1]

                time.sleep(3)

        self.data_res.index += 1
        print(self.data_res)

        self.data_res.to_excel(f'{self.name_authors}.xlsx', sheet_name=self.name_authors)
        print('Готово, наслаждайтесь!')

# Nikita : 1192741
# rsci = 1192741

if __name__ == '__main__':
    print(f'Введите rsci автора:')
    rsci = int(input())

    pc = Parser_elibrary(rsci)
    pc.launch_parser()
