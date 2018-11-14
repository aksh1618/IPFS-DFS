import os
import pickle
import subprocess

import ipfsapi


class IpfsUtils:
    def __init__(self, IPFS_API_PORT=5001):
        self.api = ipfsapi.connect("127.0.0.1", IPFS_API_PORT)
        # TODO: Move it to appropriate location where it runs during first run only
        self.init_filelist()

    def add_to_ipfs(self, path):
        pwd = os.getcwd()
        # TODO: Account for path being file path
        # TODO: Send absolute path
        os.chdir(path)
        os.chdir("..")

        list_of_hashes = []
        # Size is None for directories
        # TODO: Validate path
        file_hashes = str(
            subprocess.check_output(
                f"ipfs add -r {path}", shell=True, stderr=open(os.devnull, "w")
            )
        ).split("added")[1:]
        file_hashes[-1] = file_hashes[-1][:-1]
        file_hashes = [x[1:-2] for x in file_hashes]
        for filehash in file_hashes:
            size = None
            hash, name = filehash.split(" ")
            if os.path.isfile(name):
                size = os.path.getsize(name)
            list_of_hashes.append({"name": name, "hash": hash, "size": size})
        os.chdir(pwd)
        return list_of_hashes

    def init_filelist(self):
        filelist = {"directories": [], "files": []}
        with open("own.filelist", "wb") as f_list:
            pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_filelist():
        with open("own.filelist", "rb") as f_list:
            filelist = pickle.load(f_list)
        return filelist

    # TODO: This should be in main file.
    def add_to_filelist(self, list_of_hashes):
        filelist = self.get_filelist()
        for fileobject in list_of_hashes:
            temp = filelist
            fullpath = fileobject["name"].split("/")
            for path in fullpath[:-1]:
                path_exists = False
                for i in temp["directories"]:
                    if i["name"] == path:
                        # Already exists
                        path_exists = True
                        temp = i
                if not path_exists:
                    new_object = {"name": path, "directories": [], "files": []}
                    temp["directories"].append(new_object)
                    temp = new_object
            new_object = {
                "name": fullpath[-1],
                "hash": fileobject["hash"],
                "directories": [],
                "files": [],
            }
            if not fileobject["size"]:
                # Is a directory
                dir_or_file = "directories"
            else:
                # Is a file
                dir_or_file = "files"
                new_object["size"] = fileobject["size"]
            path_exists = False
            for i in temp[dir_or_file]:
                if i["name"] == fullpath[-1]:
                    # Already exists
                    # TODO: Check hash to see if a newer version of file/directory is being added
                    path_exists = True
                    temp = i
            if not path_exists:
                temp[dir_or_file].append(new_object)
                temp = new_object
        print(filelist)
        with open("own.filelist", "wb") as f_list:
            pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)

    # TODO: This should be in main file.
    def share(self, path):
        list_of_hashes = self.add_to_ipfs(path)
        self.add_to_filelist(list_of_hashes)


# TODO:
# Make everything static.
# Move app utils to separate file
