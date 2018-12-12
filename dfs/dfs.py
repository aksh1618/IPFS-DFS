import os
import time

import ipfsapi

from search import SearchListener, SearchManager
from util import ipfs_utils, filelist_utils, config_utils


class Dfs:
    """Main application functions."""

    def __init__(self, IPFS_API_PORT=5001):
        config_utils.init_config()
        self.api = ipfsapi.connect("localhost", IPFS_API_PORT)
        self.search_listener = SearchListener(self.api)
        self.search_listener.init_servers_and_listen()
        # TODO: Ensure that this runs only once
        filelist_utils.init_filelist()

    def search(self, query):
        """Send search request."""
        search_results = SearchManager(self.api).get_search_results(query)
        return search_results

    def share(self, path):
        """Share file(s)/directory(ies)."""  # TODO: Check what to do about the 'y'
        if not os.path.exists(path): return False
        list_of_hashes = ipfs_utils.IpfsUtils(self.api).add_to_ipfs(path)
        filelist_utils.add_to_filelist(list_of_hashes)
        return True

    def download(self, file_hash, file_name):
        """Download a file."""
        # TODO: Decide on download location.
        try:
            self.api.get(file_hash)
            os.rename(file_hash, file_name)
            return True
        except:
            return False

    def cleanup(self, after_seconds):
        time.sleep(after_seconds)
        self.search_listener.close()
