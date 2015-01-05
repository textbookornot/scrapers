#######################################################################
#                               imports                               #
#######################################################################

import scrapy
from ton_scraper.utils import clean_string
from ton_scraper.items import Course

#######################################################################
#                               spider                                #
#######################################################################

class StanfordCourseSpider(scrapy.Spider):
    name = "StanfordCourseSpider"
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

            # instructors
            instructors = course.xpath('div[@class="courseAttributes"][2]//a[@class="instructorLink"]/text()').extract()
            item['instructors'] = [inst.strip()[:-5] for inst in instructors if inst.strip() != ""] if instructors else None

            # continue only for classes with 5 instructors or less (avoid thesis, grad courses)
            if item['instructors'] and len(item['instructors']) < 6:

                # scrape the course subject, number, and title
                course_code = course.xpath('h2/span[@class="courseNumber"]/text()').extract()[0][:-1].split()
                item['subject'] = course_code[0]
                item['number'] = course_code[1]
                item['title'] = course.xpath('h2/span[@class="courseTitle"]/text()').extract()[0]

                # scrape the description
                description = course.xpath('div[@class="courseDescription"]/descendant-or-self::*/text()').extract()
                item['description'] = clean_string("".join(description)) if description else None

                # scrape the units
                attributes = course.xpath('div[@class="courseAttributes"][1]//text()').extract()[0]
                units = attributes[attributes.find('Units:') + 7 : ].split('|')[0].strip().split('-')
                item['min_units'] = int(units[0])
                item['max_units'] = int(units[1]) if len(units) > 1 else int(units[0])

                item['school'] = "stanford"

                yield item

        # iterate through all of the pages and scrape them
        for url in response.xpath('//div[@id="pagination"]/a[contains(text(), "next")]/@href').extract():
            yield scrapy.Request("".join([self.start_urls[0], url]), callback=self.parse_subject)
