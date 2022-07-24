"""Tests for loader.scraper_browse_id"""

import os
from shutil import rmtree
from requests import Response
from loaders import scraper_helpers

PATH = 'test_data'
FILENAME = 'test.txt'
CONTENTS = 'test contents'

def teardown_files(PATH):
    rmtree(PATH)


def test_save_file_new_folder():
    if os.path.exists(PATH):
        rmtree(PATH)
    scraper_helpers.save_file(PATH, FILENAME, CONTENTS.encode())
    assert os.path.exists(PATH), 'Directory not created'
    assert os.path.exists(f'{PATH}/{FILENAME}'), 'File not created'
    with open(f'{PATH}/{FILENAME}', 'rb') as file:
        read_contents = file.read().decode()
    assert read_contents == CONTENTS, 'Incorrect contents written'
    teardown_files(PATH)
    

def test_save_file_new_file():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    scraper_helpers.save_file(PATH, FILENAME, CONTENTS.encode())
    assert os.path.exists(PATH), 'Directory not created'
    assert os.path.exists(f'{PATH}/{FILENAME}'), 'File not created'
    with open(f'{PATH}/{FILENAME}', 'rb') as file:
        read_contents = file.read().decode()
    assert read_contents == CONTENTS, 'Incorrect content written'
    teardown_files(PATH)


def test_save_file_existing_file():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    if not os.path.exists(f'{PATH}/{FILENAME}'):
        with open(f'{PATH}/{FILENAME}', 'xb') as file:
            file.write('preexisting code'.encode())
    scraper_helpers.save_file(PATH, FILENAME, CONTENTS.encode())
    assert os.path.exists(PATH), 'Directory not created'
    assert os.path.exists(f'{PATH}/{FILENAME}'), 'File not created'
    with open(f'{PATH}/{FILENAME}', 'rb') as file:
        read_contents = file.read().decode()
    assert read_contents == CONTENTS, 'Incorrect content found'
    teardown_files(PATH)


def test_fetch_page():
    test_url = 'https://boardgamegeek.com/browse/boardgame'
    test_res = scraper_helpers.fetch_page(test_url)
    assert isinstance(test_res, Response), 'Did not return a Response object'
    assert test_res.status_code == 200, 'Unsuccessful get request'
