import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Instagram:

    def __init__(self):
        self.browser = webdriver.Chrome(os.getcwd() + "/chromedriver").get("https://www.instagram.com")
        time.sleep(1)

    def login(self):
        NEXT_BUTTON_XPATH = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
        button = self.browser.find_element_by_xpath(NEXT_BUTTON_XPATH)
        button.click()

        user_name_form = self.browser.find_element_by_name("username")
        user_name_form.send_keys("aturner9967@gmail.com")

        password_form = self.browser.find_element_by_name("password")
        password_form.send_keys("C35ar3_7411")

        login_button = self.browser.find_element_by_css_selector("button._qv64e._gexxb._4tgw8._njrw0")
        login_button.click()
