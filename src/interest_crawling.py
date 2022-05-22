import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import glob
import bs4
from dateutil.parser import parse
import datetime
import warnings

# 대부분 1년물이 존재하지만 1년물이 아닌 2년물이 존재하는 경우, 혹은 둘다 존재하지 않는 경우를 모두 고려
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

date_storage = sorted(glob.glob('./../data/exchange/*.csv'))  # 환율 데이터 경로(날짜 가져오기)
warnings.filterwarnings("ignore") # 경고문 제거
driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
action = ActionChains(driver)
driver.get('https://google.com') # 구글 창 열기
driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

for i in range(39, len(investing_countries)+2): # 한국은 두번
    if i < 37:
        continue
    if i < 39:
        if investing_countries_1Y[i] != None:
            country = investing_countries_1Y[i]
            url = f'https://www.investing.com/rates-bonds/{country}-1-year-bond-yield-historical-data' # 1년물 채권 사이트
            condition = 1
        elif investing_countries_2Y[i] != None:
            country = investing_countries_2Y[i]
            url = f'https://www.investing.com/rates-bonds/{country}-2-year-bond-yield-historical-data' # 2년물 채권 사이트
            condition = 1
        else:
            continue
    else: # 한국 1년 & 2년물
        country = 'south-korea'
        if i == 39:
            url = 'https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data'
            condition = 1
        elif i == 40:
            url = 'https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data'
            condition = 1
    
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
    if i < 39:
        exchange = pd.read_csv(date_storage[0])['date'].iloc[-1].replace('-', '/') # 환율 시작 날짜
        date = exchange[5:] + '/' + exchange[:4]
    else:
        date = '01/01/2000'
    time.sleep(15)
    try:
        driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
    except:pass
    
    try:
        date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
    except:
        driver.refresh()
        time.sleep(15)
        try:
            driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
        except:pass
        date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
        
    start_date = driver.find_element_by_id('startDate') # 시작 날짜 입력
    start_date.clear()
    start_date.send_keys(date)
    time.sleep(5)
    driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
    time.sleep(10)

    tbody = driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
    table = tbody.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
    
    df = pd.DataFrame(columns = ['date', 'interest', 'change'])
    for tr in rows:
        td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
        d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
        data = [d, td[1].text, td[5].text.replace('%','')] # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
        print(data)
        df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
    
    # 약 17년 동안의 데이터만 표시해주므로 나머지 날짜에 대한 데이터를 다시 크롤링
    try:
        driver.find_element_by_class_name('popupCloseIcon.largeBannerCloser').click() # 광고 배너 닫기
    except:pass
    connect_date = df['date'].iloc[0].replace('-', '/')
    print(connect_date)
    connect_date = connect_date[5:] + '/' + connect_date[:4]
    print(connect_date)
    date_input = driver.find_element_by_id('widgetFieldDateRange').click() # 날짜 변경 버튼
    start_date = driver.find_element_by_id('startDate') # 시작 날짜 입력
    start_date.clear()
    start_date.send_keys(connect_date)
    time.sleep(5)
    driver.find_element_by_id('applyBtn').click() # 바뀐 날짜 적용
    time.sleep(10)
    
    tbody = driver.find_element_by_id('curr_table') # 환율 데이터 테이블 접근
    table = tbody.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_tag_name("tr") # 테이블의 각 행에 접근
    
    df1 = pd.DataFrame(columns = ['date', 'interest', 'change'])
    for tr in rows:
        td = tr.find_elements_by_tag_name("td") # 모든 열 찾기
        d = parse(td[0].text, ignoretz = True).strftime("%Y-%m-%d")
        if df['date'].iloc[0] == d:
            break
        data = [d, td[1].text, td[5].text.replace('%','')] # 날짜, 종가, 시가, 고가, 저가, 변화율(%)
        print(data)
        df1 = df1.append(pd.Series(data, index=df.columns), ignore_index=True)
    if df1.empty == True:
        result = df
    else:
        result = pd.concat([df1, df])
    
    if len(str(i+1)) == 1:
        num = '0' + str(i+1)
    else:
        num = str(i+1)
    result.to_csv(f'{num}_{country}_government_bond_rate_{condition}year.csv')
    print(country) # 한국 나오면 끝
    driver.close()  #탭 닫기
    driver.switch_to.window(driver.window_handles[0])  #다시 이전 창(탭)으로 이동