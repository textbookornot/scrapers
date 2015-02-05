#######################################################################
#                               imports                               #
#######################################################################

import scrapy
import os
import time

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
AMAZON_URL = 'http://www.amazon.com/dp/{ASIN}/?tag={trackingID}'

#######################################################################
#                              selenium                               #
#######################################################################

browser = webdriver.Firefox()

def get_pages(bookstore_url):
    base_book_page_url = "http://www.bkstr.com/webapp/wcs/stores/servlet/CourseMaterialsResultsView?catalogId=10001&categoryId=9604&storeId=10161&langId=-1&programId=562&termId=100033801&divisionDisplayName=Stanford&departmentDisplayName={}&courseDisplayName={}&sectionDisplayName=01&demoKey=d&purpose=browse"
    book_page_urls = set()
    browser.get(bookstore_url)
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//select[@id="programIdSelect"]/option[@value="562"]').click()
    browser.find_element_by_xpath('//select[@id="divisionIdSelect"]/option[@value="Stanford"]').click()
    depts = browser.find_elements_by_xpath('//select[@id="departmentIdSelect"]/option')
    for subject in browser.find_elements_by_xpath('//select[@id="departmentIdSelect"]/option'):
        subject.click()
        time.sleep(5)
        subj = subject.get_attribute("value")
        body = browser.page_source.encode('utf-8')
        url = browser.current_url
        response = scrapy.http.HtmlResponse(url=url, body=body)

        # print subj
        for course in response.xpath('//select[@id="courseIdSelect"]/option/text()').extract()[1:]:
            # print course
            book_page_urls.add(base_book_page_url.format(subj, course.strip()))

    browser.close()
    return book_page_urls

#######################################################################
#                               spider                                #
#######################################################################

class StanfordBookSpider(scrapy.Spider):

    name = "stanford_books"
    start_urls = list(get_pages("http://www.bkstr.com/stanfordstore/shop/textbooks-and-course-materials"))
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_TRACKING_ID)

    def parse(self, response):
        print response.xpath('//p[@class="efCourseName"]/text()').extract()

