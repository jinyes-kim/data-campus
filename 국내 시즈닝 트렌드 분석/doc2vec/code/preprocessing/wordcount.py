import pandas as pd
import pprint


def word_count(data_list):
    count = {}
    for data in data_list:
        words = str(data).split()
        for word in words:
            word = word.strip()
            if word not in count:
                count[word] = 1
            else:
                count[word] += 1
    pprint.pprint(count)
    return count


def to_df(data_dict): #dict type
    tmp = []
    for word in data_dict:
        if data_dict[word] > 10 and str(word).isalnum():
            tmp.append([word, data_dict[word]])
    new_df = pd.DataFrame(tmp, columns=['word', 'count'])
    return new_df


df1 = pd.read_excel('seasoning.xlsx', 0, encoding='unicode_escape')
df2 = pd.read_excel('seasoning.xlsx', 1, encoding='unicode_escape')
df3 = pd.read_excel('seasoning.xlsx', 2, encoding='unicode_escape')
df4 = pd.read_excel('seasoning.xlsx', 3, encoding='unicode_escape')
df = pd.concat([df1, df2, df3, df4])

title_data = list(df['제목'])
article_data = list(df['내용'])
title = word_count(title_data)
article = word_count(article_data)

writer = pd.ExcelWriter('C:/wisenut_crawling/wordcount.xlsx', engine='xlsxwriter')
to_df(title).to_excel(writer, sheet_name='title', header=True, index=False)
to_df(article).to_excel(writer, sheet_name='article', header=True, index=False)
writer.save()

