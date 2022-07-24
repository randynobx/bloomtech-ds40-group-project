'''Helper functions for scrapers'''

import os
import requests

def save_file(path: str, filename: str, content: str) -> None:
    '''Save page to file

    Args:
        path (str): path to file location
        filename (str): name of file, with file extension
        content (str): html of page to save
    '''
    filepath = f'{path}/{filename}'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(filepath, 'wb') as file:
        file.write(content)


def fetch_page(url: str) -> requests.Response:
    '''Fetch specified html page

    Args:
        url (str): url of webpage to fetch

    Returns:
        (requests)'''
    return requests.get(url)