import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
from DepartmentUrlData import DepartmentUrlData
from Record import Record
from DBManager import DBManager


class Wiz5Departments:
    base_url = ".sookmyung.ac.kr/wiz5/wizard/frames/server_sub.html?"

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.url_key_list = []
        self.category_list = []
        self.division_list = []
        self.record_list = []

    def start(self):
        self.set_department_data_list()

        for url_data, category, division in zip(self.url_key_list, self.category_list, self.division_list):
            url = self.get_url(url_data)
            self.browser.get(url)

            number_list = self.browser.find_elements_by_xpath("//div[2]/form/table/tbody/tr/td[2]")
            last_notice_number = self.get_last_notice_number(number_list)
            start_notice_page = url_data.page
            last_notice_page = self.get_last_page(last_notice_number, 15)

            self.scrap_current_to_max_page(start_notice_page, last_notice_page, url_data, category, division)
            self.save_record_list_to_db()

    def quit(self):
        self.browser.quit()

    def get_url(self, url_data, page=1):
        url = "https://" + url_data.domain_name + self.base_url
        url += "home_id=" + url_data.home_id
        url += "&menu_seq=" + str(url_data.menu_seq)
        url += "&handle=" + str(url_data.handle)
        url += "&board_id=" + str(url_data.board_id)
        url += "&categoryId=" + str(url_data.category_id)
        url += "&page=" + str(page)
        url += "&siteId=" + url_data.site_id
        return url

    def set_department_data_list(self):
        data = json.load(open('wiz5_departments.json'))
        for i in data:
            department_url_key = self.get_department_url_data(i)
            self.url_key_list.append(department_url_key)
            self.category_list.append(i["department"])
            self.division_list.append(i["type"])

    def get_department_url_data(self, item):
        url_data = DepartmentUrlData()
        url_data.college = item["college"]
        url_data.department = item["department"]
        url_data.domain_name = item["domain_name"]
        url_data.home_id = item["home_id"]
        url_data.menu_seq = item["menu_seq"]
        url_data.handle = item["handle"]
        url_data.board_id = item["board_id"]
        url_data.category_id = item["categoryId"]
        url_data.page = item["page"]
        url_data.site_id = item["siteId"]
        url_data.type = item["type"]
        return url_data

    def get_last_notice_number(self, number_list):
        for number in number_list:
            last_number = number.text
            if last_number.isdigit():
                return int(last_number)

    def get_last_page(self, last_number, page_notices_count):
        if last_number % page_notices_count != 0:
            return last_number // page_notices_count + 1
        else:
            return last_number // page_notices_count

    def scrap_current_to_max_page(self, start_page, last_page, url_data, category, division):
        current_page = start_page
        while current_page <= last_page:
            print("page: " + str(current_page))
            current_page += 1
            self.set_notices_data(category, division)
            self.browser.get(self.get_url(url_data, current_page))

    def set_notices_data(self, category, division):
        notice_href_list = self.browser.find_elements_by_css_selector("td.title > a")
        notice_number_list = self.browser.find_elements_by_css_selector(
            "#board-container > div.list > form > table > tbody > tr > td:nth-child(2)")
        for notice, number in zip(notice_href_list, notice_number_list):
            if number.text.isdigit():
                notice_item_url = notice.get_attribute("href")
                notice_item_response = urllib.request.urlopen(notice_item_url)
                soup_notice = BeautifulSoup(notice_item_response, "html.parser")

                record = self.get_record_data(category, division, soup_notice)
                self.record_list.append(record)

                time.sleep(1)

    def get_record_data(self, category, division, soup_notice):
        record = Record()
        record.id = int(soup_notice.select_one("p.no").text.replace("글번호 : ", ""))
        record.title = self.get_content_output(soup_notice.select_one("head > title").text)
        record.content = self.get_content_output(soup_notice.select("td > div").text)
        record.category = category
        record.division = division
        record.view = int(soup_notice.select_one("td.no").text)
        record.date = datetime.strptime(soup_notice.select_one("td.date").text.strip(), "%Y-%m-%d").date()
        return record

    def get_content_output(self, content):
        if content is None:
            return ""
        stripped = str(content).strip()
        stripped = re.sub(r'<[^>]*?>', '', stripped)
        pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        return pattern.sub(u'\uFFFD', stripped)

    def save_record_list_to_db(self):
        for i in self.record_list:
            DBManager.insert(i)
