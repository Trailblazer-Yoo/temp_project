from datetime import datetime
from pymongo import MongoClient
import pandas as pd
from .exchange_crawling import exchange
from interest_crawling import Interest_Crawling

country_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

exchange_countries = ['AUD(호주)', 'BHD(바레인)', 'BRL(브라질)', 'BND(브루나이)', 'KHR(캄보디아(100))', 'CAD(캐나다)', 'HKD(홍콩)',
                      'CNY(중국)', 'CZK(체코)', 'DKK(덴마크)', 'EUR(유럽연합)', 'FJD(피지)', 'HUF(헝가리)', 'INR(인도)', 'IDR(인도네시아(100))', 'ILS(이스라엘)',
                      'JPY(일본(100))', 'JOD(요르단)', 'KWD(쿠웨이트)', 'MYR(말레이지아)', 'MXN(멕시코)', 'NZD(뉴질랜드)', 
                      'NOK(노르웨이)', 'PHP(필리핀)', 'PLN(폴란드)', 'RUB(러시아)', 'SAR(사우디)', 'SGD(싱가포르)', 'ZAR(남아공)',
                      'SEK(스웨덴)', 'CHF(스위스)', 'TWD(대만)', 'THB(태국)', 'TRY(터키)', 'AED(U.A.E)', 'GBP(영국)', 'USD(미국)', 'VND(베트남(100))']

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

date_Dict = {0 : '월요일', 1 : '화요일', 2 : '수요일', 3: '목요일',
             4 : '금요알', 5 : '토요일', 6 : '일요일'}

class DBUpdater_ex():
    def __init__(self):
        self.exchange_countries = exchange_countries
        self.country_name = country_name
        self.client = MongoClient('localhost', 27017)  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
        self.db = self.client['exchange']
        self.ex = exchange()
        self.int = Interest_Crawling()
        
    def make_DB(self, db_name):

        # 컬렉션 생성
        coll = self.db[db_name]
        print("컬렉션이름  : ",coll)
        
        return coll
    
    def rename_dict_key(self, dict_data, rename_list):
        dict_data = pd.DataFrame(dict_data)
        dict_data.columns = rename_list
    
        return dict_data.to_dict('record')
    
    def autoupdate(self):
        print('오늘은', f'{date_Dict[datetime.now().date().weekday()]}입니다.')
        if int(datetime.now().date().weekday()) < 5:
            print('은행 영업 마감 시간은 3시 30분이므로 크롤링은 그 이후에 진행하실 수 있습니다.')
            print('현재 시간은 ', f'{datetime.now().hour}시', f'{datetime.now().minute}분입니다.')
            try :
                if int(datetime.now().hour) > 15 and int(datetime.now().minute) > 30:
                    print('따라서 크롤링을 진행합니다.')
                    # 데이터베이스 생성
                    print("현재 존재하는 데이터베이스 이름 : ",self.client.list_database_names()) # 사용중인 모든 데이터베이스를 출력
                    print('현재 존재하는 DB의 Collection 목록 : ', self.db.list_collection_names())
                    
                    for i, country in enumerate(self.country_name):
                        if country == 'Korea':
                            return
                        coll = self.make_DB(country)
                        print(coll.find_one())
                        print("크롤링을 진행할 국가 : ", country)
                        if not coll.find_one():
                            print('크롤링을 진행하지 않았으므로 처음부터 크롤링을 진행함둥!')
                            insert_data = self.ex.country(self.exchange_countries[i])
                            coll.insert_many(insert_data)
                            print(country, '완료됐슴둥!')
                            print('데이터 갯수는 ', coll.count_documents({}), '개임둥!')
                        else: # 최근 날짜까지 업데애트
                            print(coll.find_one()['date'])
                            if coll.find_one()['date'] != str(datetime.now().date()):
                                print('DB 날짜와 현재 날짜가 언~발란스한 상황')
                                date = coll.find_one()['date']
                                insert_data = self.ex.country(self.exchange_countries[i],date)
                                coll.insert_many(insert_data)
                                print(country, '완료됐슴둥!')
                                print('데이터 갯수는', coll.count_documents({}), '개임둥!')
                            elif coll.find_one()['date'] == datetime.now().date():
                                print('이미 업데이트해놨지롱~')
                else:
                    raise
            except:
                print('크롤링 가능한 시간까지', f'{14-int(int(datetime.now().hour))}시간', f'{60-int(datetime.now().minute)}분 남았습니다.')
        else:
            print('주말에는 은행이 영업하지 않으므로 새로 업데이트할 데이터가 없습니다.')
                
    def update_one_country(self, country):
        coll = self.make_DB(country)
        print("크롤링을 진행할 국가 : ", country)
        i = imf_counties.find(country)
        if not coll.find_one():
            print('크롤링을 진행하지 않았으므로 처음부터 크롤링을 진행함둥!')
            insert_data = self.ex.country(self.exchange_countries[i])
            coll.insert_many(insert_data)
            print(country, '완료됐슴둥!')
            print('데이터 갯수는 ', coll.count_documents({}), '개임둥!')
        else: # 최근 날짜까지 업데애트
            if coll.find_one()['date'] != str(datetime.now().date()):
                print('DB 날짜와 현재 날짜가 언~발란스한 상황')
                date = coll.find_one()['date']
                insert_data = self.ex.country(self.exchange_countries[i],date)
                coll.insert_many(insert_data)
                print(country, '완료됐슴둥!')
                print('데이터 갯수는', coll.count_documents({}), '개임둥!')
            elif coll.find_one()['date'] == datetime.now().date():
                print('이미 업데이트해놨지롱~')

        
            
mg = DBUpdater_ex()
mg.autoupdate()