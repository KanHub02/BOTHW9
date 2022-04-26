from bs4 import BeautifulSoup
import requests

URL = 'https://kaktus.media/?lable=8&date=2022-04-26&order=time'

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
}


def get_requests(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_data_link(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_='Tag--article')
    newslink = []
    for item in items:
        newslink.append(
            {
                "link": item.find("a", class_='ArticleItem--name').get("href"),
                # "image": item.find("div", class_="top100-img").find("img").get("src")
            }
        )
    for i in newslink:
        print(f'\n{i})')
    return newslink[0].values()


def get_data_title(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_='Tag--article')
    newstitle = []

    for item in items:
        newstitle.append(
            {
                "title": item.find("a", class_="ArticleItem--name").get_text(),
            }
        )
    return newstitle[0].values()


def scrapy_script():
    html = get_requests(URL)
    if html.status_code == 200:
        links = []
        links.extend(get_data_link(html.text))
        return links

    else:
        raise Exception("Error in scrapy script function")


def scrapy_script_title():
    html = get_requests(URL)
    if html.status_code == 200:
        titles = []
        titles.extend(get_data_title(html.text))
        return titles
    else:
        raise Exception("Error in scrapy script function")


html = get_requests(URL)
#get_data_link(html.text)