import os
import random
import subprocess
import traceback
from pathlib import Path

import toga
from toga.style.pack import *

from dfs import Dfs

### TODO: Make OS call ipfs swarm connect /ip4/13.76.195.242/tcp/4001/ipfs/QmU5a4TYjuiuBdQwU2ycm6ArTTwWatWVUTS3w93cJKedKU (IPDC)
CONNECT_COMMAND = "ipfs swarm connect /ip4/13.76.195.242/tcp/4001/ipfs/QmU5a4TYjuiuBdQwU2ycm6ArTTwWatWVUTS3w93cJKedKU"


class DfsApp(toga.App):
    def startup(self):
        # Initialization
        self.dfs = Dfs()

        self.main_window = toga.MainWindow(title=self.name, size=(1366, 720))
        self.main_container = toga.SplitContainer(
            style=Pack(flex=1, padding=(0, 5, -62, 5)),
            direction=toga.SplitContainer.HORIZONTAL,
        )
        self.search_results_table = toga.Table(
            headings=["Name", "Size", "Hash"], on_select=self.download, data=[]
        )
        self.logs_table = toga.Table(headings=["Category", "Detail"], data=[])
        self.search_query_input = toga.TextInput(
            placeholder="Search Query", style=Pack(flex=1)
        )
        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.search_query_input,
                        toga.Button(
                            "Search",
                            on_press=self.search,
                            style=Pack(width=80, padding_left=5),
                        ),
                    ],
                    style=Pack(direction=ROW, alignment=CENTER, padding=(70, 5, 5, 5)),
                ),
                self.main_container,
            ],
            style=Pack(direction=COLUMN),
        )
        self.main_container.content = [self.search_results_table, self.logs_table]
        add_file_cmd = toga.Command(
            self.share,
            label="Add File",
            tooltip="Select file to share",
            icon=Path("./res/icons/baseline_add_black_18dp.png").absolute(),
        )
        add_folder_cmd = toga.Command(
            self.share,
            label="Add Folder",
            tooltip="Select folder to share",
            icon=Path("./res/icons/baseline_add_black_18dp.png").absolute(),
        )
        # self.commands.add(add_file_cmd)
        self.main_window.toolbar.add(add_file_cmd, add_folder_cmd)
        self.main_window.content = box
        self.main_window.show()

    def share(self, widget):
        target_type = widget.label.split()[1].lower()
        print(f"_{target_type}_")
        try:
            if target_type == "folder":
                target = self.main_window.select_folder_dialog("Select Folder")
            else:
                target = self.main_window.save_file_dialog("Select File", "none")
            print(f"Sharing {target}")
            if self.dfs.share(target):
                self.main_window.info_dialog(
                    "Success!", f"Shared {target} successfully!!"
                )
            self.log(f"Shared {target_type}", target)
        except ValueError:
            self.error(f"No {target_type} selected!")

    def download(self, table, row):
        print(f"Downloading {row.name}")
        if self.main_window.confirm_dialog(
            "Confirm Download", f"Do you want to download {row.name}?"
        ):
            self.log("Download started", row.name)
            try:
                self.dfs.download(row.hash, row.name)
            except:
                self.error(f"Failed to download {row.name}!")
                self.log("Download failed", row.name)
                traceback.print_exc()
            self.log("Download completed", row.name)

    def search(self, widget):
        try:
            subprocess.check_output(
                        CONNECT_COMMAND, shell=True, stderr=open(os.devnull, "w")
                    )
        except:
            self.error("No peers found!")
        self.search_results_table.data = []
        query = self.search_query_input.value
        print(f"Searching for {query}")
        self.log("Searched for", query)
        search_results = self.dfs.search(query)
        print(f"\n\nresults: {search_results}\n\n")
        # TODO: Handle duplicates.
        for search_result in search_results:
            self.search_results_table.data.append(
                search_result["name"], search_result["size"], search_result["hash"]
            )
        self.log("Search results", f"{len(search_results)} results for {query}")

    def error(self, message):
        self.main_window.error_dialog("Error!", message)

    def log(self, category, detail):
        self.logs_table.data.append(category, detail)


def main():
    app = DfsApp("IPFS DFS v0.1_alpha", "app.aksh.ipfs-dfs")
    return app


if __name__ == "__main__":
    main().main_loop()
