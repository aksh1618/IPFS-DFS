from dfs import Dfs


def test_share():
    dfs_instance = Dfs()
    dfs_instance.share("test/test_dir")


# TODO: Things to test:
# config.is_first_run is false in future runs.
