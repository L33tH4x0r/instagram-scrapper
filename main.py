from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver

get_park_names()

browser = webdriver.Chrome("/home/austin/Projects/social_networks/instagram-scrapper/chromedriver")
browser.get('https://instagram.com/')

instagram_login(browser)

instagram_base_url = "https://www.instagram.com/"

def get_park_names():
    wikipedia_url = "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States"
    wikipedia_client = uReq(wikipedia_url)
    wikipedia_html = wikipedia_client.read()
    wikipedia_client.close()
    wikipedia_soup = soup(wikipedia_html, "html.parser")

    park_rows = wikipedia_soup.table.find_all('tr')
    park_rows.pop(0)
    num_parks = len(park_rows)
    parks = []
    for row in park_rows:
        parks.append(row.contents[1].contents[0].contents[0].encode('ascii', 'ignore'))
    fo = open("national_parks", "wb")
    for park in parks:
        fo.write(park)
        fo.write("\n")

    fo.close()

def instagram_login(browser):
    NEXT_BUTTON_XPATH = '//a[@href="/accounts/login/"]'
    button = browser.find_element_by_xpath(NEXT_BUTTON_XPATH)
    button.click()
