import os
import random
import time
import pprint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import params
from logger_settings import logger
from utils import dump_json


class ApifyScraper:
    def __init__(self, username: str, password: str, hidden: bool = True):
        self._username = username
        self._password = password
        options = Options()

        if hidden:
            options.add_argument('--headless=new')

        self.driver = webdriver.Chrome(service=Service(params.chrome_driver_path), options=options)

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def while_not_xpath(self, xpath: str, wait: int = 5, error_message: str = '') -> bool:
        count = 0
        while True:
            if count == wait:
                logger.error(f'Not find xpath: {xpath}. {error_message}')
                return False

            if self.xpath_exist(xpath):
                return True
            else:
                count += 1
                time.sleep(count)
                logger.debug(f"#{count} try find xpath [{xpath}] ...")

    def get_actors_with_soup(self, url: str):
        result = dict()
        browser = self.driver

        browser.get(url)
        if self.while_not_xpath(xpath='//*[@id="data-tracking-actor-card-store-console"]') is False:
            return None

        pade_data = browser.page_source
        soup = BeautifulSoup(pade_data, 'lxml')

        actors = soup.find_all(class_='link__StyledLink-sc-7850fu-1 bmmrWC sc-papXJ eGSVMB')
        logger.info(f"Count Actors: {len(actors)}")

        all_title_actors = [item.text for item in soup.find_all(
            class_='sc-bczRLJ lijWUm sc-gsnTZi bGfyhk sc-hKMtZM jYfVRO ActorStoreItem-title')]
        all_hrefs = ['https://console.apify.com' + item.get('href') for item in actors]
        all_images = [item.get('src') for item in soup.find_all(
            class_='ActorAvatar ActorAvatar-image ActorStoreItem-avatar')]
        all_descriptions = [item.text for item in soup.find_all(
            class_='sc-bczRLJ lijWUm sc-gsnTZi bGfyhk sc-dkzDqf frxcEe ActorStoreItem-desc')]
        all_number_users = [item.text for item in soup.find_all(
            class_='sc-bczRLJ lijWUm sc-gsnTZi bGfyhk sc-dkzDqf kwrRuF')]

        if (len(all_title_actors) == len(actors) and len(all_hrefs) == len(actors) and len(all_images) == len(actors) and
                len(all_descriptions) == len(actors) and len(all_number_users) == len(actors)):
            logger.info('Count elements verified!')
        else:
            logger.critical(f'Wrong data on page {url}')
            return None

        for number in range(len(actors)):
            logger.info(f'Download record #{number + 1} - {all_title_actors[number]}')
            mistake_status, url_data = self.get_page_on_url(all_hrefs[number])

            result[all_title_actors[number]] = {
                "Name": all_title_actors[number],
                "Url": all_hrefs[number],
                "Logo": all_images[number],
                "HL-description": all_descriptions[number],
                "Number-users": all_number_users[number],
                'Number_runs': url_data['Number_runs'],
                'Last_modified': url_data['Last_modified'],
                'Owner': url_data['Owner'],
                'Owner_url': url_data['Owner_url'],
                'Payment-type': url_data['Payment-type'],
                'OpenAPI scheme': url_data['OpenAPI scheme'],
                'Information tab info': url_data['Information tab info'],
                'Information text': url_data['Information text'],
            }

            data_for_log = {
                "Name": all_title_actors[number],
                "Url": all_hrefs[number],
                "Logo": all_images[number],
                "HL-description": all_descriptions[number],
                "Number-users": all_number_users[number],
                'Number_runs': url_data['Number_runs'],
                'Last_modified': url_data['Last_modified'],
                'Owner': url_data['Owner'],
                'Owner_url': url_data['Owner_url'],
                'Payment-type': url_data['Payment-type'],
                'OpenAPI scheme': len(url_data['OpenAPI scheme']),
                'Information tab info': len(url_data['Information tab info']),
                'Information text': len(url_data['Information text']),
            }

            if mistake_status:
                logger.critical(f'#{number + 1} Find mistake in records for {all_title_actors[number]}')
                logger.info(f'#{number + 1} Data for dump, Actor - {all_title_actors[number]}: \n'
                            f'{pprint.pformat(data_for_log)}')

            dump_json(result, os.path.join(params.temp_dir, f'Page_{url.split("=")[-1]}.json'))
            logger.info(f"Finished Successfuly for #{number + 1} - {all_title_actors[number]}")

        return result

    def get_page_on_url(self, url: str):
        mistake_answer = True, {
            'Number_runs': 'unknown',
            'Last_modified': 'unknown',
            'Owner': 'unknown',
            'Owner_url': 'unknown',
            'Payment-type': 'unknown',
            'OpenAPI scheme': 'unknown',
            'Information tab info': 'unknown',
            'Information text': 'unknown',
        }
        browser = self.driver
        browser.get(url)
        if self.while_not_xpath(
                xpath='//*[@id="main"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/div[2]/div[2]/button',
                wait=15) is False:
            logger.critical(f'Didn"t find page {url}')
            return mistake_answer

        pade_data = browser.page_source
        soup = BeautifulSoup(pade_data, 'lxml')
        stats = soup.find_all(class_='ActorDetailHeader-insights-value')
        stats = [item.text for item in stats]

        if len(stats) != 4:
            logger.warning(f"Wrong count stats: {len(stats)}")
            time.sleep(1)
            pade_data = browser.page_source
            soup = BeautifulSoup(pade_data, 'lxml')
            stats = soup.find_all(class_='ActorDetailHeader-insights-value')
            stats = [item.text for item in stats]
            if len(stats) != 4:
                logger.critical(f"Mistake on get data stats: {stats}, for page: {url}")
                return mistake_answer

        number_runs = stats[2]
        last_modified = stats[0]

        try:
            owner = soup.find(class_='ProfileInfo-PersonLink').text
        except Exception as ex:
            logger.error(f"Error for owner: {ex}")
            owner = 'UNKNOWN'

        try:
            owner_url = soup.find(class_='ProfileInfo-PersonLink').get('href')
        except Exception as ex:
            logger.error(f"Error for owner_url: {ex}")
            owner_url = 'UNKNOWN'

        try:
            payment_type = soup.find(
                class_='chip__Default-sc-1aw04iu-0 fzxzoI paid_actor_tagstyled__ActorDropdownTag-sc-1mo7zji-0 fThFpI Chip-body'
            ).text
        except Exception as ex:
            logger.error(f"Error payement_type: {ex}")
            payment_type = 'UNKNOWN'

        if self.while_not_xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/button') is False:
            return mistake_answer

        browser.find_element(By.XPATH,
                             '//*[@id="main"]/div[1]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/button').click()
        self.while_not_xpath('//*[@id="OpenApi"]', wait=7)
        browser.find_element(By.XPATH, '//*[@id="OpenApi"]').click()
        self.while_not_xpath('//*[@id="react-target"]/div[3]/div/section/div/div/div/div[2]/code')
        time.sleep(1)
        open_api_scheme = browser.find_element(By.XPATH,
                                             'open_api_scheme = info_open_api//*[@id="react-target"]/div[3]/div/section/div/div/div/div[2]/code').text

        browser.get(url + '/information')
        self.while_not_xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/button')
        time.sleep(1)
        information_html = browser.page_source

        self.while_not_xpath('//*[@id="main"]/div[1]/div[2]/div[5]/div/div/div')
        time.sleep(1)
        information_text = browser.find_element(By.XPATH, '//*[@id="main"]/div[1]/div[2]/div[5]/div/div/div').text

        mistake = False
        result = {
            'Number_runs': number_runs,
            'Last_modified': last_modified,
            'Owner': owner,
            'Owner_url': owner_url,
            'Payment-type': payment_type,
            'OpenAPI scheme': open_api_scheme,
            'Information tab info': information_html,
            'Information text': information_text,
        }

        for key, value in result.items():
            if len(value) < 2 or value == 'UNKNOWN':
                mistake = True
                break

        return mistake, result

    def login(self):
        try:
            browser = self.driver
            browser.get("https://console.apify.com")
            time.sleep(random.randrange(1, 4))

            login_input = browser.find_element(By.NAME, 'email')
            login_input.clear()
            login_input.send_keys(self._username)

            time.sleep(3)

            password_input = browser.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(self._password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(10)
            return True

        except Exception as ex:
            logger.error(f"Catch mistake during login: {ex}")
            return False

    def xpath_exist(self, xpath: str) -> bool:
        browser = self.driver
        try:
            browser.find_element(By.XPATH, xpath)
            exist = True

        except NoSuchElementException:
            exist = False

        return exist
