from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE_PATH = (Path.home() / ".ipfs-dfs" / "config.ini").absolute()


# @first_run
def init_config():
    """Initialize config with default values."""
    # TODO: Only to be run on first run.
    config = ConfigParser()
    # TODO: Maybe include the file itself and read from it instead of creating?
    # TODO: Ensure that this changes on first run.
    config["internal"] = {"is_first_run": "yes"}
    config["paths"] = {
        "app_dir": str((Path.home() / ".ipfs-dfs").absolute()),
        "filelist_dir": "%(app_dir)s/filelists",
        "own_filelist": "%(filelist_dir)s/own.filelist",
    }
    write_config(config)


def get_config():
    """Get current config."""
    config = ConfigParser()
    config.read(CONFIG_FILE_PATH)
    # TODO: Fix this.
    if not "paths" in config:
        init_config()
        config.read(CONFIG_FILE_PATH)
    return config


def write_config(config):
    """Write config to config file."""
    CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config.write(config_file)
