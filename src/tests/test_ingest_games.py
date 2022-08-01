'''Tests for ingest_games module'''

from os import remove
from bs4 import BeautifulSoup
import loaders.ingest_games as ingest_games
from loaders.database_helpers import connect_to_db
from loaders.models import Mechanic, Category

TEST_DB_FILE = 'src/tests/test_db.sqlite3'
TEST_XML_FILE = 'src/tests/test_data.xml'
TEST_MECH_ID_LIST = [2001, 2916, 2912]
TEST_CAT_ID_LIST = [1009, 1022, 1002, 2687]


def setup_xml_file():
    with open(TEST_XML_FILE, 'rb') as file:
        return BeautifulSoup(file.read(), features='xml')


def setup_test_db():
    url = f'sqlite+pysqlite:///{TEST_DB_FILE}'
    return connect_to_db(url)


def teardown_test_db(session):
    session.close()
    

def test_transform_game_data():
    test_soup = setup_xml_file()
    test_dict = ingest_games.transform_game_data(test_soup)
    assert isinstance(test_dict, dict), 'transform_game_data() did not return a dict'


def test_transform_game_class_ids_mechanic():
    test_soup = setup_xml_file()
    test_list = ingest_games.transform_game_class_ids('mechanic', test_soup)
    assert isinstance(test_list, list), 'transform_game_class_ids() did not return a list'
    for i in test_list:
        assert isinstance(i, int), 'Non-integer ID returned within id_list'


def test_load_game_classifications_mechanics():
    session, test_ids = setup_test_db(), TEST_MECH_ID_LIST
    test_list = ingest_games.load_game_classifications(session,
                                                       Mechanic,
                                                       test_ids)
    assert isinstance(test_list, list), 'transform_game_class_ids() did not return a list'
    assert len(test_list) == len(test_ids), f'Did not get expected number of elements in list: {len(test_ids)}. Got {len(test_list)} instead'
    for i in test_list:
        assert isinstance(i, Mechanic), 'load_game_classifications(...,Mechanic,...) returned a non Mechanic object within list'
    teardown_test_db(session)


def test_load_game_classifications_categories():
    session, test_ids = setup_test_db(), TEST_CAT_ID_LIST
    test_list = ingest_games.load_game_classifications(session,
                                                       Category,
                                                       test_ids)
    assert isinstance(test_list, list), 'transform_game_class_ids() did not return a list'
    assert len(test_list) == len(test_ids), f'Did not get expected number of elements in list: {len(test_ids)}. Got {len(test_list)} instead'
    for i in test_list:
        assert isinstance(i, Category), 'load_game_classifications(...,Category,...) returned a non Category object within list'
    teardown_test_db(session)
