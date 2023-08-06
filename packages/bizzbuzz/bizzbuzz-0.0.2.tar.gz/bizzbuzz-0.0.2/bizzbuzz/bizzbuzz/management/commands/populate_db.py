from urllib.request import urlopen
from django.core.management.base import BaseCommand
from bizzbuzz.models import News
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):
    def _delete_everything(self):   #clear out all news in DB, just in case
        News.objects.all().delete()

    def _forbes(self):
        req = requests.get('https://www.forbes.com/business')
        soup = BeautifulSoup(req.content, features='html.parser')

        urls = []
        titles = []
        summary = []

        # finds each article
        articles = soup.findAll('h2')

        for article in articles:
            if article.a is not None:
                url = (article.a['href'])
                req = requests.get(url)
                soup = BeautifulSoup(req.content, features='html.parser')
                first_para = soup.find('div', class_="article-body-container")
                if first_para is None:
                    continue
                first_line = first_para.find('p').text
                titles.append(soup.find('title').text)
                urls.append(url)
                summary.append(first_line)

        title_url_map = zip(titles, urls, summary)
        for x, y, z in title_url_map:
            article = News(title=x, url=y, summary=z)
            article.save()


    def _BI(self):
        # In order: Tech, Finance, Strategy, Retail, Executive, Prime, Intelligence, Politics, Transportation, Markets,
        # Science, News, Media, Enterprise
        BIurls = ["https://www.businessinsider.com/sai", "https://www.businessinsider.com/clusterstock",
                  "https://www.businessinsider.com/warroom", "https://www.businessinsider.com/retail",
                  "https://www.businessinsider.com/thelife", "https://www.businessinsider.com/prime",
                  "https://www.businessinsider.com/research", "https://www.businessinsider.com/politics",
                  "https://www.businessinsider.com/transportation", "https://www.businessinsider.com/moneygame",
                  "https://www.businessinsider.com/science", "https://www.businessinsider.com/news",
                  "https://www.businessinsider.com/media", "https://www.businessinsider.com/enterprise"]

        urls = []
        titles = []
        summary = []

        for scrape in BIurls:
            req = requests.get(scrape)
            soup = BeautifulSoup(req.content, 'lxml')

            #Finds all of the titles, urls, and summaries of each article (top 3 of each URL)
            for div in soup.find_all("div", class_="top-vertical-trio-item"):
                a_tag = div.find("a", class_="tout-title-link")
                title = a_tag.text
                if title in titles:     #don't add articles that are already going to be added to the DB
                    continue
                else:
                    titles.append(title)
                    if a_tag.attrs["href"][0] == "/":
                        urls.append("https://businessinsider.com" + a_tag.attrs["href"])
                    else:
                        urls.append(a_tag.attrs["href"])
                    summary_tag = div.find("div", class_="tout-copy three-column")
                    summary.append(summary_tag.text.strip())

        for x, y, z in zip(titles,urls, summary):
            article = News(title=x, url=y, summary=z)
            article.save()

    def handle(self, *args, **options):
        self._delete_everything()
        self._forbes()
        self._BI()