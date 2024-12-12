'''
This module provides tools for cleaning and preprocessing text data.
'''
import re
import time
from datetime import datetime

from bs4 import BeautifulSoup

from logging_presets import setup_logging


logger = setup_logging()


class TextCleaner:
    '''
    Utility class for cleaning text, including removing HTML code and extra spaces.
    '''

    @staticmethod
    def _remove_html_code(text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text()
        clean_text = re.sub(r'&[a-zA-Z]+;', '', clean_text)
        return clean_text.strip()
    

    @staticmethod
    def _remove_double_spaces(text: str) -> str:
        clean_text = text.replace('  ', ' ')
        return clean_text
    

    def clean_text(self, text):
        cleaned_text = self._remove_double_spaces(self._remove_html_code(text))
        return cleaned_text


def retry_request(max_retries: int = 3, delay: int = 6):
    '''
    A decorator to retry a function call up to a specified number of times with a delay.

    :param max_retries: The maximum number of attempts to retry the function (default is 3).
    :param delay: Time in seconds to wait between retries (default is 6).

    :return response content: Response content if the request is successful, or an empty dictionary if the request fails.
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            counter = 0

            while counter < max_retries:
                try:
                    time.sleep(delay)
                    return func(*args, **kwargs)

                except Exception as e:
                    logger.error(f'Failed to send a request. Attempt {counter + 1}/{max_retries}. Error: {e}.')
                    counter += 1

            logger.error(f'Max retries reached for request. Returning empty response.')
            return {}

        return wrapper
    return decorator


def convert_unix_to_datetime(unix_timestamp: int) -> str:
    '''
    Converts a Unix timestamp to a formatted datetime string.
    '''
    dt_object = datetime.fromtimestamp(unix_timestamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')
