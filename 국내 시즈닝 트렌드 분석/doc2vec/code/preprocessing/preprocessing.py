import pandas as pd
import pprint


# 3 제목
# 4 본문
def rm_garbage(df, stopword):
    res = []
    length = len(df)

    for i in range(len(df)):
        check = True
        data = list(df.loc[i])

        title = str(data[3]).strip()
        #article = data[4]
        for word in stopword:
            if word in title:
                check = False

        if check:
            res.append(data)

    new_df = pd.DataFrame(res)
    new_df.columns = df.columns

    pp_length = len(new_df)
    print("입력 데이터 {} 건".format(length))
    print("보존 데이터 {} 건".format(pp_length))
    print("삭제 데이터 {} 건".format(length - pp_length))
    return new_df


rm_word_list = ['맛집', '술집', '여행', '스테이크', '주식', '창업']
df1 = pd.read_excel('wisenut.xlsx', 8, encoding='unicode_escape')
df2 = pd.read_excel('wisenut.xlsx', 9, encoding='unicode_escape')
df3 = pd.read_excel('wisenut.xlsx', 10, encoding='unicode_escape')
df4 = pd.read_excel('wisenut.xlsx', 11, encoding='unicode_escape')
sheet = '1'
writer = pd.ExcelWriter('C:/wisenut_crawling/seasoning.xlsx', engine='xlsxwriter')

for df in [df1, df2, df3, df4]:
    res = rm_garbage(df, rm_word_list)
    print("svae as sheet {}".format(sheet), end='\n\n')
    res.to_excel(writer, sheet_name=sheet, header=True, index=False)
    sheet = str(int(sheet) + 1)

writer.save()
