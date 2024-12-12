import json

from apscheduler.schedulers.blocking import BlockingScheduler

from config import PARSING_INTERVAL
from news_tags import tags
from forbes_parser import ForbesParser


def save_articles_to_file(filename: str, articles: dict[str, list[dict]]):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=2)


def parse_news_articles(forbes_parser: ForbesParser):
    news_articles = forbes_parser.parse_latest_articles(tags)
    save_articles_to_file('news_articles.json', news_articles)


if __name__ == '__main__':
    proxy = {
        'proxy_host': '',
        'proxy_port': '',
        'proxy_user': '',
        'proxy_pass': ''
    }
    forbes_parser = ForbesParser(proxy)

    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: parse_news_articles(forbes_parser), 'interval', minutes=PARSING_INTERVAL)
    scheduler.start()
