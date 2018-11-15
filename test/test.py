import os
import time

import ipfsapi

from search import SearchListener, SearchManager
from util import IpfsUtils

TEST_LIFE = 15  # seconds


def main():
    api = ipfsapi.connect("127.0.0.1", "5001")
    ipfs_utils = IpfsUtils(api)
    ipfs_utils.share("./test_dir")
    SearchManager.search_filelist("file1")
    # search_listener = SearchListener(api)
    # search_listener.init_servers_and_listen()
    # time.sleep(TEST_LIFE)
    # search_listener.close()


if __name__ == "__main__":
    main()

# TODO: Things to test:
# config.is_first_run is false in future runs.
