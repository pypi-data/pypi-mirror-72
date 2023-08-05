# -*- coding: utf-8 -*-
#
#   UDP: User Datagram Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import socket
import threading
import time
import weakref
from typing import Optional

from .connection import ConnectionStatus, ConnectionDelegate, Connection


class DatagramPacket:

    def __init__(self, data: bytes, address: tuple):
        super().__init__()
        self.__data = data
        self.__address = address

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def offset(self) -> int:
        return 0

    @property
    def length(self) -> int:
        return len(self.__data)

    @property
    def address(self) -> tuple:
        return self.__address

    @property
    def ip(self) -> str:
        return self.__address[0]

    @property
    def port(self) -> int:
        return self.__address[1]


class Socket(threading.Thread):
    """
        Max count for caching packages
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Each UDP data package is limited to no more than 576 bytes, so set the
        MAX_CACHE_SPACES to about 2,000,000 means it would take up to 1GB memory
        for the caching.
    """
    MAX_CACHE_SPACES = 1024 * 1024 * 2

    """
        Buffer size for receiving package
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    BUFFER_SIZE = 2048

    def __init__(self, port: int, host: str ='0.0.0.0'):
        super().__init__()
        self.__local_address = (host, port)
        # create socket
        self.__socket = self._create_socket()
        # delegate
        self.__delegate: weakref.ReferenceType = None
        # connection list
        self.__connections = []
        self.__connections_lock = threading.Lock()
        # received packages
        self.__cargoes = []
        self.__cargoes_lock = threading.Lock()

    @property
    def local_address(self) -> tuple:
        return self.__local_address

    @property
    def running(self) -> bool:
        return not getattr(self.__socket, '_closed', False)

    def _create_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(2)
        sock.bind(self.local_address)
        return sock

    def settimeout(self, timeout: Optional[float]):
        self.__socket.settimeout(timeout)

    @property
    def delegate(self) -> Optional[ConnectionDelegate]:
        if self.__delegate is not None:
            return self.__delegate()

    @delegate.setter
    def delegate(self, value: Optional[ConnectionDelegate]):
        self.__delegate = weakref.ref(value)

    #
    #  Connections
    #

    def get_connection(self, remote_address: tuple) -> Optional[Connection]:
        with self.__connections_lock:
            for conn in self.__connections:
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.remote_address == remote_address:
                    # got it
                    return conn

    # noinspection PyMethodMayBeStatic
    def _create_connection(self, remote_address: tuple, local_address: tuple=None) -> Connection:
        return Connection(local_address=local_address, remote_address=remote_address)

    def connect(self, remote_address: tuple) -> Connection:
        """ add remote address to keep connected with heartbeat """
        with self.__connections_lock:
            for conn in self.__connections:
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.remote_address == remote_address:
                    # already connected
                    return conn
            conn = self._create_connection(remote_address=remote_address, local_address=self.local_address)
            self.__connections.append(conn)
            return conn

    def disconnect(self, remote_address: tuple) -> bool:
        """ remove remote address from heartbeat tasks """
        count = 0
        with self.__connections_lock:
            pos = len(self.__connections)
            while pos > 0:
                pos -= 1
                conn = self.__connections[pos]
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.remote_address == remote_address:
                    # got one
                    self.__connections.pop(pos)
                    count += 1
                    # break
        return count > 0

    def __connection_by_status(self, status: ConnectionStatus) -> Optional[Connection]:
        """ get connection by status """
        with self.__connections_lock:
            for conn in self.__connections:
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.status == status:
                    return conn

    def __expired_connection(self) -> Optional[Connection]:
        """ get any expired connection """
        return self.__connection_by_status(ConnectionStatus.Default)

    def __error_connection(self) -> Optional[Connection]:
        """ get any error connection """
        return self.__connection_by_status(ConnectionStatus.Error)

    def __update_sent_time(self, remote_address: tuple):
        connection = None
        old_status = None
        new_status = None
        with self.__connections_lock:
            for conn in self.__connections:
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.remote_address == remote_address:
                    # refresh time
                    old_status, new_status = conn.update_sent_time()
                    connection = conn
        # callback
        if old_status != new_status and self.delegate is not None:
            # assert connection is not None, 'connection error: %s' % remote_address
            self.delegate.connection_status_changed(connection=connection,
                                                    old_status=old_status,
                                                    new_status=new_status)

    def __update_received_time(self, remote_address: tuple):
        connection = None
        old_status = None
        new_status = None
        with self.__connections_lock:
            for conn in self.__connections:
                assert isinstance(conn, Connection), 'connection error: %s' % conn
                if conn.remote_address == remote_address:
                    # refresh time
                    old_status, new_status = conn.update_received_time()
                    connection = conn
        # callback
        if old_status != new_status and self.delegate is not None:
            self.delegate.connection_status_changed(connection=connection,
                                                    old_status=old_status,
                                                    new_status=new_status)

    def send(self, data: bytes, remote_address: tuple) -> int:
        """
        Send data to remote address

        :param data:
        :param remote_address:
        :return: how many bytes have been sent
        """
        try:
            res = self.__socket.sendto(data, remote_address)
            assert res == len(data), 'send failed: %d, %d' % (res, len(data))
            self.__update_sent_time(remote_address=remote_address)
            return res
        except socket.error as error:
            print('Failed to send data: %s' % error)
            return -1

    def __receive(self, buffer_size: int = 2048) -> Optional[DatagramPacket]:
        try:
            data, address = self.__socket.recvfrom(buffer_size)
            if data is not None:
                assert len(address) == 2, 'remote address error: %s, data length: %d' % (address, len(data))
                self.__update_received_time(remote_address=address)
                return DatagramPacket(data=data, address=address)
        except socket.error as error:
            if not isinstance(error, socket.timeout):
                print('Failed to receive data: %s' % error)

    def receive(self) -> Optional[DatagramPacket]:
        """
        Get received data package from buffer, non-blocked

        :return: received data and source address
        """
        with self.__cargoes_lock:
            if len(self.__cargoes) > 0:
                return self.__cargoes.pop(0)

    def __cache(self, packet: DatagramPacket):
        with self.__cargoes_lock:
            if len(self.__cargoes) >= self.MAX_CACHE_SPACES:
                # drop the first package
                self.__cargoes.pop(0)
            # append the new package to the end
            self.__cargoes.append(packet)
        # callback
        if self.delegate is not None:
            connection = self.get_connection(remote_address=packet.address)
            if connection is not None:
                self.delegate.connection_received_data(connection=connection)

    def run(self):
        while self.running:
            try:
                packet = self.__receive(buffer_size=self.BUFFER_SIZE)
                if packet is None:
                    # receive nothing
                    time.sleep(0.1)
                    continue
                if packet.length == 4:
                    # check heartbeat
                    data = packet.data
                    if data == b'PING':
                        # respond heartbeat
                        self.send(data=b'PONG', remote_address=packet.address)
                        continue
                    elif data == b'PONG':
                        # ignore it
                        continue
                # cache the data received
                self.__cache(packet=packet)
            except Exception as error:
                print('Socket.run error: %s' % error)

    def ping(self):
        """ send heartbeat to all expired connections """
        while True:
            conn = self.__expired_connection()
            if conn is None:
                # no more expired connection
                break
            self.send(data=b'PING', remote_address=conn.remote_address)

    def purge(self):
        """ remove error connections """
        while True:
            conn = self.__error_connection()
            if conn is None:
                # no more error connection
                break
            # remove error connection (long time to receive nothing)
            self.disconnect(remote_address=conn.remote_address)

    def close(self):
        self.__socket.close()

    def stop(self):
        self.close()
