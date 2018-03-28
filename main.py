from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
import csv
import sys
import psycopg2
import os
import sys

# Globals
global password
global username
global csv
global browser
global cur
global con
global instagram_base_url
instagram_base_url = "https://www.instagram.com"

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
        parks.append(row.contents[1].contents[0].contents[0].encode('ascii', 'ignore') + " National Park")
    fo = open("national_parks", "wb")
    for park in parks:
        fo.write(park)
        fo.write("\n")

    fo.close()

    return parks

def instagram_login():
    NEXT_BUTTON_XPATH = '//a[@href="/accounts/login/"]'
    button = browser.find_element_by_xpath(NEXT_BUTTON_XPATH)
    button.click()

    user_name_form = browser.find_element_by_name("username")
    user_name_form.send_keys("aturner9967@gmail.com")

    password_form = browser.find_element_by_name("password")
    password_form.send_keys("C35ar3_7411")

    login_button = browser.find_element_by_css_selector("button._qv64e._gexxb._4tgw8._njrw0")
    login_button.click()

def write_csv_file(parks_list):
    fo = open("national_parks", "wb")
    for park in parks_list:
        if park[0] is not None:
            fo.write(park[0])
        fo.write(", ")
        if park[1] is not None:
            fo.write(park[1])
        fo.write("\n")

    fo.close()

def get_url(park):
    root = browser.find_element_by_id("react-root")
    root_html = root.get_attribute('innerHTML')
    react_soup = soup(root_html, "html.parser")

    links = []
    for div in react_soup.find_all('a', href=True):
        if "explore" in div["href"] and "locations"in div["href"]:
            links.append(div)

    for link in links[0:-2]:
        if link.find_all("span") is not None and link.find_all("span")[0] is not None and link.find_all("span")[0].contents is not None and link.find_all("span")[0].contents[0].encode('ascii', 'ignore') == park:
            return instagram_base_url + link["href"].encode('ascii', 'ignore')

def go_to_national_park(park):
    search_bar = browser.find_element_by_css_selector("input._avvq0._o716c")
    search_bar.clear()
    time.sleep(1)
    search_bar.send_keys(park)
    time.sleep(2)
    return get_url(park)

def get_parks_urls():
    parks = get_park_names()
    parks_list = [["Park", "Url"]]

    for park in parks:
        parks_list.append([park, go_to_national_park(park)])

    write_csv_file(parks_list)

    print parks_list

def setup_database(username, password):
    # Check if database exists
    con = psycopg2.connect("dbname='instagramresults' user='austin' host='localhost' password='%s'" % password )
    cur = con.cursor()
    cur.execute('SELECT 1 from Post')
    # try:
    # except:
        # print "Database Not found"
def check_parameters():
    password = ''
    username = ''
    for arg in sys.argv:
        if arg == "csv":
            csv = True
        else if 'password' in arg:
            password = arg.split("=")[-1]
        else if 'username' in arg:
            username = arg.split("=")[-1]

    if password = '':
        print "You need to supply a password"
        sys.exit()
    else if username = '':
        print "You need to supply a username"
        sys.exit()

if __name__ == "__main__":
    check_paramters()
    setup_database(username, password)

    browser = webdriver.Chrome(os.getcwd() + "/chromedriver")
    browser.get(instagram_base_url)

    if csv:
        get_parks_urls()
    instagram_login()
