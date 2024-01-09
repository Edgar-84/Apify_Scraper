from config import params
from logger_settings import logger
from work_module import ApifyScraper


def main():
    logger.info(f'Starting program ...')
    scraper = ApifyScraper(username=params.username, password=params.password)
    scraper.login()

    for page in range(2, 63):
        url = f'https://console.apify.com/store?page={page}'
        logger.info(f"Run work with PAGE: {url}...")
        scraper.get_actors_with_soup(url)
        logger.info(f"FINISHED work with PAGE: {url}.")


if __name__ == '__main__':
    main()
