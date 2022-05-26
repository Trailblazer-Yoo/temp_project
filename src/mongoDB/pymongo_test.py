import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import warnings
from pymongo import MongoClient
import pandas as pd

warnings.filterwarnings("ignore")
#################################################  크롤링 파트  #######################################################

class exchange():
    def __init__(self):
        pass
            
    def crawling(self, country_name):
        driver = webdriver.Chrome('/Users/yuseonjong/chromedriver')
        driver.get('https://google.com')
        driver.maximize_window()
        driver.execute_script('window.open("https://spot.wooribank.com/pot/Dream?withyou=FXXRT0014");')  ### 우리은행 환율 사이트
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[-1]) ## 우리은행 탭으로 이동

        #날짜 선택(제일 처음)
        select_year = Select(driver.find_element_by_id('START_DATEY')) # Select 함수를 이용하여 드롭 다운 메뉴에서 요소 선택
        select_month = Select(driver.find_element_by_id('START_DATEM'))
        select_day = Select(driver.find_element_by_id('START_DATED'))
        
        date = ['2022', '01', '02']
        select_year.select_by_visible_text(date[0]) # 연
        select_month.select_by_visible_text(date[1]) # 월
        select_day.select_by_visible_text(date[2]) # 일
            

        # 국가 선택
        select = Select(driver.find_element_by_id('id01')) # Select 함수를 이용하여 드롭 다운 메뉴에서 요소 선택
        select.select_by_visible_text(country_name) # 눈에 보이는 텍스트로 접근

        driver.find_element_by_xpath('//*[@id="frm"]/fieldset/div/span/input').click() # 조회 클릭
        print('조회 선택했슴둥')
        time.sleep(15)

        table = driver.find_element_by_xpath('//*[@id="fxprint"]/table/tbody') # 테이블 접근
        rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
    
        data_list = []
        for tr in rows:
            td = tr.find_elements_by_tag_name("td") # td 전체 찾기
            data = {'date' : td[0].text.replace('.', '-') , 'buy' : float(td[3].text.replace(',','')), 'standard' : float(td[6].text.replace(',',''))}
            data_list.append(data)
        driver.quit()
        
        return sorted(data_list, key=lambda x: x['date'])
    
ex = exchange()
data = ex.crawling('USD(미국)')
print(data)

host = '35.78.27.97'
port = '27017'
client = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 27017 포트로 들어가서 aws의 DB 와 연결해준다.
print(client.list_database_names()) # 현재 데이터베이스 목록 출력
db = client['exchange']


