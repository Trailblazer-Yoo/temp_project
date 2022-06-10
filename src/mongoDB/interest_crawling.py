import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from pymongo import MongoClient
from dateutil.parser import parse
import warnings
warnings.filterwarnings("ignore") # 경고문 제거

# 대부분 1년물이 존재하지만 1년물이 아닌 2년물이 존재하는 경우, 혹은 둘다 존재하지 않는 경우를 모두 고려
mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']
investing_countries = ['australia', 'bahrain','brazil', None, None, 'canada', 'hong-kong',
                'china', 'czech-republic', None, 'germany', None, 'hungary', 'india', 'indonesia', 'israel',
                 'japan', 'jordan', None, 'malaysia', 'mexico', 'new-zealand',
                'norway', 'philippines', 'poland', 'russia', None, 'singapore', 'south-africa',
                None, 'switzerland', 'taiwan', 'thailand', 'turkey', None, 'uk', 'u.s.', 'vietnam', 'south-korea']

investing_countries_1Y = ['australia', None,'brazil', None, None, 'canada', 'hong-kong',
                'china', 'czech-republic', None, 'germany', None, 'hungary', 'india', 'indonesia', 'israel',
                 'japan', None, None, 'malaysia', 'mexico', None,
                'norway', 'philippines', 'poland', 'russia', None, 'singapore', None,
                None, 'switzerland', None, 'thailand', 'turkey', None, 'uk', None, 'vietnam', 'south-korea']

investing_countries_2Y = [None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, 'new-zealand',
                None, None, None, None, None, None, 'south-africa',
                None, None, 'taiwan', None, None, None, None, 'u.s.', None, 'south-korea']

imf_REF_AREA = ['AU', 'BH', 'BR', 'BN', 'KH', 'CA', 'HK', 'CN', 'CZ', 'DK', 'U2', 'FJ', 'HU', 'IN', 'ID', 'IL', 'JP', 'JO', 'KW', 'MY',
                'MX', 'NZ', 'NO', 'PH', 'PL', 'RU', 'SA', 'SG', 'ZA', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'GB', 'US', 'VN', 'KR']

