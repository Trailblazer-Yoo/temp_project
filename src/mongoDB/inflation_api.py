from re import S
from pymongo import ASCENDING
import requests
import pandas as pd

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']
imf_REF_AREA = ['AU', 'BH', 'BR', 'BN', 'KH', 'CA', 'HK', 'CN', 'CZ', 'DK', 'U2', 'FJ', 'HU', 'IN', 'ID', 'IL', 'JP', 'JO', 'KW', 'MY',
                 'MX', 'NZ', 'NO', 'PH', 'PL', 'RU', 'SA', 'SG', 'ZA', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'GB', 'US', 'VN', 'KR']
'''indicator 목록은 https://sdmxcentral.imf.org/items/codelist.html 에서 codelist에서 엑셀 파일로 다운로드 받아 확인'''
base_url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/'

         # 산업지수, 물가 상승률, 기준금리, 국제 통화량, 실질환율
series = ['AIP_IX', 'PCPI_IX', 'FIR_PA','RAXG_USD', 'ENSE_XDC_XDR_RATE']
name = ['산업지수', '물가상승률', '기준금리', '국제통화량', '실질환율']

cp = pd.read_csv('Crude_Oil_WTI_Futures_Historical_Data.csv')
key = f'M.US.AIP_IX' # adjust codes here
r = requests.get(f'{base_url}{key}').json()
# imf_dict = r['CompactData']['DataSet']['Series']['Obs']
# print(imf_dict)


for country in imf_REF_AREA:
    print(mongo_name[imf_REF_AREA.index(country)])
    for k in series:
        for date in ['M', 'Q', 'Y']:
            try:
                key = f'{date}.{country}.{k}' # adjust codes here
                r = requests.get(f'{base_url}{key}').json()
                imf_dict = r['CompactData']['DataSet']['Series']['Obs']
                print(date, name[series.index(k)],'데이터 :',imf_dict[0]['@TIME_PERIOD'],'부터', imf_dict[-1]['@TIME_PERIOD'], '까지')
            except:
                print(date, name[series.index(k)], '데이터 없음')
imf_df = pd.DataFrame(imf_dict)
imf_df.columns = ['date', 'inflation']
imf_dict = imf_df.to_dict('record')
