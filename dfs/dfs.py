import ipfsapi

from search import SearchListener, SearchManager
from util import IpfsUtils, filelist_utils


class Dfs:
    """Main application functions."""

    def __init__(self, IPFS_API_PORT=5001):
        self.api = ipfsapi.connect("127.0.0.1", IPFS_API_PORT)
        # search_listener = SearchListener(api)
        # search_listener.init_servers_and_listen()
        # time.sleep(TEST_LIFE)
        # search_listener.close()

    def search(self, query):
        """Send search request."""
        search_results = SearchManager(self.api).get_search_results(query)
        # TODO: Send back to UI

    def share(self, path):
        """Share file(s)/directory(ies)."""  # TODO: Check what to do about the 'y'
        list_of_hashes = IpfsUtils(self.api).add_to_ipfs(path)
        filelist_utils.add_to_filelist(list_of_hashes)

    def download(self):
        """Download a file."""
        # TODO: Implement.
