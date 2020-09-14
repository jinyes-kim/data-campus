from selenium import webdriver
from time import sleep
import csv

file = open('walmart_data.csv', 'w', newline='')
writer = csv.writer(file)

writer.writerow(['score', 'product', 'author', 'date', 'comment'])
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.walmart.com/search/?query=snack')
sleep(2)
item_boxes = driver.find_elements_by_css_selector("a.product-title-link.line-clamp.line-clamp-2")
item_boxes = item_boxes[0:2]

for i in range(1, len(item_boxes)): #한 화면에 40개, 크롤링 len(item_boxes)
    try:
        driver.find_element_by_xpath('//*[@id="searchProductResult"]/ul/li[' + str(i + 1) + ']').click() # 1위부터 하나씩
        sleep(2)
        product = driver.find_element_by_css_selector("h1.prod-ProductTitle.prod-productTitle-buyBox.font-bold").text
        sub_url = "https://www.walmart.com/reviews/product/" + driver.current_url.split('/').pop()  # see all reviews
        driver.get(sub_url)
        sleep(2)
        repeat = driver.find_elements_by_css_selector("ul.paginator-list li")
        print("item # at: ", i)
        for repeat in range(1): #review-page int(repeat[-1].text) + 1
            driver.get(sub_url + "?page=" + str(repeat))
            sleep(2)
            sub_boxes = driver.find_elements_by_css_selector("div.review")
            for j in range(len(sub_boxes)):
                stars = sub_boxes[j].find_elements_by_css_selector("span.stars-container span.elc-icon.star.star-small.star-rated.elc-icon-star-rating")
                score = len(stars)
                author = sub_boxes[j].find_element_by_css_selector("span.review-footer-userNickname").text
                date = sub_boxes[j].find_element_by_css_selector(".review-date-submissionTime").text
                comment = sub_boxes[j].find_element_by_css_selector("div.review-text").text
                tmp = [score, product, author, date, comment]
                print(tmp)
                writer.writerow(tmp)

    except:
         print("scanning item #" + str(i) + "failed")
    driver.get('https://www.walmart.com/search/?query=snack')

file.close()
driver.close()
