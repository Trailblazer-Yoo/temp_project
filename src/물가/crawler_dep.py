def crawl(day):
    
    import pandas as pd
    import numpy
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import re
    import time
    from tqdm import tqdm    # 상태진행바 확인

    
    dep_code = "ICN" # 출발지
    person = 1 # 인원
    df = pd.read_excel("공항코드.xlsx") # 나라별 공항 코드 정리 파일
    
    chromedriver_path = '/usr/local/bin/chromedriver'

    columns = ['출발지', '도착지', '날짜', '항공사', '출발', '도착', '경유', '비행시간', '가격'] # Dataframe head
    airplane_df = pd.DataFrame(columns=columns) # 항공권 정보 담을 Dataframe

    for arr_code in tqdm(df['공항코드']):
        url = f'https://flight.naver.com/flights/international/{dep_code}-{arr_code}-{day}?adult={person}&fareType=Y'

        driver = webdriver.Chrome(chromedriver_path)
        driver.get(url)

        WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[3]/div/div[3]')))
        time.sleep(2)

        element1 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div[1]/div/div[2]/button')
        element1.click() # 요금 조건 창 선택
        element2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div[1]/div/div[2]/div/button[2]')
        element2.click() # 카드 조건 제외 옵션 선택

        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')

        airline_info = soup.select('div.airline > b.name') # 항공사
        trans_info_raw = soup.select('i.route_info__1RhUH') # 경유 + 시간
        price_info = soup.select('i.item_num__3R0Vz') # 가격

        for i in range(0, len(airline_info)):
            dep_path = f'div.indivisual_IndividualList__3Ajvq > div > div:nth-child({i+1}) > div > div.indivisual_schedule__1tq7j > div > div.route_Route__2UInh > span:nth-child(1) > b'
            arr_path = f'div.indivisual_IndividualList__3Ajvq > div > div:nth-child({i+1}) > div > div.indivisual_schedule__1tq7j > div > div.route_Route__2UInh > span:nth-child(2) > b'

            n = 1; dep_time_info = soup.select(dep_path)[0].text # 출발 시간
            n = 2; arr_time_info = soup.select(arr_path)[0].text # 도착 시간
            trans_info = re.split(r',', trans_info_raw[i].text) # 경유 / 시간

            row = [dep_code, arr_code, day, airline_info[i].text, dep_time_info, arr_time_info, trans_info[0], trans_info[1], price_info[i].text]
            series = pd.Series(row, index=airplane_df.columns)
            airplane_df = airplane_df.append(series, ignore_index=True)

        driver.close()
        
    return airplane_df
