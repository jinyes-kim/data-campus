from instagram import insta_api as insta

keyword = input("Input Keyword: ")

link_list = insta.crawl_insta_link(keyword, "tempcrawlingbot2", "")
insta.save_links_to_txt("topic_link", link_list)
data_list = insta.crawl_instagram_data("topic_link.txt")
insta.save_to_csv("instagram_data.csv", data_list)


