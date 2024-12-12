'''
Simple logger
'''
import logging
from config import SERVICE_NAME


def setup_logging() -> logging.Logger:
    '''
    Sets up a logger that logs messages to the console with a specified format.
    
    :return logger: A configured logger instance.
    '''
    # Create a logger and set the log level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a console handler to display logs in the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define the log format
    formatter = logging.Formatter(f'%(asctime)s - {SERVICE_NAME} - %(levelname)s - %(message)s')

    # Set the formatter for the console handler
    console_handler.setFormatter(formatter)

    # Attach the handler to the logger
    logger.addHandler(console_handler)

    return logger
