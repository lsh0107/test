# 2022-01-PROJECT-GROUP2

# Online Bookstore Platform Big Data Analysis

## Team2 Member
* 2019102157 컴퓨터공학과 김서현
* 2019110632 컴퓨터공학과 윤희찬
* 2019110633 컴퓨터공학과 이상혁

## System Design

<img width="692" alt="image" src="https://user-images.githubusercontent.com/68395698/174059978-8bde5714-c82c-4eef-a777-052c10dc1506.png">

## Data
* [문화빅데이터플랫폼 도서별 키워드 정보](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=f183c145-fb5a-49da-a72e-35e16e3de833) 900MB
* [문화빅데이터플랫폼 도서별 상세정보](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=63513d7b-9b87-4ec1-a398-0a18ecc45411) 2.7GB
* [문화빅데이터플랫폼 동시대출정보](https://www.culture.go.kr/bigdata/user/data_market/detail.do?id=ae5bd687-c20f-4658-bf40-16eb6bbca9be#) 56MB
* naverbook_info_and_url.csv 5MB
* book_isbn_and_trailer.csv 20MB
* book_data.csv 2MB
* review 350MB

## Data Analysis using Spark
* 동시대출 정보 기반 도서 추천 데이터 분석
* 추천을 위한 도서 유사도 분석
  * [PORORO Semantic Textual Similarity](https://kakaobrain.github.io/pororo/text_cls/sts.html)
  * [Word2Vec](https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.ml.feature.Word2Vec.html)
* 서점 플랫폼 데이터 분석
* 트렌드 키워드 분석

## Service & Visualize
[책나와](http://booknawa.seohyuni.com/)

### Main Page
<img width="1423" alt="image" src="https://user-images.githubusercontent.com/68395698/174063121-a137b57e-c3d6-4ebe-9a6d-a093d757f3e6.png">

### Visualize
<img width="1426" alt="image" src="https://user-images.githubusercontent.com/68395698/174063184-54eea4e9-404f-4bde-934b-781cbd115d9f.png">

<img width="1424" alt="image" src="https://user-images.githubusercontent.com/68395698/174063280-bab5a92c-7e81-4dca-b31d-67642a7b46b6.png">


<img width="1414" alt="image" src="https://user-images.githubusercontent.com/68395698/174063233-92c16b8b-7db7-4396-b88c-329fc4daa06a.png">



## Feature
1. 4대 서점 플랫폼 통합 정보

한국 인기 온라인 서점 플랫폼 알라딘, 교보문고, Yes24, 인터파크도서의 가격, 별점, 리뷰를 한눈에 확인할 수 있습니다.

2. 도서 추천

NLP 기반 빅데이터 처리를 통해 유사한 내용의 도서와, 국립중앙도서관 동시대출정보를 바탕으로 함께 읽으면 좋은 도서를 추천해드립니다.

3. 서점&도서 빅데이터 분석

서점별 특징 비교 분석 / 워드클라우드를 통한 도서 최신 트렌드를 파악할 수 있습니다.

## Scrum

노션을 이용하여 스크럼 정리 및 일정 관리, 에러 및 정보 공유를 진행하였습니다.

<img width="1428" alt="image" src="https://user-images.githubusercontent.com/68395698/174233800-b856c50b-af2a-416b-92d6-45609554e364.png">

<img width="1432" alt="image" src="https://user-images.githubusercontent.com/68395698/174234189-f71f38b3-5fce-4d5b-bd71-bbf41c936252.png">

<img width="1429" alt="image" src="https://user-images.githubusercontent.com/68395698/174234216-148f4b91-c4e0-4e1d-8f08-4e3db8a474b3.png">
