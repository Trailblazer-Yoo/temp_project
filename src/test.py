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
text_box = driver.find_element_by_class_name('PPTextBox.PPC.PPMacOS.PPTextBoxEllipsis.PPTextBoxRightContent.Hovered.PPTextBoxFocused') # 두개의 텍스트 입력 박스 중에 첫번째(국가)
ac.send_keys_to_element(text_box, 2022).perform()

button = driver.find_elements_by_class_name('PPRS')[3]
ac.move_to_element(button).click_and_hold().pause(5).perform()

temp_list = driver.find_elements_by_class_name('PPTLVNodeRow')  # 아직 선택되지 않아 선택해야 할 날짜
print(temp_list)
print(len(temp_list[5:9]))
print(len(temp_list[9:12]))
date_list = temp_list[5:9] + temp_list[9:12]
date_list = date_list[::-1]
selected_list = driver.find_elements_by_class_name('PPTLVNodeRow.PPTLVNodeSelected') # 이미 선택되어 있는 날짜