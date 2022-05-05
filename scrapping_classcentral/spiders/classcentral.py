import re
from scrapy.http import Request
import scrapy
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

class ClasscentralSpider(scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject="Data Science"):
        self.subject = subject
    
    def parse(self, response):
        #self.log('Scrapping %s courses...', self.subject)
        subject_url = response.xpath('//h3/a[contains(@title, "' + self.subject + '")]/@href').extract_first()
        abs_subject_url = response.urljoin(subject_url)
        yield Request(abs_subject_url,callback=self.parse_subject)
    
    def parse_subject(self, response):
        options = Options()
        driver_path = '###' #Your Chrome Webdriver Path
        browser_path = '###' #Your Google Chrome Path
        options.binary_location = browser_path

        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)
        self.driver.get(response.url)

        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)

        self.new_src = None
        self.new_response = None

        while True:
            # click next link
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="hidden small-up-inline-block"]')))
                #element.click()
                self.driver.execute_script("arguments[0].click();", element)
                self.new_src = self.driver.page_source
                self.new_response = response.replace(body=self.new_src)
            except TimeoutException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break
            
        # grab the data
        course_url = self.new_response.xpath('//a[@class="color-charcoal course-name"]/@href').extract()

        for url in course_url:
            abs_url = 'https://www.classcentral.com' + url
            yield Request (abs_url, callback=self.parse_course)
                    
    def parse_course(self,response):
        course_name = response.xpath('//h1[@class="head-2 medium-up-head-1 small-down-margin-bottom-xsmall"]/text()').extract_first()
        platform = response.xpath('//a[contains(@data-overlay-trigger, "provider")]/text()').extract_first()
        language = response.xpath('//a[contains(@href, "language") and @class="text-2 color-charcoal line-tight"]/text()').extract_first()
        language = re.sub(r"[\n\t\s]*", "", language)

        yield {
            'course_name': course_name,
            'platform': platform,
            'language': language,
            'url': response.url
        }
