import atexit
import collections
import socket
import threading
import time

UDP_PORT_NO = 43462
UDP_PORT_NO_V6 = 43463
SOCKET_TIMEOUT = 1


class SearchListener:
    """Server which listens for search queries."""

    def __init__(self, api):
        # TODO: Make sure daemon is running.
        self.terminated = False
        self.api = api
        self.previous_queries = collections.deque(maxlen=20)
        # TODO: Should this be in init_servers_and_listen ?
        atexit.register(self.__cleanup)

    def init_servers_and_listen(self):
        """Initialize ipv4 and ipv6 servers and start listening."""

        self.server_socket_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.server_socket_v6.bind(("::", UDP_PORT_NO_V6))
        self.server_socket_v6.settimeout(SOCKET_TIMEOUT)
        self.server_socket_v4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket_v4.bind(("0.0.0.0", UDP_PORT_NO))
        self.server_socket_v4.settimeout(SOCKET_TIMEOUT)
        self.server_thread_v4 = threading.Thread(
            target=self.__listen_for_query, args=(self.server_socket_v4,)
        )
        self.server_thread_v6 = threading.Thread(
            target=self.__listen_for_query, args=(self.server_socket_v6,)
        )
        self.server_thread_v4.start()
        self.server_thread_v6.start()

    def close(self):
        """Terminate search listener. To be called on app exit."""
        self.terminated = True

    def __listen_for_query(self, server_socket):
        while not self.terminated:
            try:
                data, addr = server_socket.recvfrom(1024)
                print(f"Message: {data}, from: {addr}")
                if addr not in self.previous_queries:
                    # TODO: handle this request
                    # TODO: Check if needed
                    self.previous_queries.append(addr)
                else:
                    # This request has already been served. Ignore it.
                    pass
            except:
                # print('trying')
                continue

    def __cleanup(self):
        self.server_socket_v4.close()
        self.server_socket_v6.close()
        # TODO : Check if needed
        # self.server_thread_v4.join()
        # self.server_thread_v6.join()
