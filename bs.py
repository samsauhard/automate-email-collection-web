from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys 
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt
import xlsxwriter

# a queue of urls to be crawled
new_urls = deque(['https://www.kijiji.ca/v-house-for-sale/owen-sound/sauble-beach-6-cottage-resort/1539822375'])

# a set of urls that we have already crawled
processed_urls = set()
w = []
# a set of crawled emails
emails = set()

counter = 1



while(True):
    for i in w:
       
        new_urls.append(i.get('href'))

    try:

# process urls one by one until we exhaust the queue
        while len(new_urls):
            # move next url from the queue to the set of processed urls
            url = new_urls.popleft()
            if url in processed_urls:    
                print('already')
            else:
                processed_urls.add(url)
                reqs = requests.get(url) 
                soup = BeautifulSoup(reqs.text, 'html.parser') 
                w = soup.find_all('a')
                # extract base url to resolve relative links
                # get url's content
                print("Processing %s" % url)
                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                    # ignore pages with errors
                    continue
                try:
                    # extract all email addresses and add them into the resulting set
                    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                    book_ro = open_workbook('EmailList.xls')
                    book = copy(book_ro)
                    for i in new_emails:
                        sheet1 = book.get_sheet(0)
                        sheet1.write(counter, 0, i)
                        book.save("EmailList.xls")
                        counter = counter+1
                        print(i)
                except:
                    print('error')
    except Exception as e:
        print(e)

        # create a beutiful soup for the html document
        
