import csv
import urllib.request
from bs4 import BeautifulSoup, NavigableString
from requests import request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.parse

def get_isbn_and_trailer():
    category_file_name = 'book_category.csv'
    # 동적으로 생성되는 값이 있어 selenium 이용
    chrome_options = webdriver.ChromeOptions()

    # 크롬창 숨기기 옵션 추가
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    bookstore = ["알라딘","인터넷 교보문고","예스24","인터파크 도서"]
    # 카테고리 정보 csv 읽어서 저장하기
    category = list()
    with open(category_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            category.append(line)

    book_info_file_name = "book_isbn_and_trailer.csv"

    with open(book_info_file_name, "w", encoding = "utf-8-sig") as f:
        f.write("book_id,book_isbn,book_trailer\n")
        for i in range(1, len(category)): # 첫 칸 헤더 제외
            url = category[i][2]

            # 서브 카테고리별 top 100 & 플랫폼별 주소 가져오기
            for j in range(1,6): # 20개씩 5페이지로 구성되어있다 ## DEMO 5개씩만 가져옴
                # j = 1
                driver.get(url+"&page="+str(j)) 

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                detail_a_list = soup.select("#category_section > ol > li > div > div > a")
                cnt = 0
                for detail_a in detail_a_list:
                    if(cnt == 20):
                        break
                    try:
                        cnt+=1
                        # 네이버 책 도서 상세정보에서 책 정보와 서점 링크 가져오기
                        bookstore_url_dict = dict()
                        detail_url = detail_a.attrs['href']
                        driver.get(detail_url)
                        detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        book_id = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(detail_url).query))["bid"]
                        book_isbn = detail_soup.select_one("a#isbnBtn").parent.next_sibling

                        with open(f'naverbooks_trailer/{book_id}.txt', 'r', encoding="UTF-8") as textfile:
                            data = textfile.read()
                            data = data.replace('"', "'")
                            book_trailer = '"'+data+'"'
                        print(book_id, book_isbn)
                        f.write(str(book_id)+","+book_isbn+","+book_trailer+"\n")
                        print("완료!")

                    except Exception as e:
                        print("[에러]",e)
                        continue


