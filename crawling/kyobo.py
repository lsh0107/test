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
import os

def get_review():
    book_info = list()

    book_info_file_name = "book_info_and_bookstore_url.csv"

    with open(book_info_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            book_info.append(line)

    for i in range(1,len(book_info)):
        info = book_info[i]
        try:
            book_id = info[2]
            url = info[8]
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
        except:
            continue

        # 스크롤해서 페이지 끝까지 내리기
        before_location = driver.execute_script("return window.pageYOffset") 
        while True:
            driver.execute_script("window.scrollTo(0,{})".format(before_location + 700)) 
            time.sleep(0.5)
            after_location = driver.execute_script("return window.pageYOffset")
            if before_location == after_location: break
            else:
                before_location = driver.execute_script("return window.pageYOffset")
        print(book_id)
        try:
            # Klover 리뷰
            Klover_review_list = driver.find_elements(By.XPATH, "//div[@class='box_detail_review']//ul[@class='board_list']/li")
            print("짧은 리뷰 갯수: ", len(Klover_review_list))
            if len(Klover_review_list) == 0:
                with open("kyobo_short_review.csv", 'a', encoding='utf-8-sig') as KR:
                    KR.write(str(book_id)+","+" "+","+" "+'\n')
            for i in range(len(Klover_review_list)):
                # Klover 리뷰 별점
                kloverRating = Klover_review_list[i].find_element(By.CLASS_NAME, "kloverRating").text
                kloverReview = Klover_review_list[i].find_element(By.CLASS_NAME, "comment").text
                kloverRating = kloverRating[-1]
                #print(kloverRating)
                #print(kloverReview)
                kloverReview = kloverReview.replace('"', "'")
                kloverReview = '"'+kloverReview+'"'
                #print("---------------------------------")

                with open("kyobo_short_review.csv", 'a', encoding='utf-8-sig') as KR:
                    KR.write(str(book_id)+","+kloverRating+","+kloverReview+'\n')

        except:
            with open("kyobo_short_review.csv", 'a', encoding='utf-8-sig') as KR:
                KR.write(str(book_id)+","+" "+","+" "+'\n')

        try:
            # 북로그 리뷰
            Booklog_review_list = driver.find_elements(By.XPATH, "//ul[@class='list_detail_booklog']/li")
            print("긴 리뷰 갯수: ", len(Booklog_review_list))
            if len(Booklog_review_list) == 0:
                with open("kyobo_long_review.csv", 'a', encoding='utf-8-sig') as BR:
                    BR.write(str(book_id)+","+" "+","+" "+'\n')
            for j in range(len(Booklog_review_list)):
                # 북로그 리뷰 별점
                BooklogRating = Booklog_review_list[j].find_element(By.TAG_NAME, "img").get_attribute("alt")

                # 북로그 리뷰
                button_path = "//ul[@class='list_detail_booklog']/li["+str(j+1)+"]/div[3]"
                BooklogReview = Booklog_review_list[j].find_element(By.XPATH, button_path).get_attribute("textContent")
                BooklogReview = BooklogReview[:len(BooklogReview)-7] # 맨 끝에 '닫기' 제거하기
                BooklogReview = BooklogReview.replace('"', "'")
                BooklogReview = '"'+BooklogReview+'"'
                BooklogRating = BooklogRating[-2:-1]
                #print(BooklogReview)
                #print("---------------------------------")

                with open("kyobo_long_review.csv", 'a', encoding='utf-8-sig') as BR:
                    BR.write(str(book_id)+","+BooklogRating+","+BooklogReview+'\n')
        except:
            with open("kyobo_long_review.csv", 'a', encoding='utf-8-sig') as BR:
                BR.write(str(book_id)+","+" "+","+" "+'\n')
        print()
        print()
