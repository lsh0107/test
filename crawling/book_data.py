import csv
import crawling_4_bookstore

def crawling_platform():
    book_info = list()
    book_data = []

    book_info_file_name = "book_info_and_bookstore_url.csv"

    with open(book_info_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            book_info.append(line)

    book_data_file_name = "book_data.csv"

    with open(book_data_file_name, "r",  encoding = "UTF-8") as f:
        rdr = csv.reader(f)
        for line in rdr:
            book_data.append(line)
    data_length = len(book_data)  
    print(data_length)

    if data_length == 0:
        with open(book_data_file_name, "w",  encoding = "utf-8-sig") as f:
            f.write("main_category,sub_category,book_id,book_title,book_author,publisher,publish_date,aladin_price,aladin_star,aladin_review,kyobo_price,kyobo_star,kyobo_review,yes24_price,yes24_star,yes24_review,interpark_price,interpark_star,interpark_review\n")
        data_length += 1
        f.close()

    for i in range(0, len(data_length)):
        with open(book_data_file_name, "a", encoding = "utf-8-sig") as f:
            info = book_info[i]
            try:
                aladin = crawling_4_bookstore.aladin(info[7])
                kyobo = crawling_4_bookstore.kyobo(info[8])
                yes24 = crawling_4_bookstore.yes24(info[9])
                interpark = crawling_4_bookstore.interpark(info[10])
                print(info[0]+","+info[1]+","+info[2]+","+info[3]+","+info[4]+","+info[5]+","+info[6]+","+str(aladin[0])+","+str(aladin[1])+","+str(aladin[2])+","+str(kyobo[0])+","+str(kyobo[1])+","+str(kyobo[2])+","+str(yes24[0])+","+str(yes24[1])+","+str(yes24[2])+","+str(interpark[0])+","+str(interpark[1])+","+str(interpark[2]))
                f.write(info[0]+","+info[1]+","+info[2]+","+info[3]+","+info[4]+","+info[5]+","+info[6]+","+str(aladin[0])+","+str(aladin[1])+","+str(aladin[2])+","+str(kyobo[0])+","+str(kyobo[1])+","+str(kyobo[2])+","+str(yes24[0])+","+str(yes24[1])+","+str(yes24[2])+","+str(interpark[0])+","+str(interpark[1])+","+str(interpark[2])+"\n")
                f.close()
            except Exception as e:
                print("[에러]", e)
                continue



