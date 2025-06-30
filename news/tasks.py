# news/tasks.py
from celery import shared_task
import requests
from bs4 import BeautifulSoup
from news.models import News
from urllib.parse import urljoin

@shared_task
def fetch_xabaruz_latest():
    base_url = "https://xabar.uz"
    resp = requests.get(base_url + "/", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36"
    }, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    main_news = soup.find("div", class_="latest__news-text")
    if not main_news:
        return "Container not found"

    news_boxes = main_news.select("div.news__item.clickable-block")
    for box in news_boxes:
        title_tag = box.select_one("p.news__item-title a")
        title = title_tag.text.strip() if title_tag else ""
        link  = urljoin(base_url, title_tag["href"]) if title_tag else ""
        meta  = box.select_one("p.news__item-meta")
        time_ago = meta.text.strip() if meta else ""
        desc  = box.select_one("p:not([class])")
        description = desc.text.strip() if desc else ""
        img   = box.select_one("img")
        image = urljoin(base_url, img["src"]) if img and img.has_attr("src") else ""

        News.objects.update_or_create(
            link=link,
            defaults={
                "title": title,
                "description": description,
                "image": image,
                "category": "",
                "published_at": None,
            }
        )
    return f"Fetched {len(news_boxes)} items"
