from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

service = Service('chromedriver')
driver = webdriver.Chrome(service=service)

driver.get("https://www.aviasales.ru")

search_bar_from = driver.find_element(by=By.ID, value ="avia_form_origin-input")
search_bar_to = driver.find_element(by=By.ID, value ="avia_form_destination-input")

date_fst_bar = driver.find_element(by=By.CSS_SELECTOR, value ='[data-test-id="start-date-value"]')
date_scd_bar = driver.find_element(by=By.CSS_SELECTOR, value ='[data-test-id="end-date-value"]')

sch_button = driver.find_element(by=By.CSS_SELECTOR, value ='[data-test-id="form-submit"]')

search_bar_from.clear()
search_bar_to.clear()
# date_fst_bar.clear()
# date_scd_bar.clear()

search_bar_from.send_keys("Moscow")
search_bar_to.send_keys("Vladivostok")
date_fst_bar.send_keys("21 ноября, чт")
date_scd_bar.send_keys("25 ноября, чт")

sch_button.click()

