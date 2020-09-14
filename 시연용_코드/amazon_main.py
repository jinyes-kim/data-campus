from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

url_list = []
keyword = ['seaweed', 'chip']

for i in range(1, 6):
    url = "https://www.amazon.com/s?k=" + keyword[0] + '+' + keyword[
        1] + '&rh=n%3A16322721&ref=nb_sb_noss&' + 'page=' + str(i)
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    list_ = soup.select("div.a-section.a-spacing-none.a-spacing-top-small > h2 > a.a-link-normal.a-text-normal")

    for l in list_:
        url_ = l.attrs['href']
        url_list.append("https://www.amazon.com" + url_)
        if len(url_list) >= 3:
            break
    if len(url_list) >= 3:
        break
    driver.close()

url_list = pd.DataFrame( data = {'url_list': url_list})
url_list = url_list[~url_list['url_list'].str.contains("sp_mtf")]


# 상품 리뷰 수집
products = []
stars = []
authors = []
titles = []
comments = []
dates = []

for url in url_list['url_list']:
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    try:
        product = driver.find_element_by_css_selector("#productTitle").text.strip('\n')
        content = driver.find_element_by_css_selector("a.a-link-emphasis.a-text-bold")
        content.click()

        page_source = driver.page_source
        current_url = driver.current_url
        soup = BeautifulSoup(page_source, "html.parser")
        time.sleep(0.5)

        count = soup.find("div", {"data-hook": "cr-filter-info-review-rating-count"}).text
        count = count.replace(',', '')
        a, b = count.split('|')
        counts = re.findall("\d+", b)
        number = int(counts[0]) // 10

        for page in range(1, number + 2):
            address = current_url + '&pageNumber=' + str(page)
            driver.get(address)
            time.sleep(0.5)
            ps = driver.page_source
            soup = BeautifulSoup(ps, "html.parser")

            author = soup.select(
                "div #cm_cr-review_list div.a-row.a-spacing-mini a.a-profile div.a-profile-content span.a-profile-name")
            star_rating = soup.findAll("i", {"data-hook": "review-star-rating"})
            date = soup.findAll("span", {"data-hook": "review-date"})
            title = soup.findAll("a", {"data-hook": "review-title"})
            comment = soup.findAll("span", {"data-hook": "review-body"})

            for a in author:
                authors.append(a.text.strip('\n'))

            for s in star_rating:
                stars.append(s.text.strip('\n'))

            for d in date:
                dates.append(d.text.strip('\n'))

            for t in title:
                titles.append(t.text.strip('\n'))

            for c in comment:
                comments.append(c.text.strip('\n'))
                products.append(product)

        driver.close()

    except:
        pass

        driver.close()

amazon_comment_result = pd.DataFrame( data = {'product' : products, 'date': dates, 'comment' : comments}) ; amazon_comment_result
amazon_comment_result = pd.DataFrame( data = {'author': authors, 'star': stars, 'title' : titles}) ; amazon_comment_result
amazon_comment_result = pd.DataFrame( data = {'product' : products, 'author': authors, 'star': stars, 'date': dates, 'title' : titles, 'comment' : comments}) ; amazon_comment_result
amazon_comment_result.to_csv("amazon_comment_crispy_seaweed_result.csv", index=False)