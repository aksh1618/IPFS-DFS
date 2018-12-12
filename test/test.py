import os
from dfs import Dfs

TEST_LIFE = 60  # seconds


def test_share():
    # TODO: complete this
    dfs_instance = Dfs()
    test_path = os.path.abspath("test/test_dir") 
    dfs_instance.share(test_path)
    dfs_instance.cleanup(TEST_LIFE)

def test_search(query):
    dfs_instance = Dfs()
    results = dfs_instance.search(query)
    print(results)
    dfs_instance.cleanup(TEST_LIFE)

def test_download(file_hash):
    dfs_instance = Dfs()
    ss = dfs_instance.download(file_hash, "hello.txt")
    print(ss)

# TODO: Things to test:
# config.is_first_run is false in future runs.
