import requests
from bs4 import BeautifulSoup
# from requests.api import head
import time
from random import randrange
import json
headers = {

}
# Тут будут загалови сайта


def get_art_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    # В первую очередь
    # with open('index.html', 'w') as file:
    #     file.write(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('span', class_='navigations').find_all('a')[-1].text)
    art_urls_list = list()

    for page in range(1, pagination_count + 1):
        response = s.get(url=f'site.coms/news/page/{page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        art_urls = soup.find_all('a', class_='post-title-a')

        for a_urls in art_urls:
            art_url = a_urls.get('href')
            art_urls_list.append(art_url)
        time.sleep(randrange(2, 5))
        print(f'Обработано {page}/{pagination_count}')

    with open('art_urls.txt', 'w', encoding='utf=8') as file:
        for url in art_urls_list:
            file.write(url + '\n')

    return 'Работу по сбору ссылок завершено'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    url_list_count = len(urls_list)
    s = requests.Session()
    result_data = list()
    for index, url in enumerate(urls_list):
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        art_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
        art_date = soup.find('div', class_='post').find('div', class_='tile-views').text.strip()
        art_img = 'site.coms{}'.format(
            soup.find('div', class_='post-media-full').find('img').get('src')
        )
        art_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')
        result_data.append({
            'Original_url': url,
            'Atr_title': art_title,
            'Data': art_date,
            'Img': art_img,
            'Text': art_text
        })
        time.sleep(randrange(2, 5))
        print('Обработано {}/{}'.format(
            index + 1,
            url_list_count
        ))
    with open('result.json', 'w', encoding='utf=8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    # print(get_art_urls(url='site.coms/'))
    get_data('art_urls.txt')


if __name__ == '__main__':
    main()
