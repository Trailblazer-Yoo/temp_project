import time
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import warnings
warnings.filterwarnings("ignore")

driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
ac = ActionChains(driver)

driver.get('https://www.google.co.kr/maps/?hl=ko') # 구글 창 열기
driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

print('메뉴창 클릭')
input = driver.find_element_by_id('searchboxinput')
ac.move_to_element(input).click().send_keys_to_element(input, 'Hawaii').send_keys_to_element(input, Keys.ENTER).perform()
ac.move_to_element(input).click().send_keys_to_element(input, 'Hawaii 맛집').send_keys_to_element(input, Keys.ENTER).perform()
time.sleep(5)

href_list = []
while True:
    try:
        scroll = driver.find_element_by_class_name('m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')
        # scroll = driver.find_element_by_css_selector('focus:.scrollable.focus;.blur:.scrollable.blur')
        ac.move_to_element(to_element=scroll).send_keys_to_element(scroll,Keys.PAGE_DOWN).perform()
        time.sleep(3)
        changed_scroll = driver.find_element_by_class_name('m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t')
        ac.move_to_element(to_element=changed_scroll
                           ).send_keys_to_element(changed_scroll,Keys.PAGE_DOWN
                           ).send_keys_to_element(changed_scroll,Keys.PAGE_DOWN
                           ).send_keys_to_element(changed_scroll,Keys.PAGE_DOWN
                           ).send_keys_to_element(changed_scroll,Keys.PAGE_DOWN
                           ).send_keys_to_element(changed_scroll,Keys.PAGE_DOWN
                           ).perform()

        time.sleep(3)
        google_list = driver.find_elements_by_class_name('hfpxzc')
        for a_tag in google_list:
            href_list.append(a_tag.get_attribute('href'))
        time.sleep(1)

        next_button = driver.find_elements_by_class_name('hV1iCc.Hk4XGb')[-1]
        ac.move_to_element(to_element=next_button).click().perform()
        time.sleep(3)
    except:break
print(href_list)

# driver = webdriver.Chrome('/Users/yuseonjong/chromedriver') # 드라이버 위치
# ac = ActionChains(driver)

# driver.get('https://www.google.co.kr/maps/place/%EB%9D%BC%EB%A9%98+%EB%82%98%EC%B9%B4%EB%AC%B4%EB%9D%BC/data=!4m6!3m5!1s0x7c006d8a8c295e5d:0xc0093f8a3c10bada!8m2!3d21.2812775!4d-157.8307149!16s%2Fg%2F1thf8scf?authuser=0&hl=ko&rclk=1') # 구글 창 열기
# driver.maximize_window() # 창 모니터 크기에 맞춰 최대화

# review_button = driver.find_elements_by_class_name('wNNZR.fontTitleSmall')[1]
# ac.move_to_element(to_element = review_button).click().perform()

# ac.perform()
while True:
    pass