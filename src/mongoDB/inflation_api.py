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

         # 통화량(계절조정) ,   국제 통화량(금 제외), 산업지수, 산업지수(계절조정), 물가 지수, 물가변화율(계절조정)
series = [ 'RAXG_USD', 'AIP_IX', 'PCPI_IX', 'PCPI_PC_PP_PT']

key = f'M.CA.PCPI_PC_PP_PT' # adjust codes here
r = requests.get(f'{base_url}{key}').json()
imf_dict = r['CompactData']['DataSet']['Series']['Obs']
print(imf_dict)
# imf_df = pd.DataFrame(imf_dict)
# imf_df.columns = ['date', 'inflation']
# imf_dict = imf_df.to_dict('record')
