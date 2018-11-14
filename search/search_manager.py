import atexit
import collections
import ipfsapi
import socket
from ipfs_utils import IpfsUtils

UDP_PORT_NO = 43462
UDP_PORT_NO_V6 = 43463


class SearchManager:
    """Methods for managing search operations."""

    def __init__(self, IPFS_API_PORT=5001):
        # TODO: Make sure daemon is running.
        self.api = ipfsapi.connect("127.0.0.1", IPFS_API_PORT)

    def send_search_query(self, query):
        """Send search query to peers in swarms over UDP."""
        peers = self.api.swarm_peers()["Peers"]
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        for peer in peers:
            ip = peer["Addr"].split("/")[2]
            try:
                client.sendto(query.encode(), (ip, UDP_PORT_NO))
            except:
                try:
                    client_v6.sendto(query.encode(), (ip, UDP_PORT_NO_V6))
                except:
                    # TODO: Log, not print
                    print(ip)

    def search_filelist(self, query_str):
        own_filelist = IpfsUtils.get_filelist()
        print(own_filelist)
        results = []
        for token in query_str.split():
            results += self.__recursive_search(own_filelist, "/", token)
        return results

    @staticmethod
    def __recursive_search(cur_dir, parent_str, query_str):
        results = []
        for file in cur_dir["files"]:
            if __match(query_str, parent_str + file["name"]):
                results.append(file)

        for _dir in cur_dir["directories"]:
            results += self.__recursive_search(
                _dir, f"{parent_str}{_dir['name']}/", query_str
            )

        return results

    @staticmethod
    def __match(pattern, text):
        return pattern in text
