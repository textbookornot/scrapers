#######################################################################
#                               imports                               #
#######################################################################

import scrapy
import os

from ton_scraper.utils import clean_string
from ton_scraper.items import Course

from selenium import webdriver

from amazon.api import AmazonAPI

#######################################################################
#                             access keys                             #
#######################################################################

AMAZON_TRACKING_ID = os.environ['AMAZON_TRACKING_ID']
AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']
AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY']

#######################################################################
#                              selenium                               #
#######################################################################

DRIVER_PATH = '/usr/bin/firefox'
browser = webdriver.Firefox(executable_path = DRIVER_PATH)

def get_pages(bookstore_url):
    book_pages = {}
    browser.get(bookstore_url)
    browser.find_element_by_xpath('//select[@id="programIdSelect"]/option[@value="562"]').click()
    browser.find_element_by_xpath('//select[@id="divisionIdSelect"]/option[@value="Stanford"]').click()
    depts = browser.find_elements_by_xpath('//select[@id="departmentIdSelect"]/option')[1:]
    for subject in depts:
        courses = browser.find_elements_by_xpath('//select[@id="courseIdSelect"]/option')[1:]
        for course in courses:



#######################################################################
#                               spider                                #
#######################################################################

class StanfordBookSpider(scrapy.Spider):
    pass
