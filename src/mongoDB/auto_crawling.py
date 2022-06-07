from datetime import datetime, timedelta
import schedule
from pymongo import MongoClient
import pandas as pd
import time
import warnings
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import warnings
warnings.filterwarnings("ignore")

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

imf_counties = ['Australia', 'Bahrain, Kingdom of', 'Brazil', 'Brunei Darussalam', 'Cambodia','Canada', 'China, P.R.: Hong Kong',
                'China, P.R.: Mainland', 'Czech Rep.', 'Denmark', 'Euro Area', 'Fiji, Rep. of', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland, Rep. of', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Arab Emirates', 'United Kingdom', 'United States', 'Vietnam', 'Korea, Rep. of']

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


date_Dict = {0 : '월요일', 1 : '화요일', 2 : '수요일', 3: '목요일',
             4 : '금요알', 5 : '토요일', 6 : '일요일'}

class Interest_Crawling():
    def __init__(self):
        host = '35.78.27.97'
        port = '27017'
        self.client = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
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
        display = Display(visible=0, size=(1024, 768))   # aws 서버에서 브라우저 실행
        display.start()
 
        path = '/home/ubuntu/chromedriver' # 우분투에 설치한 크롬 드라이버
        driver = webdriver.Chrome(path)
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
        display = Display(visible=0, size=(1024, 768))   # aws 서버에서 브라우저 실행
        display.start()
 
        path = '/home/ubuntu/chromedriver' # 우분투에 설치한 크롬 드라이버
        driver = webdriver.Chrome(path)
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
            close_button = driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser') # 광고 배너 닫기
            ac.move_to_element(to_element=close_button).click().perform()
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
        data = []
        for tr in rows:
            td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
            d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
            temp = {'date' : d, f'interest{condition}Y' : float(td[1].text), f'change{condition}Y' : float(td[5].text.replace('%','').replace(',',''))} # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
            data.append(temp)
        
        return sorted(data, key=lambda x: x['date'])
        
class exchange():
    def __init__(self):
        pass
            
    def country(self, country_name, date=None):
        display = Display(visible=0, size=(1024, 768))   # aws 서버에서 브라우저 실행
        display.start()
 
        path = '/home/ubuntu/chromedriver' # 우분투에 설치한 크롬 드라이버
        driver = webdriver.Chrome(path)
        driver.get("https://spot.wooribank.com/pot/Dream?withyou=FXXRT0014")   ### 우리은행 환율 사이트
        driver.maximize_window() 
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[-1]) ## 우리은행 탭으로 이동

        #날짜 선택(제일 처음)
        select_year = Select(driver.find_element_by_id('START_DATEY'))
        select_month = Select(driver.find_element_by_id('START_DATEM'))
        select_day = Select(driver.find_element_by_id('START_DATED'))
        if not date:
            select_year.select_by_index(0) # 2000년 선택
            select_month.select_by_index(0) # 1월 선택
            select_day.select_by_index(0) # 1일 선택
        else:
            date = date.split('-')
            select_year.select_by_visible_text(date[0])
            select_month.select_by_visible_text(date[1])
            select_day.select_by_visible_text(date[2])
            

        # 국가 선택
        select = Select(driver.find_element_by_id('id01')) # Select 함수를 이용하여 드롭 다운 메뉴에서 요소 선택
        select.select_by_visible_text(country_name) # 눈에 보이는 텍스트로 접근

        # country_index = self.investing_countries.find(country_name)
        # select.select_by_index(country_index) # 인덱스로 접근

        driver.find_element_by_xpath('//*[@id="frm"]/fieldset/div/span/input').click() # 조회 클릭
        print('조회 선택했슴둥')
        time.sleep(30)

        # country_name = driver.find_element_by_xpath('//*[@id="fxprint"]/div/div/dl/dd[2]').text # 국가명 추출
        table = driver.find_element_by_xpath('//*[@id="fxprint"]/table/tbody') # 테이블 접근
        rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
    
        data_list = []
        for tr in rows:
            try:
                td = tr.find_elements_by_tag_name("td") # td 전체 찾기
                data = {'date' : td[0].text.replace('.', '-') , 'buy' : float(td[3].text.replace(',','')), 'standard' : float(td[6].text.replace(',',''))}
                data_list.append(data)
            except:pass
        driver.quit()
        
        return sorted(data_list, key=lambda x: x['date'])
        