class Interest_Crawling():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
        self.db = self.client['exchange']
        
        dt = self.date()  # 환율 데이터 경로(날짜 가져오기) ## 한국은 환율 데이터가 없으므로 인덱스 맞춰주기
        try:
            self.date_storage = dt + ['2003-01-01', '2003-01-01']
        except:
            print('아직 환율 데이터 크롤링이 완료되지 않았습니다.')
        
    def date(self):
        try:
            return [self.db[country].find_one()['date'] for country in mongo_name]
        except:
            print('환율 데이터를 업데이트 해주시기 바랍니다.')
    
    def initiate(self, i):
        print('데이터를 생성합니다.')
        driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
        ac = ActionChains(driver)
        driver.get('https://google.com') # 구글 창 열기
        driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

        if i < 38:
            if investing_countries_1Y[i] != None:
                country = investing_countries_1Y[i]
                url = f'https://www.investing.com/rates-bonds/{country}-1-year-bond-yield-historical-data' # 1년물 채권 사이트
                condition = 1
            elif investing_countries_2Y[i] != None:
                country = investing_countries_2Y[i]
                url = f'https://www.investing.com/rates-bonds/{country}-2-year-bond-yield-historical-data' # 2년물 채권 사이트
                condition = 2
            else:
                return
        else: # 한국 1년 & 2년물
            country = 'south-korea'
            if i == 38:
                url = 'https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data'
                condition = 1
            elif i == 39:
                url = 'https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data'
                condition = 2
        
        driver.execute_script(f'window.open("{url}");') # 채권 과거 데이터 사이트 탭 열기
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1]) # 채권 사이트로 탭 이동
        try: # bond-yeild가 url 주소에 없는 사이트가 존재하므로 error메세지가 있을 경우 bond-yeild를 삭제하여 다시 사이트 열기
            driver.find_element_by_class_name('error404')
            driver.close()
            time.sleep(1)
            url2 = url.replace('-bond-yield', '')
            print(url2)
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
            driver.switch_to.window(driver.window_handles[-1])
            if bool(driver.find_element_by_class_name('error404')) == True:
                driver.close()
                url2 = url.replace('year', 'years')
                driver.switch_to.window(driver.window_handles[0])
                driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
                driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)
        except:
            pass
        driver.execute_script("window.scrollTo(0, 700)") # 밑으로 조금 스크롤
        try:
            exchange = self.date_storage[i].replace('-', '/') # 환율 시작 날짜
            date = exchange[5:] + '/' + exchange[:4]
        except:
            date = '01/01/2000'
        time.sleep(20)
        try:
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
        except:pass
        
        try:
            date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
        except:
            driver.refresh()
            time.sleep(20)
            try:
                close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
                ac.move_to_element(to_element=close_button).click().perform()
            except:pass
            date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
        time.sleep(5)
        try:
            driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
        except:pass
        start_date = driver.find_element_by_id('startDate') # 시작 날짜 입력
        start_date.clear()
        start_date.send_keys(date)
        time.sleep(1)
        driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
        time.sleep(10)
        
        tbody = driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
        table = tbody.find_element_by_tag_name('tbody')
        rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
        try:
            driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
        except:pass
        data1 = []
        for tr in rows:
            td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
            d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
            temp = {'date' : d, f'interest{condition}Y' : float(td[1].text), f'change{condition}Y' : float(td[5].text.replace('%','').replace(',',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
            data1.append(temp)
        
        # 약 17년 동안의 데이터만 표시해주므로 나머지 날짜에 대한 데이터를 다시 크롤링
        try:
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
        except:pass
        connect_date = data1[0]['date'].replace('-', '/')
        connect_date = connect_date[5:] + '/' + connect_date[:4]
        print(connect_date)
        date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
        start_date = driver.find_element_by_id('startDate') # 시작 날짜 입력
        start_date.clear()
        start_date.send_keys(connect_date)
        time.sleep(5)
        try:
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
        except:pass
        driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
        time.sleep(10)
        
        tbody = driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
        table = tbody.find_element_by_tag_name('tbody')
        rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
        try:
            driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
        except:pass
        data2 = []
        for tr in rows:
            td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
            d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
            if data1[0]['date'] == d:
                break
            temp = {'date' : d, f'interest{condition}Y' : float(td[1].text), f'change{condition}Y' : float(td[5].text.replace('%','').replace(',',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
            data2.append(temp)
        data = data2 + data1
            
        print(country) # 한국 나오면 끝
        driver.quit()  #탭 닫기
        
        return sorted(data, key=lambda x: x['date']) 
    
    def update(self, i, last_date):
        print('업데이트를 진행합니다.')
        driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
        ac = ActionChains(driver)
        driver.get('https://google.com') # 구글 창 열기
        driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

        if i < 39:
            if investing_countries_1Y[i] != None:
                country = investing_countries_1Y[i]
                url = f'https://www.investing.com/rates-bonds/{country}-1-year-bond-yield-historical-data' # 1년물 채권 사이트
                condition = 1
            elif investing_countries_2Y[i] != None:
                country = investing_countries_2Y[i]
                url = f'https://www.investing.com/rates-bonds/{country}-2-year-bond-yield-historical-data' # 2년물 채권 사이트
                condition = 2
            else:
                return
        else: # 한국 1년 & 2년물
            country = 'south-korea'
            if i == 39:
                url = 'https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data'
                condition = 1
            elif i == 40:
                url = 'https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data'
                condition = 2
        
        driver.execute_script(f'window.open("{url}");') # 채권 과거 데이터 사이트 탭 열기
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1]) # 채권 사이트로 탭 이동
        try: # bond-yeild가 url 주소에 없는 사이트가 존재하므로 error메세지가 있을 경우 bond-yeild를 삭제하여 다시 사이트 열기
            driver.find_element_by_class_name('error404')
            driver.close()
            time.sleep(1)
            url2 = url.replace('-bond-yield', '')
            print(url2)
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
            driver.switch_to.window(driver.window_handles[-1])
            if bool(driver.find_element_by_class_name('error404')) == True:
                driver.close()
                url2 = url.replace('year', 'years')
                driver.switch_to.window(driver.window_handles[0])
                driver.execute_script(f'window.open("{url2}");') # 채권 과거 데이터 사이트 탭 열기
                driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)
        except:
            pass
        driver.execute_script("window.scrollTo(0, 700)") # 밑으로 조금 스크롤
        try:
            exchange = last_date.replace('-', '/') # 환율 시작 날짜
            date = exchange[5:] + '/' + exchange[:4]
        except:
            date = '01/01/2000' 
        time.sleep(20)
        try:
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
        except:pass
        date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
        
        try:
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
        except:pass
        start_date = driver.find_element_by_id('startDate') # 시작 날짜 입력
        start_date.clear()
        start_date.send_keys(date)
        time.sleep(1)
        try:
            driver.find_element_by_class_name('newBtn.Arrow.LightGray.float_lang_base_2.disabled').click() # 바뀐 날짜 적용
            return
        except:
            driver.find_element_by_class_name('newBtn.Arrow.LightGray.float_lang_base_2').click() # 바뀐 날짜 적용
        time.sleep(10)
        
        tbody = driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
        table = tbody.find_element_by_tag_name('tbody')
        rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
        try:
            driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
        except:pass
        data = []
        for tr in rows:
            td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
            d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
            temp = {'date' : d, f'interest{condition}Y' : float(td[1].text), f'change{condition}Y' : float(td[5].text.replace('%','').replace(',',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
            data.append(temp)
        
        return sorted(data, key=lambda x: x['date'])   
    