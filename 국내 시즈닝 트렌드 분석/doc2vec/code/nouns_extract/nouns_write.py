import pandas as pd

df1_0 = pd.read_excel('2017_nouns.xlsx', 0)
df1_1 = pd.read_excel('2017_nouns.xlsx', 1)

df2_0 = pd.read_excel('2018_nouns.xlsx', 0)
df2_1 = pd.read_excel('2018_nouns.xlsx', 1)
df2_2 = pd.read_excel('2018_nouns.xlsx', 2)

df3_0 = pd.read_excel('2019_nouns.xlsx', 0)
df3_1 = pd.read_excel('2019_nouns.xlsx', 1)
df3_2 = pd.read_excel('2019_nouns.xlsx', 2)
df3_3 = pd.read_excel('2019_nouns.xlsx', 3)

df4_0 = pd.read_excel('2020_nouns.xlsx', 0)
df4_1 = pd.read_excel('2020_nouns.xlsx', 1)
df4_2 = pd.read_excel('2020_nouns.xlsx', 2)
df4_3 = pd.read_excel('2020_nouns.xlsx', 3)

df_list = [df1_0, df1_1, df2_0, df2_1, df2_2, df3_0, df3_1, df3_2, df3_3, df4_0, df4_1, df4_2, df4_3]


file = open("nouns.txt", "w", encoding='utf-8-sig')

for df in df_list:
    nouns_list = list(df['명사'])
    for nouns in nouns_list:
        if nouns == '[]':
            continue
        else:
            nouns = nouns[2:-2]
            data = nouns.split("', '")
            data = ' '.join(data)
            file.write(data + '\n')
file.close()
