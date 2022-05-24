import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from pymongo import MongoClient
from dateutil.parser import parse
import warnings
warnings.filterwarnings("ignore") # 경고문 제거

# 대부분 1년물이 존재하지만 1년물이 아닌 2년물이 존재하는 경우, 혹은 둘다 존재하지 않는 경우를 모두 고려
country_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']
investing_countries = ['australia', 'bahrain','brazil', None, None, 'canada', 'hong-kong',
                'china', 'czech-republic', None, 'germany', None, 'hungary', 'india', 'indonesia', 'israel',
                 'japan', 'jordan', None, 'malaysia', 'mexico', 'new-zealand',
                'norway', 'philippines', 'poland', 'russia', None, 'singapore', 'south-africa',
                None, 'switzerland', 'taiwan', 'thailand', 'turkey', None, 'uk', 'u.s.', 'vietnam', 'south-korea']

investing_countries_1Y = ['australia', 'bahrain','brazil', None, None, 'canada', 'hong-kong',
                'china', 'czech-republic', None, 'germany', None, 'hungary', 'india', 'indonesia', 'israel',
                 'japan', 'jordan', None, 'malaysia', 'mexico', None,
                'norway', 'philippines', 'poland', 'russia', None, 'singapore', None,
                None, 'switzerland', None, 'thailand', 'turkey', None, 'uk', 'u.s.', 'vietnam', 'south-korea']

investing_countries_2Y = [None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, 'new-zealand',
                None, None, None, None, None, None, 'south-africa',
                None, None, 'taiwan', None, None, None, None, None, None, 'south-korea']

imf_REF_AREA = ['AU', 'BH', 'BR', 'BN', 'KH', 'CA', 'HK', 'CN', 'CZ', 'DK', 'U2', 'FJ', 'HU', 'IN', 'ID', 'IL', 'JP', 'JO', 'KW', 'MY',
                'MX', 'NZ', 'NO', 'PH', 'PL', 'RU', 'SA', 'SG', 'ZA', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'GB', 'US', 'VN', 'KR']

class Interest_Crawling():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
        self.db = self.client['exchange']
        
        self.date_storage = self.date() + [None, None]  # 환율 데이터 경로(날짜 가져오기) ## 한국은 환율 데이터가 없으므로 인덱스 맞춰주기
        self.driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
        self.action = ActionChains(self.driver)
        
    def date(self):
        return [self.db[country].find_one()['date'] for country in country_name]
    
    def crawl(self):
        self.driver.get('https://google.com') # 구글 창 열기
        self.driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

        for i in range(39, len(investing_countries)+2): # 한국은 두번
            if i < 37:
                continue
            if i < 39:
                if investing_countries_1Y[i] != None:
                    country = investing_countries_1Y[i]
                    url = f'https://www.investing.com/rates-bonds/{country}-1-year-bond-yield-historical-data' # 1년물 채권 사이트
                elif investing_countries_2Y[i] != None:
                    country = investing_countries_2Y[i]
                    url = f'https://www.investing.com/rates-bonds/{country}-2-year-bond-yield-historical-data' # 2년물 채권 사이트
                else:
                    continue
            else: # 한국 1년 & 2년물
                country = 'south-korea'
                if i == 39:
                    url = 'https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data'
                elif i == 40:
                    url = 'https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data'
            
            self.driver.execute_script(f'window.open("{url}");') # 채권 과거 데이터 사이트 탭 열기
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[-1]) # 채권 사이트로 탭 이동
            try: # bond-yeild가 url 주소에 없는 사이트가 존재하므로 error메세지가 있을 경우 bond-yeild를 삭제하여 다시 사이트 열기
                self.driver.find_element_by_class_name('error404')
                self.driver.close()
                time.sleep(1)
                url2 = url.replace('-bond-yield', '')
                print(url2)
                time.sleep(2)
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
                self.driver.switch_to.window(self.driver.window_handles[-1])
                if bool(self.driver.find_element_by_class_name('error404')) == True:
                    self.driver.close()
                    url2 = url.replace('year', 'years')
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(5)
            except:
                pass
            self.driver.execute_script("window.scrollTo(0, 700)") # 밑으로 조금 스크롤
            try:
                exchange = self.date_storage[0].iloc[-1].replace('-', '/') # 환율 시작 날짜
                date = exchange[5:] + '/' + exchange[:4]
            except:
                date = '01/01/2000'
            time.sleep(15)
            try:
                self.driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
            except:pass
            
            try:
                date_input = self.driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
            except:
                self.driver.refresh()
                time.sleep(15)
                try:
                    self.driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
                except:pass
                date_input = self.driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
                
            start_date = self.driver.find_element_by_id('startDate') # 시작 날짜 입력
            start_date.clear()
            start_date.send_keys(date)
            time.sleep(5)
            self.driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
            time.sleep(10)

            tbody = self.driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
            table = tbody.find_element_by_tag_name('tbody')
            rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
            
            data = []
            for tr in rows:
                td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
                d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
                temp = {'date' : d, 'interest' : float(td[1].text), 'change' : float(td[5].text.replace('%',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
                data.append(temp)
            
            # 약 17년 동안의 데이터만 표시해주므로 나머지 날짜에 대한 데이터를 다시 크롤링
            try:
                self.driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
            except:pass
            connect_date = data[0]['date'].replace('-', '/')
            print(connect_date)
            connect_date = connect_date[5:] + '/' + connect_date[:4]
            print(connect_date)
            date_input = self.driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
            start_date = self.driver.find_element_by_id('startDate') # 시작 날짜 입력
            start_date.clear()
            start_date.send_keys(connect_date)
            time.sleep(5)
            self.driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
            time.sleep(10)
            
            tbody = self.driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
            table = tbody.find_element_by_tag_name('tbody')
            rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
            
            for tr in rows:
                td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
                d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
                if data[0]['date'] == d:
                    break
                temp = {'date' : d, 'interest' : float(td[1].text), 'change' : float(td[5].text.replace('%',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
                data.insert(0, temp)
                
            print(country) # 한국 나오면 끝
            self.driver.close()  #탭 닫기
            self.driver.switch_to.window(self.driver.window_handles[0])  #다시 이전 창(탭)으로 이동
            
            return data