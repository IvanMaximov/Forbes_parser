'''
This module provides a class for parsing the latest articles from Forbes.

It handles requests through proxies, processes the response to extract and clean article data.
'''
import requests
from requests.auth import HTTPProxyAuth

from config import MAX_RETRIES, RETRY_DELAY
from utils import TextCleaner, convert_unix_to_datetime, retry_request, logger


text_cleaner = TextCleaner()


class ForbesParser:
    '''
    Parser for retrieving and processing the latest articles from Forbes.

    This class handles requests through proxies and processes the response to extract
    and clean article data.
    '''

    def __init__(self, proxy: dict[str, str]) -> None:
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5,ru;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Connection': 'keep-alive',
        }
        self.proxies = {
            'http': f'http://{proxy["proxy_host"]}:{proxy["proxy_port"]}'
        }
        self.proxy_auth = HTTPProxyAuth(proxy['proxy_user'], proxy['proxy_pass'])


    def parse_latest_articles(self, tags: dict[str, str]) -> dict[str, list[dict]]:
        '''
        Parses the latest articles for a given set of tags.

        :param tags: A tuple of tag URLs to parse articles from.

        :return list of articles: A list of dictionaries containing article information.
        '''
        logger.info('Start parsing articles from Forbes')
        articles = {}
        unique_urls = set()

        for tag_name, tag_url in tags.items():
            articles[tag_name] = []
            articles_info = self._parse_articles_from_tag(tag_url)

            for article in articles_info:
                article_url = article['url']
                if article_url not in unique_urls:
                    article['text'] = self._parse_article_text(article_url)
                    articles[tag_name].append(article)

        logger.info(f'Finish parsing articles from Forbes')
        return articles


    @retry_request(MAX_RETRIES, RETRY_DELAY)
    def send_request(self, url: str) -> dict[str, str | int]:
        '''
        Sends a GET request to the given URL.

        :param url: The URL to send the request to.

        :return reponse content: The JSON response content as a dictionary.
        '''
        response = requests.get(url=url, headers=self.headers, proxies=self.proxies, auth=self.proxy_auth, timeout=10)
        response.raise_for_status()
        content = response.json()
        return content
    

    @staticmethod
    def _get_article_text(article_info: dict) -> str:
        '''
        Extracts and cleans the main text from an article.

        :param article_info: A dictionary containing article details, including its body.

        :return text: The cleaned text content of the article.
        '''
        article_text = ''

        try:
            paragraphs = article_info['body']

            for paragraph in paragraphs:
                if paragraph['type'] == 'paragraph':
                    text = paragraph['data']['text']
                    clean_text = text_cleaner.clean_text(text)
                    article_text += clean_text + ' '

        except KeyError as ke:
            logger.error(f'Failed to get article text. Response structure has changed. Error: {ke}.')

        return article_text.strip()
         

    def _parse_article_text(self, article_url: str) -> str:
        '''
        Retrieves and cleans the text content of an article.

        :param article_url: The URL of the article.

        :return text: The cleaned text of the article.
        '''
        article_url = article_url.replace('https://www.forbes.ru/', '')
        article_url = 'https://www.forbes.ru/api/pub/article?url_alias=' + article_url

        article_info = self.send_request(article_url)
        article_text = self._get_article_text(article_info)
        return article_text
    

    @staticmethod
    def _get_articles_info(response: dict) -> list[dict]:
        '''
        Extracts information about articles from the API response.

        :param response: The JSON response containing article data.

        :return articles info: A list of dictionaries with article details, including title, 
                                description, URL, and publish date.
        '''
        articles_info = []

        articles = response['articles']

        try:
            for article in articles:
                article_info = {
                    'title': article['title'],
                    'description': article['subtitle'],
                    'url': 'https://www.forbes.ru/' + article['url_alias'],
                    'publish_date': convert_unix_to_datetime(article['time'])
                }
                articles_info.append(article_info)

        except KeyError as ke:
            logger.error(f'Failed to get articles info. Response structure has changed. Error: {ke}.')

        return articles_info


    def _parse_articles_from_tag(self, tag_url: str) -> list[dict]:
        '''
        Parses articles from a specific tag URL.

        :param tag_url: The tag URL to parse articles from.

        :return articles content: A list of dictionaries containing articles information.
        '''
        tag_name = tag_url.split('%2F')[1]
        logger.info(f'Start parsing news from tag {tag_name}.')

        response = self.send_request(tag_url)

        if not response:
            return []

        articles_info = self._get_articles_info(response)

        logger.info(f'Finish parsing news from tag {tag_name}')
        return articles_info
