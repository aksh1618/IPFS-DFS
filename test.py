import time
from search.search_listener import SearchListener
from search.search_manager import SearchManager


TEST_LIFE = 15  # seconds


def main():
    SearchManager().search_filelist()
    # search_listener = SearchListener()
    # search_listener.init_servers_and_listen()
    # time.sleep(TEST_LIFE)
    # search_listener.close()


if __name__ == '__main__':
    main()
