import datetime
import logging
from dataclasses import dataclass
from random import randrange
from typing import Tuple
from urllib.parse import urljoin, urlencode

from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger('django')

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'


@dataclass
class Place:
    letter: str
    title: str
    places: int


@dataclass
class Train:
    num: str
    category: str

    date_at: datetime.date
    time_at: datetime.time

    places: list[Place]


class TrainScraper:
    BASE_URL = 'https://booking.uz.gov.ua/'

    ACTION_TIMEOUT = 1
    WAIT_TIMEOUT = 10

    DEFAULT_SERVICE_ARGS = [
        '--allow-running-insecure',

        '--no-sandbox',
        '--hide-scrollbars',
        '--disable-infobars',

        '--disable-application-cache',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-notifications',
        '--disable-setuid-sandbox',
        '--disable-web-security',
    ]

    def __init__(self):
        chrome_options = ChromeOptions()

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option(
            'prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0,
            })
        for arg in self.DEFAULT_SERVICE_ARGS:
            chrome_options.add_argument(arg)

        self.__driver = webdriver.Chrome(service=ChromService(ChromeDriverManager().install()), options=chrome_options)
        self.__driver.maximize_window()

    def scrapy(self, checker):
        try:
            logger.info(f'Checker by id:{checker.id} run.')
            params = {
                'from': checker.from_station.value,
                'to': checker.to_station.value,
                'date': checker.date_at.strftime(DATE_FORMAT),
                'time': checker.time_at.strftime(TIME_FORMAT),
                'url': 'train-list'
            }

            self.open_search_page(params)
            # if self.is_captcha():
            #     self.skip_captcha(params)

            return self.get_exist_trains()
        except:
            logger.error(f'Invalid scrapy checker by id{checker.id}.')

        finally:
            self.__driver.close()
            self.__driver.quit()

    def open_search_page(self, params):
        # self.__driver.get(self.BASE_URL)
        url_with_params = urljoin(self.BASE_URL, '?' + urlencode(params))

        try:
            self.__driver.get(url_with_params)
            self.wait_until_event((By.CLASS_NAME, 'interchange-button'), clicked=False)
        except TimeoutException:
            self.skip_captcha(params)

    def wait_with_timeout(self, timeout: int = ACTION_TIMEOUT):
        action = webdriver.ActionChains(self.__driver)
        action.pause(randrange(timeout, timeout + 2, 1))
        action.perform()

    def wait_until_event(self, locator: Tuple[str, str], clicked: bool = True):
        driver_wait = WebDriverWait(self.__driver, self.WAIT_TIMEOUT)
        element = driver_wait.until(EC.presence_of_element_located(locator))
        if clicked:
            element.click()

    def get_exist_trains(self) -> list[Train]:
        if self.is_search_error() or not self.is_has_train:
            return []

        trains = []
        table_rows = self.__driver.find_elements(By.XPATH, '//table[@class="train-table"] tr')

        for row in table_rows[1:]:
            data_at = row.find_element(By.CSS_SELECTOR, '.date span:nth-child(2)').text
            time_at = row.find_element(By.CSS_SELECTOR, '.time div:nth-child(1)').text
            train_data = {
                'num': row.find_element(By.CSS_SELECTOR, '.num').text.strip(),
                'category': row.find_element(By.CSS_SELECTOR, '.num i').text,
                'date_at': datetime.datetime.strptime(data_at, DATE_FORMAT).date(),
                'time_at': datetime.datetime.strptime(time_at, TIME_FORMAT),
                'places': [
                    Place(
                        letter=row.find_element(By.CSS_SELECTOR, '.place .wagon-class').text[-1],
                        title=row.find_element(By.CSS_SELECTOR, '.place .wagon-class span').text,
                        places=int(row.find_element(By.CSS_SELECTOR, '.place .place-count').text)
                    )
                ]
            }
            train_instance = Train(**train_data)
            trains.append(train_instance)

        return trains

    def is_search_error(self) -> bool:
        try:
            self.__driver.find_element(By.CLASS_NAME, 'search-error')
            return True
        except (WebDriverException, NoSuchElementException):
            return False

    def is_has_train(self) -> bool:
        try:
            self.__driver.find_element(By.CLASS_NAME, 'train-table')
            return True
        except (WebDriverException, NoSuchElementException):
            return False

    def is_captcha(self) -> bool:
        try:
            self.__driver.find_element(By.ID, 'rc-imageselect')
            return True
        except (WebDriverException, NoSuchElementException):
            return False

    def skip_captcha(self, params):
        url_with_params = urljoin(self.BASE_URL, '?' + urlencode(params))
        self.__driver.get(url_with_params)
        self.wait_until_event((By.ID, 'search-frm'))
