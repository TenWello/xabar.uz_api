from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from news.models import News
from urllib.parse import urljoin

class Command(BaseCommand):
    help = "xabar.uz bosh sahifasidan so‘nggi yangiliklarni olib keladi"

    def handle(self, *args, **kwargs):
        base_url = "https://xabar.uz"
        url = base_url + "/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        print("Requesting...", url)
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # "So‘nggi yangiliklar" konteyneri
        main_news = soup.find("div", class_="latest__news-text")
        print("main_news_container:", bool(main_news))
        if not main_news:
            self.stdout.write(self.style.ERROR("Yangiliklar konteyneri topilmadi!"))
            return

        # Barcha yangilik elementlari (rasmli va rasmisiz)
        news_boxes = main_news.select("div.news__item.clickable-block")
        print("Topildi:", len(news_boxes), "ta yangilik")

        for box in news_boxes:
            # Sarlavha va link
            title_tag = box.select_one("p.news__item-title a")
            title = title_tag.text.strip() if title_tag else ""
            link  = urljoin(base_url, title_tag["href"]) if title_tag else ""

            # Vaqt ("Ҳозиргина", "12 дақиқа олдин", "1 соат олдин" yoki "бугун, 11:29")
            meta_tag = box.select_one("p.news__item-meta")
            time_ago = meta_tag.text.strip() if meta_tag else ""

            # Qisqacha matn (tagida class bo‘lmagan birinchi <p>)
            desc_tag = box.select_one("p:not([class])")
            description = desc_tag.text.strip() if desc_tag else ""

            # Rasm (agar bo‘lsa)
            img_tag = box.select_one("img")
            image = urljoin(base_url, img_tag["src"]) if img_tag and img_tag.has_attr("src") else ""

            # Saqlash
            News.objects.update_or_create(
                link=link,
                defaults={
                    "title": title,
                    "description": description,
                    "image": image,
                    "category": "",
                    'time_ago': time_ago,
                    # Agar hozircha narsa bo‘lmasa:
                    "published_at": None,
                }
            )
            print(f"Saqlanmoqda: {title} | {link}")

        self.stdout.write(self.style.SUCCESS("xabar.uz yangiliklari muvaffaqiyatli saqlandi!"))
