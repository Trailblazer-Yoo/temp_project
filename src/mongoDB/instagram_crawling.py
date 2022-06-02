import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import warnings
warnings.filterwarnings("ignore") # 경고문 제거
from selenium import webdriver


driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
ac = ActionChains(driver)
driver.get('https://www.instagram.com/') # 구글 창 열기
driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

time.sleep(3)

login_in = driver.find_elements_by_class_name('_2hvTZ.pexuQ.zyHYP')
ac.move_to_element(to_element=login_in[0]).click().send_keys('01064749591').perform()  # 아이디
ac.move_to_element(to_element=login_in[1]).click().send_keys('!!yousj35710').perform() # 비밀번호
time.sleep(1)
ac.move_to_element(to_element=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')).click().perform() # 접속

time.sleep(5)

text_bar = driver.find_element_by_class_name('XTCLo.d_djL.DljaH') # 상단 입력창
ac.move_to_element(to_element=text_bar).click().perform()
ac.move_to_element(to_element=text_bar).send_keys('#도쿄맛집').perform()
time.sleep(3)
visible_text_bar = driver.find_element_by_xpath()
ac.move_to_element(to_element=visible_text_bar).click().send_keys(Keys.ENTER).perform()

time.sleep(5)

# bs_obj = BeautifulStoneSoup(driver.page_source)
# post_obj = bs_obj.find_all('div', {'class': 'v1Nh3 kIKUG _bz0w'}) # 모든 게시물 파싱

# for post in post_obj:
#     print(post.find('a'))
    


while True:
    pass