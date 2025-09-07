import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

def create_english_word_cloud_from_book_titles():
  
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_titles_text = ""
    page_num = 1
    max_pages = 5 

    print("英語の書籍タイトルのスクレイピングを開始します...")
    while page_num <= max_pages:
        url = base_url.format(page_num)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')

            if not books:
                print(f"ページ {page_num} に書籍が見つかりませんでした。スクレイピングを終了します。")
                break
            
            for book in books:
                title = book.h3.a['title']
                all_titles_text += " " + title.lower() 
            
            print(f"ページ {page_num} のタイトルを取得しました。")
            page_num += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")
            break

    if not all_titles_text:
        print("スクレイピングされたテキストがありませんでした。")
        return

  
    wordcloud = WordCloud(
        background_color="white",
        width=800,
        height=600,
        max_words=100
    ).generate(all_titles_text)

    
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    wordcloud.to_file("books_english_wordcloud.png")
    print("\n英語のワードクラウドが 'books_english_wordcloud.png' として保存されました。")


create_english_word_cloud_from_book_titles()