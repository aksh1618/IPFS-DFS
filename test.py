import time

import ipfsapi

from search.search_listener import SearchListener
from search.search_manager import SearchManager
from util.ipfs_utils import IpfsUtils

TEST_LIFE = 15  # seconds


def main():
    api = ipfsapi.connect("127.0.0.1", "5001")
    ipfs_utils = IpfsUtils(api)
    ipfs_utils.share("./test_dir")
    SearchManager(api).search_filelist("file1")
    # search_listener = SearchListener(api)
    # search_listener.init_servers_and_listen()
    # time.sleep(TEST_LIFE)
    # search_listener.close()


if __name__ == "__main__":
    main()