class DBUpdater_ex():
    def __init__(self):
        self.exchange_countries = ['AUD(호주)', 'BHD(바레인)', 'BRL(브라질)', 'BND(브루나이)', 'KHR(캄보디아(100))', 'CAD(캐나다)', 'HKD(홍콩)', 'CNY(중국)', 'CZK(체코)', 'DKK(덴마크)', 'EUR(유럽연합)', 'FJD(피지)', 'HUF(헝가리)', 'INR(인도)', 'IDR(인도네시아(100))', 'ILS(이스라엘)', 'JPY(일본(100))', 'JOD(요르단)', 'KWD(쿠웨이트)', 'MYR(말레이지아)', 'MXN(멕시코)', 'NZD(뉴질랜드)', 'NOK(노르웨이)', 'PHP(필리핀)', 'PLN(폴란드)', 'RUB(러시아)', 'SAR(사우디)', 'SGD(싱가포르)', 'ZAR(남아공)', 'SEK(스웨덴)', 'CHF(스위스)', 'TWD(대만)', 'THB(태국)', 'TRY(터키)', 'AED(U.A.E)', 'GBP(영국)', 'USD(미국)', 'VND(베트남(100))']
        self.mongo_name = mongo_name
        # host = '35.78.27.97'
        # port = '27017'
        # self.client = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
        self.client = MongoClient('localhost',27017)
        self.ex = exchange()
        self.int = Interest_Crawling()
        
    def make_DB(self, db_name, coll_name):
        # DB 생성
        db = self.client[db_name]
        # 컬렉션 생성
        coll = db[coll_name]
        print("컬렉션이름  : ",coll)
        
        return coll
    
    def rename_dict_key(self, dict_data, rename_list):
        dict_data = pd.DataFrame(dict_data)
        dict_data.columns = rename_list
    
        return dict_data.to_dict('record')
    
    def exchange_autoupdate(self):
        print('오늘은', f'{date_Dict[datetime.now().date().weekday()]}입니다.')
        # 데이터베이스 생성
        print("현재 존재하는 데이터베이스 이름 : ",self.client.list_database_names()) # 사용중인 모든 데이터베이스를 출력
        print('현재 존재하는 DB의 Collection 목록 : ', self.client['exchange'].list_collection_names())
        
        for i, country in enumerate(self.mongo_name):
            if country == 'Korea':
                return
            coll = self.make_DB('exchange', country)
            print(coll.find_one())
            print("크롤링을 진행할 국가 : ", country)
            if not coll.find_one():
                print('크롤링을 진행하지 않았으므로 처음부터 크롤링을 진행함둥!')
                insert_data = self.ex.country(self.exchange_countries[i])
                coll.insert_many(insert_data)
                print(country, '완료됐슴둥!')
                print('데이터 갯수는 ', coll.count_documents({}), '개임둥!')
            else: # 최근 날짜까지 업데애트
                last_date = datetime.strptime(list(coll.find())[-1]['date'], "%Y-%m-%d")
                last_date = last_date + timedelta(days=1)
                last_date = last_date.strftime('%Y-%m-%d')
                if last_date != str(datetime.now().date()):
                    print('DB 날짜와 현재 날짜가 언~발란스한 상황')
                    print(last_date)
                    try:
                        insert_data = self.ex.country(self.exchange_countries[i],last_date)
                        coll.insert_many(insert_data)
                        print(country, '완료됐슴둥!')
                        print('데이터 갯수는', coll.count_documents({}), '개임둥!')
                    except:
                        print('휴일입니다')

            
    def interest_autoupdate(self):
        mongo_name = self.mongo_name + ['Korea1Y', 'Korea2Y']
        for i, country in enumerate(mongo_name):
            print("크롤링을 진행할 국가 :", country)
            coll = self.make_DB('interest', country)
            if not coll.find_one():
                insert_data = self.int.initiate(i)
            else:
                last_date = datetime.strptime(list(coll.find())[-1]['date'], "%Y-%m-%d")
                last_date = last_date - timedelta(days=1)
                last_date = last_date.strftime('%Y-%m-%d')
                print(last_date)
                try:
                    insert_data = self.int.update(i, last_date)
                    for data in insert_data:
                        coll.update_one({'date' : data['date']}, {"$set" : data})
                    print('데이터 갯수는 ', coll.count_documents({}), '개임둥!')
                    print(f'{i}번째 {country} 국가 완료')
                except:print('업데이트할 데이터가 없음')

    def preprocessing(self):
        mongo_name = self.mongo_name + ['Korea1Y', 'Korea2Y']
        for i, country in enumerate(mongo_name):
            coll = self.make_DB('interest', country)
            data_dict = list(coll.find({}, {'_id' : 0}))
            keys_ori = list(data_dict[0].keys())
            print(keys_ori)
            for i, row in enumerate(data_dict):
                keys_list = list(row.keys())
                try:
                    keys_list[1]
                except:
                    insert = list(coll.find({'date' : {'$regex' : data_dict[i-1]['date']}}))
                    print(insert)
                    coll.update_one({'date' : row['date']}, {"$set" : {keys_ori[1] : insert[0][keys_ori[1]], keys_ori[2] : insert[0][keys_ori[2]]}})
    def make_date(self):
        mongo_name = self.mongo_name + ['Korea1Y', 'Korea2Y']
        for i, country in enumerate(mongo_name):
            coll = self.make_DB('interest', country)
            coll.insert_one({'date' : datetime.today().strftime('%Y-%m-%d')})

        
mg = DBUpdater_ex()

# step3.실행 주기 설정
schedule.every().monday.at("17:00").do(lambda: mg.exchange_autoupdate())
schedule.every().tuesday.at("17:00").do(lambda: mg.exchange_autoupdate())
schedule.every().wednesday.at("17:00").do(lambda: mg.exchange_autoupdate())
schedule.every().thursday.at("17:00").do(lambda: mg.exchange_autoupdate())
schedule.every().friday.at("17:00").do(lambda: mg.exchange_autoupdate())
schedule.every().day.at("16:00").do(lambda: mg.interest_autoupdate())
schedule.every().day.at("01:00").do(lambda: mg.make_date())
schedule.every().monday.at("16:30").do(lambda: mg.preprocessing())

# step4.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(1)