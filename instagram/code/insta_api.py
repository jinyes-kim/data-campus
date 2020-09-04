from selenium import webdriver as wb
from bs4 import BeautifulSoup
from time import sleep
import csv
import pprint
import re


def crawl_insta_link(kwd, user_id, user_pw):
    driver = wb.Chrome('chromedriver.exe')
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)

    id_input = driver.find_elements_by_css_selector('#loginForm > div > div:nth-child(1) > div > label > input')[0]
    id_input.send_keys(user_id)
    password_input = driver.find_elements_by_css_selector('#loginForm > div > div:nth-child(2) > div > label > input')[0]
    password_input.send_keys(user_pw)
    password_input.submit()
    sleep(3)

    url = "https://www.instagram.com/explore/tags/" + str(kwd)
    driver.get(url)
    sleep(3)

    item_link = []
    while True:
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        for tmp in soup.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
            dummy_link = tmp.select('a')
            for dummy in dummy_link:
                item_link.append(dummy.attrs['href'])

        # scroll down
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(30)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                continue

    print("Total link: ", end=' ')
    print(len(item_link))
    return item_link


def save_links_to_txt(file_name, link_list):
    file = open(file_name + '.txt', 'w')

    for link in link_list:
        file.write(str(link) + '\n')

    file.close()


def crawl_instagram_data(link_file_name):
    driver = wb.Chrome('chromedriver.exe')
    link_list = []

    with open(link_file_name, 'r') as file:
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
    return feed


def save_to_csv(new_file_name, data_list):
    output = open(new_file_name + '.csv', 'w', encoding='utf-8-sig', newline='')
    wr = csv.writer(output)
    wr.writerow(['date', 'user_id', 'text', 'like', 'tag'])

    for record in data_list:
        wr.writerow(record)

    output.close()


def only_eng_num(word):
    word = re.sub('[^0-9a-zA-Z]', ' ', word).strip()
    dummy_word = word.replace(' ', '')
    if dummy_word.isdigit():
        word = ''
    return word


def pp(word):
    spaces = [' ' * x for x in range(2, 10)]
    for space in spaces:
        if space in word:
            word = word.replace(space, '')
    return word


def extract_tag(text):
    res = []
    data = text.split(' ')
    for word in data:
        if word.startswith('#'):
            res.append(word)

    result = []
    for word in res:
        word = re.sub('[^0-9a-zA-Z]', '', word).strip()
        if len(word) > 1:
            result.append('#' + word)

    return ' '.join(result)


def extract_like(text):
    if type(text) == float:
        return 0
    if text.isdigit():
        return int(text)
    if '좋아요' in text:
        start_location = text.find('좋아요')
        end_location = text.find('개')
        return text[start_location + 3: end_location]
    else:
        return 0
