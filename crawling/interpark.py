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

    for i in range(6468, 10000):
        info = book_info[i]
        try:
            book_id = info[2]
            url = info[10]

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
        except:
            continue

        # 스크롤해서 페이지 끝까지 내리기
        before_location = driver.execute_script("return window.pageYOffset") 
        while True:
            driver.execute_script("window.scrollTo(0,{})".format(before_location + 3000)) 
            time.sleep(0.5)
            after_location = driver.execute_script("return window.pageYOffset")
            if before_location == after_location: break
            else:
                before_location = driver.execute_script("return window.pageYOffset")
        print(book_id)

        try:
            # 리뷰
            reView_list = driver.find_elements(By.XPATH, "//ul[@class='reViewList']/li")
            print("리뷰 갯수: ", len(reView_list))
            if len(reView_list) == 0:
                with open("interpark_review_1.csv", 'a', encoding='utf-8-sig') as OR:
                    OR.write(str(book_id)+","+" "+","+" "+'\n')
            for i in range(len(reView_list)):
                # 리뷰 별점
                reView_rating = reView_list[i].find_element(By.CLASS_NAME, "star_on").get_attribute("style")
                reView_rating = int(reView_rating.strip('width:').rstrip('%;'))/20

                # 리뷰
                more_path = "//ul[@class='reViewList']/li["+str(i+1)+"]/a[@class='bt_moreTxt']"
                driver.find_element(By.XPATH, more_path).send_keys(Keys.ENTER) # 펼쳐보기 클릭
                time.sleep(0.3)
                review_path = "//ul[@class='reViewList']/li["+str(i+1)+"]/div[@class='contentBox']/span[@class='hidden']"
                reView = reView_list[i].find_element(By.XPATH, review_path).text
                reView = reView.replace('"', "'")
                reView = '"'+reView+'"'
                with open("interpark_review_1.csv", 'a', encoding='utf-8-sig') as r:
                    r.write(str(book_id)+","+str(reView_rating)+","+reView+'\n')
        except:
            with open("interpark_review_1.csv", 'a', encoding='utf-8-sig') as r:
                r.write(str(book_id)+","+" "+","+" "+'\n')
