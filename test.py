import time

from ipfs_utils import IpfsUtils
from search.search_listener import SearchListener
from search.search_manager import SearchManager

TEST_LIFE = 15  # seconds


def main():
    ipfs_utils = IpfsUtils()
    ipfs_utils.share("./test_dir")
    SearchManager().search_filelist('file1')
    # search_listener = SearchListener()
    # search_listener.init_servers_and_listen()
    # time.sleep(TEST_LIFE)
    # search_listener.close()


if __name__ == '__main__':
    main()
