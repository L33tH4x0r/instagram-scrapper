class ParkUrls:
    from urllib2 import urlopen as uReq
    from bs4 import BeautifulSoup as soup

    def __init__(self, browser):
        self.browser = browser

    def get(self):
        parks = self.get_park_names()
        parks_list = [["Park", "Url"]]

        for park in parks:
            parks_list.append([park, self.go_to_national_park(park)])

        self.write_csv_file(parks_list)

    def get_park_names(self):
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

    def go_to_national_park(self, park):
        search_bar = self.browser.find_element_by_css_selector("input._avvq0._o716c")
        search_bar.clear()
        time.sleep(1)
        search_bar.send_keys(park)
        time.sleep(2)
        return self.get_url(park)

    def get_url(self, park):
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

    def write_csv_file(self, parks_list):
        fo = open("national_parks.csv", "wb")
        for park in parks_list:
            if park[0] is not None:
                fo.write(park[0])
            fo.write(", ")
            if park[1] is not None:
                fo.write(park[1])
            fo.write("\n")

        fo.close()
