import pandas as pd
import requests
imf_countries = ['Australia', 'Bahrain, Kingdom of', 'Brazil', 'Brunei Darussalam', 'Cambodia','Canada', 'China, P.R.: Hong Kong',
                'China, P.R.: Mainland', 'Czech Rep.', 'Denmark', 'Euro Area', 'Fiji, Rep. of', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland, Rep. of', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Arab Emirates', 'United Kingdom', 'United States', 'Vietnam', 'Korea, Rep. of']

imf_REF_AREA = ['AU', 'BH', 'BR', 'BN', 'KH', 'CA', 'HK', 'CN', 'CZ', 'DK', 'U2', 'FJ', 'HU', 'IN', 'ID', 'IL', 'JP', 'JO', 'KW', 'MY',
                'MX', 'NZ', 'NO', 'PH', 'PL', 'RU', 'SA', 'SG', 'ZA', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'GB', 'US', 'VN', 'KR']
'''indicator 목록은 https://sdmxcentral.imf.org/items/codelist.html 에서 codelist에서 엑셀 파일로 다운로드 받아 확인'''
url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'

key = 'CompactData/IFS/M.KR.RAXGFX_USD' # adjust codes here
r = requests.get(f'{url}{key}').json()
imf_dict = r['CompactData']['DataSet']['Series']['Obs']

def rename_dict_key(dict_data, rename_list):
    dict_data = pd.DataFrame(dict_data)
    dict_data.columns = rename_list
    
    return dict_data.to_dict('record')

imf_df = pd.DataFrame(imf_dict)
imf_df.columns = ['date', 'inflation']
imf_dict = imf_df.to_dict('record')
print(imf_dict)
