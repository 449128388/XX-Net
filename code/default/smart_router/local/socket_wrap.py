import time


class SocketWrap(object):

    def __init__(self, sock, ip=None, port=None, host="", target=""):
        self._sock = sock
        self.ip = ip
        self.port = port
        self.host = host
        self.target = target
        self.recved_data = 0
        self.recved_times = 0
        self.create_time = time.time()
        self.closed = False
        self.replace_pattern = None

    def __getattr__(self, attr):
        return getattr(self._sock, attr)

    def close(self):
        self._sock.close()
        self.closed = True

    def is_closed(self):
        return self.closed

    def __str__(self):
        return "%s[%s]:%d" % (self.host, self.ip, self.port)

    def recv(self, bufsiz, flags=0):
        d = self._sock.recv(bufsiz, flags)
        if self.replace_pattern and " HTTP/1.1\r\n" in d:
            line_end = d.find("\r\n")
            req_line = d[:line_end]

            words = req_line.split()
            if len(words) == 3:
                method, url, http_version = words
                url = url.replace(self.replace_pattern[0], self.replace_pattern[1])

                d = "%s %s %s" % (method, url, http_version) + d[line_end:]

        return d
