#!/usr/bin/env python3

import errno
import re
import sys
import socket
import selectors

debug = True
WSAEWOULDBLOCK = 10035

if debug:
    import pdb;

class Connection:
    HEADER = re.compile(rb'\nPyON\s+(\d+)\s+(.*)\n')
    FOOTER = re.compile(rb'\n---\n')

    MESSAGE_CONVERTERS = {
        'heartbeat': int,
        'num-slots': int,
    }


    def __init__(self, host = 'localhost', port = 36330, retry_rate = 5):
        self.host = host
        self.port = port
        self.retry_rate = retry_rate

        self.selector = selectors.DefaultSelector()
        self.socket = None
        self.connected = False
        self.fail_reason = None


    def is_connected(self):
        if self.socket is None: return False
        if self.connected: return True

        rlist, wlist, xlist = select.select([], [self.socket], [self.socket], 0)

        if len(wlist) != 0: self.connected = True
        elif len(xlist) != 0:
            self.fail_reason = 'refused'
            self.close()

        return self.connected


    def connection_error(self, err):
        print('Connection error: %d: %s' % (err.errno, err.args))
        self.close()
        if err == errno.ECONNREFUSED: self.fail_reason = 'refused'
        elif err in [errno.ETIMEDOUT, errno.ENETDOWN, errno.ENETUNREACH]:
            self.fail_reason = 'connect'
        else: self.fail_reason = 'error'


    def connection_lost(self):
        print('Connection lost')
        self._close()
        self.fail_reason = 'closed'
        raise Exception('Lost connection')


    def open(self):
        if debug: print('Opening connection to', self.host, ':', self.port)
        server_addr = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        err = self.socket.connect_ex(server_addr)

        if err != 0 and not err in [
            errno.EINPROGRESS, errno.EWOULDBLOCK, WSAEWOULDBLOCK]:
            self.fail_reason = 'connect'
            raise Exception('Connection failed: ' + errno.errorcode[err])

        self.connected = True


    def close(self):
        if self.socket is not None:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except: pass
            try:
                self.socket.close()
            except: pass
            self.socket = None

        self.connected = False


    def read_data(self):
        if not self.is_connected(): self.open()

        data = b'';
        self.selector.register(self.socket, selectors.EVENT_READ)
        try:
            while not data.endswith(b'\n> '):
                events = self.selector.select(timeout=3)
                if events:
                    for key, mask in events:
                        if mask & selectors.EVENT_READ:
                            recv_data = self.socket.recv(1024)
                            if recv_data:
                                if debug: print('Got', len(recv_data), 'bytes')
                                data += recv_data

                if not self.selector.get_map():
                    self.fail_reason = 'timeout'
                    self.close()
                    raise Exception('Timed out when reading')

        except OSError as err:
            # Error codes for nothing to read
            if err.errno not in [errno.EAGAIN, errno.EWOULDBLOCK, WSAEWOULDBLOCK]:
                if data: return data
                self.connection_error(err)
                raise

        finally:
            self.selector.unregister(self.socket)

        return data


    def write_data(self, bytes):
        if not self.is_connected(): self.open()

        data = bytes
        bytes_written = 0
        self.selector.register(self.socket, selectors.EVENT_WRITE)
        try:
            while len(data) > 0:
                events = self.selector.select(timeout=3)
                if events:
                    for key, mask in events:
                        if mask & selectors.EVENT_WRITE:
                            sent = self.socket.send(data)
                            if debug: print('Sent', sent, 'bytes')
                            data = data[sent:]

                if not self.selector.get_map():
                    break

        except socket.error as err:
            # Error codes for write buffer full
            if err.errno not in [errno.EAGAIN, errno.EWOULDBLOCK, WSAEWOULDBLOCK]:
                if bytes_written: return bytes_written
                self.connection_error(err)
                raise

        finally:
            self.selector.unregister(self.socket)

        return bytes_written


    def parse_pyon(self, bytes):
        header_match = re.search(Connection.HEADER, bytes)
        footer_match = re.search(Connection.FOOTER, bytes)
        if header_match and footer_match:
            api_version = int(header_match[1])
            message_type = header_match[2].decode()
            message = bytes[header_match.span()[1]:footer_match.span()[0]]
            if debug: print('Message version', api_version, 'type', message_type)
            obj = eval(message, {'__builtins__': None}, {})
            return self.convert(obj, message_type)


    def convert(self, obj, message_type):
        converter = self.MESSAGE_CONVERTERS.get(message_type, None)
        if converter is None:
            # raise Exception('No converter found for message %s' % (message_type))
            return obj

        return converter(obj)


if __name__ == '__main__':
    conn = Connection()
    text = conn.read_data()
    conn.write_data(b'auth putzfuck\n')
    text = conn.read_data()
    conn.write_data(b'slot-info\n')
    text = conn.read_data()
    slots = conn.parse_pyon(text)
    print(slots)
    conn.close()

