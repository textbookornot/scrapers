#######################################################################
#                               imports                               #
#######################################################################

import scrapy
from ton_scraper.utils import clean_string
from ton_scraper.items import Subject

#######################################################################
#                               spider                                #
#######################################################################

class StanfordSubjectSpider(scrapy.Spider):
    name = "StanfordSubjectSpider"
    allowed_domains = ["explorecourses.stanford.edu"]
    start_urls = ["http://explorecourses.stanford.edu"]

    # to contain all subjects and their abbreviations
    subject_list = {}

    def parse(self, response):

        # url that will be modified to access all of the majors.
        # makes sure that all term filters are enabled.
        base_url = 'http://explorecourses.stanford.edu/search?filter-term-Summer=on&filter-coursestatus-Active=on&filter-term-Spring=on&filter-term-Winter=on&filter-term-Autumn=on&page=0&q={subject}&view=catalog&filter-departmentcode-{subject}=on&filter-catalognumber-{subject}=on&academicYear=&collapse='

        # parse main page and create dictionary of subject codes mapped to subject names
        for subject in response.xpath(
                '//div[@class="departmentsContainer"]//a/text()'
        ).extract():
            self.subject_list[subject[subject.rfind('(')+1 : subject.rfind(')')]] = subject.split(' (')[0].strip()

        # use subject codes to scrape all subject urls
        for code in self.subject_list:
            yield scrapy.Request(base_url.format(subject=code), callback=self.parse_subject)


    def parse_subject(self, response):

        # parse all of the courses on the page
        for course in response.xpath('//div[@class="courseInfo"]'):

            item = Course()

            # scrape the course number and titles
            item['number'] = course.xpath('h2/span[@class="courseNumber"]/text()').extract()[0][:-1]
            item['title'] = course.xpath('h2/span[@class="courseTitle"]/text()').extract()[0]

            # set subject code and subject title
            item['subject'] = item['number'].split()[0]
            #item['subject_title'] = self.subject_list[item['subject_code']]

            # scrape the description
            description = course.xpath('div[@class="courseDescription"]/text()').extract()
            if description:
                item['description'] = clean_string("".join(description))

            # scrape the units
            attributes = course.xpath('div[@class="courseAttributes"][1]//text()').extract()[0]
            units = attributes[attributes.rfind('Units:')+6 : ].split('|')[0].strip()
            item['units'] = units

            # scrape the list of instructors into a list which is stripped
            instructors = course.xpath('div[@class="courseAttributes"]/a/text()').extract()
            item['instructors'] = [instructor.strip() for instructor in instructors if instructor.strip() != ""]

            # return only classes with 3 or less instructors
            if item['instructors'] and len(item['instructors']) < 8:
                yield item

        # iterate through all of the pages and scrape them
        for url in response.xpath('//div[@id="pagination"]/a[contains(text(), "next")]/@href').extract():
            yield scrapy.Request("".join([self.start_urls[0], url]), callback=self.parse_subject)
