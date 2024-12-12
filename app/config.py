'''
Configuration file for the application.

This module contains constants and settings used throughout the application.
Modify the values here to customize the behavior of the application.
'''
import os


SERVICE_NAME = os.getenv('SERVICE_NAME', 'forbes parser')

# Maximum number of retry attempts for a failed request
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))

# Parsing interval in minutes
PARSING_INTERVAL = int(os.getenv('PARSING_INTERVAL', '60'))
