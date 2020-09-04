from pprint import pprint
import pandas as pd
import re
from konlpy.tag import Komoran
from konlpy.tag import Okt
from konlpy.tag import Kkma
from soynlp.tokenizer import RegexTokenizer


def extract_title_nouns(df):
    okt = Okt()
    title_list = list(df['내용'])
    res_list = []
    for title in title_list:
        title = str(title)
        title = title.replace('URL', '')
        title = title.replace('이웃추가', '')
        title = title.replace('본문', '')
        title = title.replace('복사', '')
        title = title.replace('#', '')
        title = title.strip()
        try:
            nouns = okt.nouns(str(title))
            res_list.append(nouns)
        except:
            nouns = []
            res_list.append(nouns)
    print("extract complete")
    return res_list


# open xlsx file
file_name = './data/2017_data.xlsx'

df1 = pd.read_excel(file_name, 0)
df2 = pd.read_excel(file_name, 1)
#df3 = pd.read_excel(file_name, 2)
#df4 = pd.read_excel(file_name, 3)

# extract nouns
df1_nouns = extract_title_nouns(df1)
df2_nouns = extract_title_nouns(df2)
#df3_nouns = extract_title_nouns(df3)
#df4_nouns = extract_title_nouns(df4)
df1['명사'] = df1_nouns
df2['명사'] = df2_nouns
#df3['명사'] = df3_nouns
#df4['명사'] = df4_nouns


# save data
writer = pd.ExcelWriter('./2017_sample.xlsx', engine='xlsxwriter')
df_list = [df1, df2]
sheet = '1'

for df in df_list:
    print("svae as sheet {}".format(sheet), end='\n\n')
    df.to_excel(writer, sheet_name=sheet, header=True, index=False)
    sheet = str(int(sheet) + 1)

writer.save()
