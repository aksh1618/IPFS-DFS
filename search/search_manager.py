import atexit
import collections
import ipfsapi
import socket

IPFS_PORT_NO = 5001
UDP_PORT_NO = 43462
UDP_PORT_NO_V6 = 43463


class SearchManager:
    """Methods for managing search operations."""

    def __init__(self, IPFS_API_PORT=IPFS_PORT_NO):
        # TODO: Make sure daemon is running.
        self.api = ipfsapi.connect('127.0.0.1', IPFS_API_PORT)

    def send_search_query(self, query):
        """Send search query to peers in swarms over UDP."""
        peers = self.api.swarm_peers()['Peers']
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        for peer in peers:
            ip = peer['Addr'].split('/')[2]
            try:
                client.sendto(query.encode(), (ip, UDP_PORT_NO))
            except:
                try:
                    client_v6.sendto(query.encode(), (ip, UDP_PORT_NO_V6))
                except:
                    # TODO: Log, not print
                    print(ip)
