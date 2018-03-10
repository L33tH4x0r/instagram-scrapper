from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup

wikipedia_url = "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States"
instagram_base_url = "https://www.instagram.com/"

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
