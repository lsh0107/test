import csv
from msilib.schema import Directory
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def get_review():
    book_info = list()

    book_info_file_name = "book_info_and_bookstore_url.csv"

    with open(book_info_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            book_info.append(line)

    for i in range(13993, len(book_info)):
        info = book_info[i] 
        try:
            book_id = info[2]
            url = info[7]
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)

            platform_soup = BeautifulSoup(driver.page_source, 'html.parser')
        except:
            continue
        

        # 스크롤해서 페이지 끝까지 내리기
        before_location = driver.execute_script("return window.pageYOffset") 
        while True:
            driver.execute_script("window.scrollTo(0,{})".format(before_location + 800)) 
            time.sleep(0.5)
            after_location = driver.execute_script("return window.pageYOffset")
            if before_location == after_location: break
            else:
                before_location = driver.execute_script("return window.pageYOffset")
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, "//*[@id='tabTotal']").send_keys(Keys.ENTER)
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[@id='tabMyReviewTotal']").send_keys(Keys.ENTER)
            time.sleep(1)
        except:
            continue

        print(book_id)    
        try:
            reviews = driver.find_elements(By.CLASS_NAME, "hundred_list")
            # 100자
            Hundred_review = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'spnPaper')]/a[1]")
            print("짧은 리뷰 갯수: ", len(Hundred_review))
            if len(Hundred_review) == 0:
                with open("aladin_short_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                    review100.write(str(book_id)+","+" "+","+" "+'\n')
            for i in range(len(Hundred_review)):
                # 100자 리뷰 별점
                Hundred_star = driver.find_element(By.XPATH, f"//*[@id='CommentReviewList']/div[1]/ul/div[{2*i+1}]/div[1]")
                count_star = 0
                for image in Hundred_star.find_elements(By.TAG_NAME, "img"):
                    if image.get_attribute("src") == "https://image.aladin.co.kr/img/shop/2018/icon_star_on.png":
                        count_star += 1
                sr = Hundred_review[i].text
                sr = sr.replace('"', "'")
                sr = '"'+sr+'"'
                with open("aladin_short_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                    review100.write(str(book_id)+","+str(count_star)+","+sr+'\n')
        except:
            with open("aladin_short_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                review100.write(str(book_id)+","+" "+","+" "+'\n')

        try:
            # 마이리뷰
            my_review = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Ere_prod_mblog_box np_myreview')]//div[starts-with(@id, 'divPaper')]")
            click = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Ere_prod_mblog_box np_myreview')]//a[starts-with(@onclick, 'fn_show_mypaper_utf8')]")
            for k in range(len(click)):
                click[k].send_keys(Keys.ENTER)
            time.sleep(1)    
            if len(my_review) == 0:
                with open("aladin_long_review_3.csv", 'a', encoding='utf-8-sig') as myreview:
                    myreview.write(str(book_id)+","+" "+","+" "+'\n')
            csl = []
            my_star = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Ere_prod_mblog_box np_myreview')]//div[@class='HL_star']")
            print("긴 리뷰 갯수: ", len(my_star))
            for j in range(len(my_star)):
                # 마이 리뷰 별점
                count_star = 0
                for image in my_star[j].find_elements(By.TAG_NAME, "img"):
                    if image.get_attribute("src") == "https://image.aladin.co.kr/img/shop/2018/icon_star_on.png":
                        count_star += 1
                csl.append(count_star)
            rl = []
            my_review = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Ere_prod_mblog_box np_myreview')]//div[@class='paper-contents']")
            for l in range(len(my_review)):
                try:
                    review = my_review[l].find_element(By.TAG_NAME, "a").text
                    review = review.replace('"', "'")
                    review = '"'+review+'"'
                    rl.append(review)
                    with open("aladin_long_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                        review100.write(str(book_id)+","+str(csl[l])+","+review+'\n')
                except NoSuchElementException:
                    try:
                        temp = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Ere_prod_mblog_box np_myreview')]//div[@class='hundred_list']")
                        review1 = temp[l].find_element(By.CSS_SELECTOR, "[id^='divPaper']").text
                        review1 = review1.replace('"', "'")
                        review1 = '"'+review1+'"'
                        with open("aladin_long_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                            review100.write(str(book_id)+","+str(csl[l])+","+review1+'\n')
                    except NoSuchElementException:
                        with open("aladin_long_review_3.csv", 'a', encoding='utf-8-sig') as review100:
                            review100.write(str(book_id)+","+str(csl[l])+","+" "+'\n')
        except:
            with open("aladin_long_review_3.csv", 'a', encoding='utf-8-sig') as myreview:
                myreview.write(str(book_id)+","+" "+","+" "+'\n')

