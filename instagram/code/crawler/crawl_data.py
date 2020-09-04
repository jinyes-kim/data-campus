import pprint
from bs4 import BeautifulSoup
from selenium import webdriver as wb
from time import sleep
import csv

kwd = input("save as: ")
driver = wb.Chrome('chromedriver.exe')
link_list = []

with open('topic_link.txt', 'r') as file:
    for link in file:
        link_list.append(link)

link_list = list(set(link_list))
print(len(list(set(link_list))))


feed = []
for link in link_list:
    article = 'https://www.instagram.com' + str(link)
    driver.get(article)
    sleep(3)

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    for i, tmp in enumerate(soup.find_all(name='div', attrs={"class": "C4VMK"})):
        date_data = soup.find(name='time', attrs={"class": "_1o9PC Nzb55"}).attrs['datetime']
        tmp_list = [date_data]
        for j, word in enumerate(tmp):
            if i == 0 and j == 2:
                writer_like_point = soup.find(name='div', attrs={"class": "Nm9Fw"})
                try:
                    likes = str(writer_like_point.select('span'))
                    start = likes.find('<span>')
                    end = likes.find('</span>')
                    tmp_list.append(likes[start + 6: end])
                except:
                    likes = str(soup.select('head > meta:nth-child(35)'))
                    tmp_list.append(likes)

            else:
                tmp_list.append(word.get_text())
        feed.append(tmp_list)

pprint.pprint(feed)


# export csv file
output = open(kwd + '_.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(output)
wr.writerow(['date', 'user_id', 'text', 'like', 'tag'])

for record in feed:
    wr.writerow(record)

output.close()
