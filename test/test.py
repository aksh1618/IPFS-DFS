from dfs import Dfs

TEST_LIFE = 60  # seconds


def test_share():
    dfs_instance = Dfs()
    dfs_instance.share("test/test_dir")
    dfs_instance.cleanup(TEST_LIFE)


# TODO: Things to test:
# config.is_first_run is false in future runs.
