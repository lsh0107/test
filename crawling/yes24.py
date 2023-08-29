import csv
from msilib.schema import Directory
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def get_review():
    book_info = list()

    book_info_file_name = "book_info_and_bookstore_url.csv"

    with open(book_info_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            book_info.append(line)

    for i in range(13570  , len(book_info)): #len(book_info) 
        info = book_info[i]
        try:
            book_id = info[2]
            url = info[9]

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
        except:
            continue

        # 스크롤해서 페이지 끝까지 내리기
        before_location = driver.execute_script("return window.pageYOffset") 
        while True:
            driver.execute_script("window.scrollTo(0,{})".format(before_location + 1000)) 
            time.sleep(0.5)
            after_location = driver.execute_script("return window.pageYOffset")
            if before_location == after_location: break
            else:
                before_location = driver.execute_script("return window.pageYOffset")
        print(book_id)
        try:
            # 한줄 리뷰
            OneComment_list = driver.find_elements(By.XPATH, "//div[@id='infoset_oneCommentList']//div[@class='cmtInfoBox']")
            print("짧은 리뷰 갯수: ", len(OneComment_list))
            if len(OneComment_list) == 0:
                with open("yes24_short_review_3.csv", 'a', encoding='utf-8-sig') as OR:
                    OR.write(str(book_id)+","+" "+","+" "+'\n')
            for i in range(len(OneComment_list)):
                OneComment_rating = OneComment_list[i].find_element(By.CLASS_NAME, "cmt_rating").text
                OneComment_rating = OneComment_rating[-2:-1]
                OneComment_review = OneComment_list[i].find_element(By.CLASS_NAME, "cmt_cont").text

                OneComment_review = OneComment_review.replace('"', "'")
                OneComment_review = '"'+OneComment_review+'"'
                with open("yes24_short_review_3.csv", 'a', encoding='utf-8-sig') as OR:
                    OR.write(str(book_id)+","+OneComment_rating+","+OneComment_review+'\n')
        except:
            with open("yes24_short_review_3.csv", 'a', encoding='utf-8-sig') as OR:
                OR.write(str(book_id)+","+" "+","+" "+'\n')       

        try:
            # 리뷰
            review_list = driver.find_elements(By.CLASS_NAME, "reviewInfoGrp.lnkExtend")
            print("긴 리뷰 갯수: ", len(review_list))
            if len(review_list) == 0:
                with open("yes24_long_review_3.csv", 'a', encoding='utf-8-sig') as r:
                    r.write(str(book_id)+","+" "+","+" "+'\n')
            for j in range(len(review_list)):
                # 리뷰 별점(내용, 편집/디자인)
                review_rating = review_list[j].find_element(By.CLASS_NAME, "review_rating").text
                review_rating = review_rating.strip('&nbsp;')
                rr1 = review_rating[5:6]
                rr2 = review_rating[-2:-1]
                # 리뷰
                review = review_list[j].find_element(By.CLASS_NAME, "reviewInfoBot.origin").find_element(By.CLASS_NAME, "review_cont").get_attribute("textContent")
                review = review[17:]
                review = review.replace('"', "'")
                review = '"'+review+'"'
                with open("yes24_long_review_3.csv", 'a', encoding='utf-8-sig') as r:
                    r.write(str(book_id)+","+rr1+","+rr2+","+review+'\n')
        except:
            with open("yes24_long_review_3.csv", 'a', encoding='utf-8-sig') as r:
                r.write(str(book_id)+","+" "+","+" "+","+" "+'\n')
        print()
        print()
