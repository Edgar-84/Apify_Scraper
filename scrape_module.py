import requests
from bs4 import BeautifulSoup

from config import params
from utils import save_html_page
from logger_settings import logger


def authorize_apify():
    session = requests.Session()
    login_url = 'https://console.apify.com/sign-in'
    # login_data = {'email': 'edgar@mknltech.com', 'password': '1997edgar'}
    token = 'apify_ui_H9k0Ea8AV5M2x0bHctxayiApwY8dVe474gZI'  # Замените на ваш токен авторизации

    headers = {
        'Authorization': f'Bearer {token}'  # Используйте соответствующий заголовок авторизации
    }
    # response = session.post(login_url, data=login_data)
    response = session.get(login_url, headers=headers)

    if response.status_code == 200:
        # Авторизация прошла успешно, выполните запрос на получение данных
        data_url = 'https://console.apify.com/store'  # Замените на URL-адрес страницы с данными

        response = session.get(data_url)
        if response.status_code == 200:
            data = response.text
            print('Good')
            print(data)
        else:
            print("Ошибка при получении данных:", response.status_code)
    else:
        print("Ошибка при выполнении авторизации:", response.status_code)
        print(response.text)


def get_links_to_actors():
    # result = save_html_page(
    #     url="https://console.apify.com/store",
    #     headers=params.headers,
    #     path_save=params.temporary_html_doc
    # )
    #
    # if result is False:
    #     return False

    try:
        with open(params.temporary_html_doc) as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_news_hrefs = soup.find_all(class_="link__StyledLink-sc-7850fu-1 bmmrWC sc-papXJ eGSVMB")
        print('all_news_hrefs ', all_news_hrefs)
        hrefs = [params.bank_url + item.get("href") for item in all_news_hrefs]
        print('hrefs ', hrefs)

    except Exception as ex:
        logger.error(f"Mistake during getting links to actors: {ex}")
        return False


def test_hi_ad():
    data_url = 'https://console.apify.com/store'
    token = 'apify_ui_H9k0Ea8AV5M2x0bHctxayiApwY8dVe474gZI'  # Замените на ваш токен авторизации

    headers = {
        'Authorization': f'Bearer {token}'  # Используйте соответствующий заголовок авторизации
    }



    result = requests.get(url=data_url, headers=headers)
    print('status ', result.status_code)
    print(result.text)

# test_hi_ad()

# def test_2():
#     s = requests.Session()
#     data_url = 'https://console.apify.com/store'
#     token = 'apify_api_HnlGZwvslLSKmd4PgmQAwWyBxYrGdN0IdXmR'  # Замените на ваш токен авторизации
#
#     headers = {
#         'Authorization': f'Bearer {token}'  # Используйте соответствующий заголовок авторизации
#     }
#     r = s.get(data_url, headers=headers)
#     print(r)
#     print('cookies', s.cookies)
#
# test_2()
# print(get_links_to_actors())
# print(authorize_apify())

# from apify_client import ApifyClient
#
#
# def test_api():
#     token = 'apify_api_HnlGZwvslLSKmd4PgmQAwWyBxYrGdN0IdXmR'
#     apify_client = ApifyClient(token)
#     actor_collection_client = apify_client.actors()
#     actor_list = actor_collection_client.list().items
#
#
#     print(actor_list)
#
#
# print(test_api())
# apify_ui_H9k0Ea8AV5M2x0bHctxayiApwY8dVe474gZI

