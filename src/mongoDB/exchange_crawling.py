import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import warnings
warnings.filterwarnings("ignore")
exchange_countries = ['AUD(호주)', 'BHD(바레인)', 'BRL(브라질)', 'BND(브루나이)', 'KHR(캄보디아(100))', 'CAD(캐나다)', 'HKD(홍콩)',
                      'CNY(중국)', 'CZK(체코)', 'DKK(덴마크)', 'EUR(유럽연합)', 'FJD(피지)', 'HUF(헝가리)', 'INR(인도)', 'IDR(인도네시아(100))', 'ILS(이스라엘)',
                      'JPY(일본(100))', 'JOD(요르단)', 'KWD(쿠웨이트)', 'MYR(말레이지아)', 'MXN(멕시코)', 'NZD(뉴질랜드)', 
                      'NOK(노르웨이)', 'PHP(필리핀)', 'PLN(폴란드)', 'RUB(러시아)', 'SAR(사우디)', 'SGD(싱가포르)', 'ZAR(남아공)',
                      'SEK(스웨덴)', 'CHF(스위스)', 'TWD(대만)', 'THB(태국)', 'TRY(터키)', 'AED(U.A.E)', 'GBP(영국)', 'USD(미국)', 'VND(베트남(100))']

imf_countries = ['Australia', 'Bahrain, Kingdom of', 'Brazil', 'Brunei Darussalam', 'Cambodia','Canada', 'China, P.R.: Hong Kong',
                'China, P.R.: Mainland', 'Czech Rep.', 'Denmark', 'Euro Area', 'Fiji, Rep. of', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland, Rep. of', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Arab Emirates', 'United Kingdom', 'United States', 'Vietnam', 'Korea, Rep. of']

investing_countries = ['australia', 'bahrain','brazil', None, None, 'canada', 'hong-kong',
                'china', 'czech-republic', None, 'germany', None, 'hungary', 'india', 'indonesia', 'israel',
                 'japan', 'jordan', None, 'malaysia', 'mexico', 'new-zealand',
                'norway', 'philippines', 'poland', 'russia', None, 'singapore', 'south-africa',
                None, 'switzerland', 'taiwan', 'thailand', 'turkey', None, 'uk', 'u.s.', 'vietnam', 'south-korea']

class exchange():
    def __init__(self):
        pass
            
    def country(self, country_name, date=None):
        driver = webdriver.Chrome('/Users/yuseonjong/chromedriver')
        driver.get('https://google.com')
        driver.maximize_window()
        driver.execute_script('window.open("https://spot.wooribank.com/pot/Dream?withyou=FXXRT0014");')
        time.sleep(10)

        driver.switch_to.window(driver.window_handles[-1])

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
        

