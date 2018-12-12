import os
import time

import ipfsapi

from search import SearchListener, SearchManager
from util import config_utils, filelist_utils, ipfs_utils


class Dfs:
    """Main application functions."""

    def __init__(self, IPFS_API_PORT=5001):
        # config_utils.init_config()
        config = config_utils.get_config()
        is_first_run = config["internal"]["is_first_run"] == "yes"
        if is_first_run:
            print("First run detected, performing initializations.")
            filelist_utils.init_filelist()
            config["internal"]["is_first_run"] = "no"
            config_utils.write_config(config)
        self.api = ipfsapi.connect("localhost", IPFS_API_PORT)
        self.search_listener = SearchListener(self.api)
        self.search_listener.init_servers_and_listen()

    def search(self, query):
        """ Send search request. Returns [{"name": , "hash": , "size": , "path": }, ...]."""
        search_results = SearchManager(self.api).get_search_results(query)
        return search_results

    def share(self, path):
        """Share file(s)/directory(ies)."""  # TODO: Check what to do about the 'y'
        if not os.path.exists(path):
            return False
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
