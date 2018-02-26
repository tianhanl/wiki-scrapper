import wiki
import re
import requests
import string
from bs4 import BeautifulSoup
from time import sleep

path = './pollings/'

domain = 'https://en.wikipedia.org'

link = 'https://en.wikipedia.org/wiki/Category:Opinion_polling_for_elections'


root = requests.get(link)

rootPage = BeautifulSoup(root.text, 'html.parser')

pollingLinks = rootPage.findAll('a', href=re.compile('polling', re.IGNORECASE))

count = 0
for pollingLink in pollingLinks:
    if pollingLink.attrs['href'] is not None:
        currLink = domain + pollingLink['href']
        print('currently working on lnik: ' + currLink)
        currTables = wiki.get_poll_tables(wiki.get_page_html_from_url(currLink))
        print('# of entries: ' + str(len(currTables)))
        if len(currTables) >= 1:
            tableName = pollingLink.get_text()
            # Replace puncutaion
            tableName = tableName.replace(',', ' ')
            # reformate the names
            tableName = tableName.lower().replace(' ', '_')
            wiki.save_tables(currTables, path + tableName + '.json')
    # Delay each request
    count += 1
    sleep(1)

print('parsed ' + str(count) + ' pages')
