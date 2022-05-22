import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import glob
import bs4
import warnings

imf_counties = ['Australia', 'Bahrain, Kingdom of', 'Brazil', 'Brunei Darussalam', 'Cambodia','Canada', 'China, P.R.: Hong Kong',
                'China, P.R.: Mainland', 'Czech Rep.', 'Denmark', 'Euro Area', 'Fiji, Rep. of', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland, Rep. of', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Arab Emirates', 'United Kingdom', 'United States', 'Vietnam', 'Korea, Rep. of']

warnings.filterwarnings("ignore")
driver = webdriver.Chrome('/Users/yuseonjong/chromedriver')
date_storage = sorted(glob.glob('./../data/exchange/*.csv'))  # 환율 데이터 경로(날짜 가져오기)
ac = ActionChains(driver)
driver.get('https://data.imf.org/regular.aspx?key=61545856')
driver.maximize_window()

wait = WebDriverWait(driver, 1500)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PPTabControlItems'))) # 날짜 선택 버튼이 나타날 때까지 기다림
print('들어간다')
time.sleep(5)
date_list = element.find_elements_by_tag_name('div')
ac.move_to_element(date_list[20]).click().perform() # 월별 데이터 탭 클릭
time.sleep(5)

dropbox = driver.find_elements_by_class_name('PPCombo.PPC.PPMacOS.Released.PPTreeDropDown') # 드롭박스 0. 국가 1. 기간
# 날짜 입력
ac.move_to_element(dropbox[1]).click().perform()
time.sleep(4)
mg = driver.find_elements_by_class_name('PPButton.PPComboControlButton.PPC.PPMacOS.PPNoSelect.PPImageButton.H.CenterContentVertically.PPRibbonButton.Released') # 돋보기 (이미지 클래스)
time.sleep(4)
ac.move_to_element(to_element=mg[1]).click().perform()
text_box = driver.find_element_by_class_name('PPTextBox.PPC.PPMacOS.PPTextBoxEllipsis.PPTextBoxRightContent.Hovered.PPTextBoxFocused') # 두개의 텍스트 입력 박스 중에 날짜 입력 박스
i = 10
for year in range(2003,2022):
    i += 1
    print(year)
    ac.send_keys_to_element(text_box, str(year)).perform()
    time.sleep(i)
    temp_list = driver.find_elements_by_class_name('PPTLVNodeRow')  # 아직 선택되지 않아 선택해야 할 날짜
    date_list = temp_list[2:5] + temp_list[6:9]
    selected_list = driver.find_elements_by_class_name('PPTLVNodeRow.PPTLVNodeSelected') # 이미 선택되어 있는 날짜
    if len(selected_list) == 0:
        for i in range(6):
            ac.move_to_element(to_element=date_list[i]).click().perform()
            time.sleep(5)
    else: # 선택된 날짜가 있을 경우
        for e in date_list:
            for es in selected_list:
                if e == es:  # 선택된 날짜가 존재하는 경우 해당 요소를 삭제하여 건너뛰게 만듬
                    date_list[date_list.index(e)] = None
        for i in range(6):
            if date_list[i] == None:
                continue
            time.sleep(5)
    button = driver.find_elements_by_class_name('PPRS')
    ac.move_to_element(button[3]).click().perform()
    ac.move_to_element(button[3]).click_and_hold().pause(8).perform()
    time.sleep(3)
    ac.move_to_element(text_box).click().perform()

    temp_list = driver.find_elements_by_class_name('PPTLVNodeRow')  # 아직 선택되지 않아 선택해야 할 날짜
    date_list = temp_list[5:8] + temp_list[9:]
    date_list = date_list[::-1]
    selected_list = driver.find_elements_by_class_name('PPTLVNodeRow.PPTLVNodeSelected') # 이미 선택되어 있는 날짜
    if len(selected_list) == 0:
        for i in range(6):
            ac.move_to_element(to_element=date_list[i]).click().perform()
            time.sleep(6)
    else: # 선택된 날짜가 있을 경우
        for e in date_list:
            for es in selected_list:
                if e == es:  # 선택된 날짜가 존재하는 경우 해당 요소를 삭제하여 건너뛰게 만듬
                    date_list[date_list.index(e)] = None
        for i in range(6):
            if date_list[i] == None:
                continue
            ac.move_to_element(to_element=date_list[i]).click().perform()
            time.sleep(6)
    for _ in range(4):
        ac.send_keys_to_element(text_box, Keys.BACK_SPACE).perform()
body = driver.find_element_by_class_name('PPNoSelect.LayoutMaster')
ac.move_to_element(to_element=body).click().perform()
print('wait')
while True:
    time.sleep(10)
    cell_number = driver.find_elements_by_class_name('PPTSCellConText')
    print('로딩중...')
    if len(cell_number) > 93:
        break
# 국가 입력
print('로딩 끝났다')
time.sleep(200)
for country in imf_counties:
    ac.move_to_element(dropbox[0]).click().perform()
    time.sleep(4)
    ac.move_to_element(to_element=mg[0]).click().perform()
    text_box = driver.find_element_by_class_name('PPTextBox.PPC.PPMacOS.PPTextBoxEllipsis.PPTextBoxRightContent.Hovered.PPTextBoxFocused') # 두개의 텍스트 입력 박스 중에 국가 입력 텍스트
    time.sleep(4)
    ac.send_keys_to_element(text_box, country).perform()
    time.sleep(4)
    element = driver.find_element_by_class_name('PPTLVNodeTextHighlight') 
    ac.move_to_element(to_element=element).click().perform() # 해당 국가 클릭
    title = driver.find_elements_by_class_name('PPTSCellConText')[1] # 첫번째 줄 Indicator 다음에 두번째 줄 국가 이름
    time.sleep(200)

    print('export in')
    export = driver.find_elements_by_class_name('PPButtonContentContainer')[8]
    ac.move_to_element(to_element=export).click().perform() # export 버튼 클릭
    time.sleep(10)
    print('export out')

    print('excel button in ')
    xlsx = driver.find_element_by_class_name('PPMenuItemContentPart')
    ac.move_to_element(to_element=xlsx).click().perform() # 엑셀 버튼 클릭
    time.sleep(10)
    print('excel button out ')

    print('세부 버튼 1 in')
    element = driver.find_element_by_class_name('CBImg.Checked')
    ac.move_to_element(to_element=element).click().perform() # 엑셀 버튼 클릭
    time.sleep(5)
    print('세부 버튼 1 out')

    print('세부 버튼 2 in')
    element = driver.find_element_by_class_name('RBImg.Unchecked')
    ac.move_to_element(to_element=element).click().perform() # 엑셀 버튼 클릭
    time.sleep(5)
    print('세부 버튼 2 out')

    print('세부 버튼 3 in')
    element = driver.find_elements_by_class_name('CBImg.Unchecked')[-1]
    ac.move_to_element(to_element=element).click().perform() # 엑셀 버튼 클릭
    time.sleep(10)
    print('세부 버튼 3 out')

    print('다운로드')
    element = driver.find_element_by_class_name('PPButton.PPC.PPMacOS.PPNoSelect.PPHighlightBorderOnFocus.Released')
    ac.move_to_element(to_element=element).click().perform() # 엑셀 버튼 클릭
    time.sleep(30)
    print('끝')


while True:
    pass
