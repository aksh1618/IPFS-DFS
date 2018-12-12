import atexit
import collections
import json
import socket
import traceback
import threading

from util import filelist_utils

TCP_PORT_NO = 43460
TCP_PORT_NO_V6 = 43461
UDP_PORT_NO = 43462
UDP_PORT_NO_V6 = 43463

SOCKET_TIMEOUT = 5


class SearchManager:
    """Methods for managing search operations."""

    def __init__(self, api):
        # TODO: Make sure daemon is running.
        self.api = api

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
                    traceback.print_exc()
                    print(ip)

    def get_search_results(self, query):
        # TODO: Listen for response and return results.
        results = []

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", TCP_PORT_NO))
        s.settimeout(SOCKET_TIMEOUT)

        s.listen(5)
        threading.Thread(self.send_search_query,(query,)).start()
        while True:
            try:
                # TODO: Use context manager.
                c, addr = s.accept()
                try:
                    c.settimeout(SOCKET_TIMEOUT)
                    print("Got connection from", addr)
                    result_string = c.recv(1024)
                    result_string = result_string.decode()
                    result = json.loads(result_string)
                    print(result)
                    results.append(result)
                except:
                    pass
                c.close()
            except:
                traceback.print_exc()
                break
        s.close()

        return results
