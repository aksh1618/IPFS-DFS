import pickle


def init_filelist():
    filelist = {"directories": [], "files": []}
    with open("own.filelist", "wb") as f_list:
        pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)


def get_filelist():
    with open("own.filelist", "rb") as f_list:
        filelist = pickle.load(f_list)
    return filelist


# TODO: This should be in main file.
def add_to_filelist(list_of_hashes):
    filelist = get_filelist()

    for fileobject in list_of_hashes:
        temp_filelist = filelist
        fullpath = fileobject["name"].split("/")

        for path in fullpath[:-1]:
            path_exists = False
            for i in temp_filelist["directories"]:
                if i["name"] == path:
                    # Already exists
                    path_exists = True
                    temp_filelist = i
            if not path_exists:
                new_object = {"name": path, "directories": [], "files": []}
                temp_filelist["directories"].append(new_object)
                temp_filelist = new_object

        name = fullpath[-1]
        new_object = {"name": name, "hash": fileobject["hash"]}

        if not fileobject["size"]:
            # Is a directory
            new_object["directories"] = []
            new_object["files"] = []
            dir_or_file = "directories"
        else:
            # Is a file
            dir_or_file = "files"
            new_object["size"] = fileobject["size"]

        path_exists = False

        for i in temp_filelist[dir_or_file]:
            if i["name"] == name:
                # Already exists
                # TODO: Check hash to see if a newer version of file/directory is being added
                path_exists = True
                temp_filelist = i
                break

        if not path_exists:
            temp_filelist[dir_or_file].append(new_object)
            temp_filelist = new_object

    # TODO: Remove this later
    print(filelist)
    with open("own.filelist", "wb") as f_list:
        pickle.dump(filelist, f_list, pickle.HIGHEST_PROTOCOL)


def search_filelist(query_str):
    own_filelist = get_filelist()
    print(own_filelist)
    results = __recursive_search(own_filelist, "/", query_str)
    return results


def __recursive_search(cur_dir, parent_str, query_str):
    results = []
    for _file in cur_dir["files"]:
        if __match(query_str, parent_str + _file["name"]):
            _file["path"] = parent_str + _file["name"]
            results.append(_file)

    for _dir in cur_dir["directories"]:
        results += __recursive_search(_dir, f"{parent_str}/{_dir['name']}/", query_str)

    return results


def __match(pattern, text):
    return all([word in text for word in pattern.split()])