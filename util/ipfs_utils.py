import os
import pickle
import subprocess

from util import filelist_utils

# TODO: Get this from config
FILELIST_PATH = os.path.abspath("../test/own.filelist")


# TODO: Remove class.
class IpfsUtils:
    def __init__(self, api):
        self.api = api
        # TODO: Move it to appropriate location where it runs during first run only
        filelist_utils.init_filelist()

    def add_to_ipfs(self, path):
        # TODO: Send absolute path

        if not os.path.exists(path):
            # Invalid path
            return []

        list_of_hashes = []
        # Size is None for directories
        # TODO: Validate path
        try:
            file_hashes = str(
                subprocess.check_output(
                    f"ipfs add -r {path}", shell=True, stderr=open(os.devnull, "w")
                )
            ).split("added")[1:]
        except:
            # File addition failed!
            # TODO: Handle it
            return []
        file_hashes[-1] = file_hashes[-1][:-1]
        file_hashes = [x[1:-2] for x in file_hashes]
        for filehash in file_hashes:
            size = None
            hash, name = filehash.split(" ")
            if os.path.isfile(name):
                size = os.path.getsize(name)
            list_of_hashes.append({"name": name, "hash": hash, "size": size})
        return list_of_hashes


# TODO:
# Make everything static.
# Or remove the class altogether in favor of top level functions.
# Move app utils to separate file.
