"""
crawl #kwd tag link

"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup
from time import sleep
#import csv

# input keyword
kwd = input("keyword: ")


#login info
driver = wb.Chrome('chromedriver.exe')
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

id = 'tempcrawlingbot2'
password = ''
id_input = driver.find_elements_by_css_selector('#loginForm > div > div:nth-child(1) > div > label > input')[0]
id_input.send_keys(id)
password_input = driver.find_elements_by_css_selector('#loginForm > div > div:nth-child(2) > div > label > input')[0]
password_input.send_keys(password)
password_input.submit()
sleep(3)


# target page
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
    sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(30)
        new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(180)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue


print(len(item_link))

file = open('topic_link.txt', 'w')

for link in item_link:
    file.write(str(link) + '\n')

file.close()