def test_3():
    import requests

    cookies = {
        '_gid': 'GA1.2.1294268146.1704751954',
        'ApifyUtk': 'hhVJTB8oOfnB85j9M',
        '_gcl_au': '1.1.1420136768.1704751955',
        'ApifyAcqSrc': 'https://console.apify.com/',
        'ApifyAcqRef': '',
        'SL_G_WPT_TO': 'en',
        'SL_GWPT_Show_Hide_tmp': '1',
        'SL_wptGlobTipTmp': '1',
        'hubspotutk': '7635a87b45529bda5a7d9a6e1c85768d',
        '__hssrc': '1',
        'intercom-device-id-kod1r788': '15a75f6b-c779-4c28-9583-577367862b94',
        'OptanonAlertBoxClosed': '2024-01-08T22:13:37.759Z',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Jan+08+2024+23%3A13%3A37+GMT%2B0100+(Central+European+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=aa446b68-209d-47db-a8f5-dadce2bfa2d2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0',
        '_vid_t': 'aADyjsFF19jPGk8ikrsSfN/ZjZCWsY6zLfAVQvJSbvkrZq6x7Y8XCtlClrFOLzWOYVQwXAYEH14hrw==',
        'SL_C_23361dd035530_SID': '{"d0773bcb0ab063d8c124f0a1f1c2c35203fb926f":{"sessionId":"3ujb2Gk7zS8hEULSRShgd","visitorId":"jVscy5sEcxK4bX0cD83aT"}}',
        'mp_ea75e434d4b4d2405d79ed9d14bfc93b_mixpanel': '%7B%22distinct_id%22%3A%20%22DEMk8Qpuav8qXbDFH%22%2C%22%24device_id%22%3A%20%2218ceb227ccf120c-0375b816f6badf-26001951-e1000-18ceb227cd01411%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22DEMk8Qpuav8qXbDFH%22%7D',
        '_ga': 'GA1.1.1672589477.1704751954',
        '__hstc': '160404322.7635a87b45529bda5a7d9a6e1c85768d.1704751956098.1704751956098.1704780830642.2',
        '__hssc': '160404322.1.1704780830642',
        'ApifyProdUserId': 'DEMk8Qpuav8qXbDFH',
        '_ga_F50Z86TBGX': 'GS1.1.1704780827.2.1.1704780833.54.0.0',
        'intercom-session-kod1r788': 'eDlLdWNTWnZkUmtuZmhqMlNPSm44b0VQalRFdnRMSVVUaStBRG5SRDIzbzhyU2NqYVFzTWt1VHRRbTVTc3hkVS0tVFNqTGdNZDRyT3lSbU42bzVYNUpIdz09--1f42575305cfec8d33e2b93b43c0779be8410459',
        'AWSALB': 'drMM3StOELNtdkm5aqaRNVq1/o8umMzZMx8DQgXhfJ+r7zTuBCK/tEe1zql7NHFTIMGTDibh3ygeaFqAw5CmX2G36xhp66ipWv9dDbBwKxDXmDvJA5jp0+6c4sAO',
        'AWSALBCORS': 'drMM3StOELNtdkm5aqaRNVq1/o8umMzZMx8DQgXhfJ+r7zTuBCK/tEe1zql7NHFTIMGTDibh3ygeaFqAw5CmX2G36xhp66ipWv9dDbBwKxDXmDvJA5jp0+6c4sAO',
    }

    headers = {
        'authority': 'console.apify.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.1294268146.1704751954; ApifyUtk=hhVJTB8oOfnB85j9M; _gcl_au=1.1.1420136768.1704751955; ApifyAcqSrc=https://console.apify.com/; ApifyAcqRef=; SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; hubspotutk=7635a87b45529bda5a7d9a6e1c85768d; __hssrc=1; intercom-device-id-kod1r788=15a75f6b-c779-4c28-9583-577367862b94; OptanonAlertBoxClosed=2024-01-08T22:13:37.759Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jan+08+2024+23%3A13%3A37+GMT%2B0100+(Central+European+Standard+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=aa446b68-209d-47db-a8f5-dadce2bfa2d2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0; _vid_t=aADyjsFF19jPGk8ikrsSfN/ZjZCWsY6zLfAVQvJSbvkrZq6x7Y8XCtlClrFOLzWOYVQwXAYEH14hrw==; SL_C_23361dd035530_SID={"d0773bcb0ab063d8c124f0a1f1c2c35203fb926f":{"sessionId":"3ujb2Gk7zS8hEULSRShgd","visitorId":"jVscy5sEcxK4bX0cD83aT"}}; mp_ea75e434d4b4d2405d79ed9d14bfc93b_mixpanel=%7B%22distinct_id%22%3A%20%22DEMk8Qpuav8qXbDFH%22%2C%22%24device_id%22%3A%20%2218ceb227ccf120c-0375b816f6badf-26001951-e1000-18ceb227cd01411%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22DEMk8Qpuav8qXbDFH%22%7D; _ga=GA1.1.1672589477.1704751954; __hstc=160404322.7635a87b45529bda5a7d9a6e1c85768d.1704751956098.1704751956098.1704780830642.2; __hssc=160404322.1.1704780830642; ApifyProdUserId=DEMk8Qpuav8qXbDFH; _ga_F50Z86TBGX=GS1.1.1704780827.2.1.1704780833.54.0.0; intercom-session-kod1r788=eDlLdWNTWnZkUmtuZmhqMlNPSm44b0VQalRFdnRMSVVUaStBRG5SRDIzbzhyU2NqYVFzTWt1VHRRbTVTc3hkVS0tVFNqTGdNZDRyT3lSbU42bzVYNUpIdz09--1f42575305cfec8d33e2b93b43c0779be8410459; AWSALB=drMM3StOELNtdkm5aqaRNVq1/o8umMzZMx8DQgXhfJ+r7zTuBCK/tEe1zql7NHFTIMGTDibh3ygeaFqAw5CmX2G36xhp66ipWv9dDbBwKxDXmDvJA5jp0+6c4sAO; AWSALBCORS=drMM3StOELNtdkm5aqaRNVq1/o8umMzZMx8DQgXhfJ+r7zTuBCK/tEe1zql7NHFTIMGTDibh3ygeaFqAw5CmX2G36xhp66ipWv9dDbBwKxDXmDvJA5jp0+6c4sAO',
        'referer': 'https://apify.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get('https://console.apify.com/actors/moJRLRc85AitArpNN/console', cookies=cookies, headers=headers)

    with open('result.html', 'w') as file:
        file.write(response.text)


# test_3()
from pprint import pprint
def api_request():
    actor = "nFJndFXA5zjCTuudP"
    token = "apify_api_HnlGZwvslLSKmd4PgmQAwWyBxYrGdN0IdXmR"
    result = requests.get(f'https://api.apify.com/v2/acts/{actor}?token={token}')
    print(result.status_code)
    pprint(result.json())


# with open('test.txt', 'w', encoding='utf-8') as file:
#     file.write(test_data)
# print(test_data)
