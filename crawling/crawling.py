import naverbook_info_and_bookstore_url
import book_data
import book_isbn_and_trailer
import aladin
import kyobo
import yes24
import interpark

naverbook_info_and_bookstore_url.get_info()
book_data.crawling_platform()
book_isbn_and_trailer.get_isbn_and_trailer()

aladin.get_review()
kyobo.get_review()
yes24.get_review()
interpark.get_review()
