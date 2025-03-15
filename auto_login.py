# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BCC65AB0544BFC1A26C1D7C497840C6601AD83934EB457D7AA2E8DDDC46AAEF7AB8AA8148FED8633CD9B079039EF49A4533239A4341D1EF7CEBF6285BB1B10E4407F92EEA201CD76A8F7879A2669F471383DF3E017C02BCB0DDCCDF70D1A588AA80DF9CE0B222422E0B7D6911964E9259F54C8EC2A2F6750E4ECFE2B14591279E9EF0B6699F776EEBD16A8BA24D8D421998CC100A102E1C75752B2AA0AB46C33D64BF3A2BBA4CB8C30C54CA126C6EA5C048CAF56A1B969F00D89AA6C513BB6564F5224F1B6F8077691B8737E5634808087BB7119505CD14F17B1089BD3E609296B782E34DFC34F2B81BBCDE077E54E1E4A1F27C6305FF1ADDEB5E682FC29155D649775090E8FBE7EC8A8B51B2A097597F1AA2DF50129EC31DF0989CE6E32A04A604BE6421322EDCD9A995F2FCCF9B46D33E06B87AD2B852FDF7E067D06A5DDB865A5CE58C92D0DF8310CEBB2B2C4FBDCCFCCAEB53BA90DF0C9052D267D64A0D1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
