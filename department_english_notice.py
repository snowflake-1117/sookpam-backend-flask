from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def print_list1():
    titles = browser.find_elements_by_css_selector('td.list_td1')
    list_len = len(titles)//5
    print('count list: '+str(list_len))
    for title in titles:
        try:
            a = title.find_element_by_css_selector("a")
            href = a.get_attribute("href")
            print("-", href)
            print("-",title.text)
            #test_click()
            browser.get(board_url)
            time.sleep(5)
        except NoSuchElementException:
            print("-",title.text)

    return;

def test_click():
    a = browser.find_element_by_css_selector('body > form:nth-child(2) > table > tbody > tr:nth-child(7) > td:nth-child(3) > a')
    href = a.get_attribute("href")
    print("-", href)
    a.click()
    time.sleep(5)
    span_list = browser.find_elements_by_css_selector('span')
    content = ""
    for span in span_list:
        if span.text:
            content = content + span.text + '\n'
    print('<content>\n',content)
    return

board_url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(board_url)
time.sleep(5)
print_list1()
browser.quit()

