import schedule
import time

# step2.실행할 함수 선언
class Interest_Crawling():
    def __init__(self):
        host = '35.78.27.97'
        port = '27017'
    def message(self):
        print("스케쥴 실행중...")


# step3.실행 주기 설정
schedule.every().monday.at("17:00").do(lambda: Interest_Crawling().message())

# step4.스캐쥴 시작
while True:
    schedule.run_pending()
    time.sleep(1)