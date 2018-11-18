import time

import ipfsapi

from search import SearchListener, SearchManager
from util import IpfsUtils, filelist_utils


class Dfs:
    """Main application functions."""

    def __init__(self, IPFS_API_PORT=5001):
        self.api = ipfsapi.connect("127.0.0.1", IPFS_API_PORT)
        self.search_listener = SearchListener(self.api)
        self.search_listener.init_servers_and_listen()

    def search(self, query):
        """Send search request."""
        search_results = SearchManager(self.api).get_search_results(query)
        return search_results

    def share(self, path):
        """Share file(s)/directory(ies)."""  # TODO: Check what to do about the 'y'
        list_of_hashes = IpfsUtils(self.api).add_to_ipfs(path)
        filelist_utils.add_to_filelist(list_of_hashes)

    def download(self):
        """Download a file."""
        # TODO: Implement.

    def cleanup(self, after_seconds):
        time.sleep(after_seconds)
        self.search_listener.close()
