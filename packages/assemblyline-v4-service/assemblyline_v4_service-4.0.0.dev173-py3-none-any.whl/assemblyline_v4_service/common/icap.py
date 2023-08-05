import os
import socket
from io import StringIO

from assemblyline.common.str_utils import safe_str

ICAP_OK = b'ICAP/1.0 200 OK'


# noinspection PyBroadException
class IcapClient(object):
    """
    A limited Internet Content Adaptation Protocol client.

    Currently only supports RESPMOD as that is all that is required to interop
    with most ICAP based AV servers.
    """

    RESP_CHUNK_SIZE = 65565
    MAX_RETRY = 3

    def __init__(self, host, port, respmod_service="av/respmod", action=""):
        self.host = host
        self.port = port
        self.service = respmod_service
        self.action = action

    def scan_data(self, data, name=None):
        return self._do_respmod(name or 'filetoscan', data)

    def scan_local_file(self, filepath):
        filename = os.path.basename(filepath)
        with open(filepath, 'r') as f:
            data = f.read()
            return self.scan_data(data, filename)

    def options_respmod(self):
        request = f"OPTIONS icap://{self.host}/{self.service} ICAP/1.0\r\n\r\n"

        for i in range(self.MAX_RETRY):
            s = None
            try:
                s = socket.create_connection((self.host, self.port), timeout=10)
                s.sendall(bytes(request))
                response = temp_resp = s.recv(self.RESP_CHUNK_SIZE)
                while len(temp_resp) == self.RESP_CHUNK_SIZE:
                    temp_resp = s.recv(self.RESP_CHUNK_SIZE)
                    response += temp_resp
                if not response or not response.startswith(ICAP_OK):
                    raise Exception(f"Unexpected OPTIONS response: {response}")
                return response
            except Exception:
                if i == (self.MAX_RETRY-1):
                    raise
            finally:
                if s is not None:
                    try:
                        # try to close the connection anyways
                        s.close()
                    except Exception:
                        pass

        raise Exception("Icap server refused to respond.")

    @staticmethod
    def chunk_encode(data):
        chunk_size = 8160
        out = ""
        offset = 0
        while len(data) < offset * chunk_size:
            out += "1FEO\r\n"
            out += data[offset * chunk_size:(offset + 1) * chunk_size]
            out += "\r\n"
            offset += 1

        out += "%X\r\n" % len(data[offset * chunk_size:])
        out += data[offset * chunk_size:]
        out += "\r\n0\r\n\r\n"

        return out

    def _do_respmod(self, filename, data):
        encoded = self.chunk_encode(data)

        # ICAP RESPMOD req-hdr is the start of the original HTTP request.
        respmod_req_hdr = "GET /{FILENAME} HTTP/1.1\r\n\r\n".format(FILENAME=safe_str(filename))

        # ICAP RESPMOD res-hdr is the start of the HTTP response for above request.
        respmod_res_hdr = (
            "HTTP/1.1 200 OK\r\n"
            "Transfer-Encoding: chunked\r\n\r\n")

        res_hdr_offset = len(respmod_req_hdr)
        res_bdy_offset = len(respmod_res_hdr) + res_hdr_offset

        # The ICAP RESPMOD header. Note:
        # res-hdr offset should match the start of the GET request above.
        # res-body offset should match the start of the response above.

        respmod_icap_hdr = (
            f"RESPMOD icap://{self.host}:{self.port}/{self.service}{self.action} ICAP/1.0\r\n"
            f"Host:{self.host}:{self.port}\r\n"
            "Allow:204\r\n"
            f"Encapsulated: req-hdr=0, res-hdr={res_hdr_offset}, res-body={res_bdy_offset}\r\n\r\n"
        )

        sio = StringIO()
        sio.write(respmod_icap_hdr)
        sio.write(respmod_req_hdr)
        sio.write(respmod_res_hdr)
        sio.write(encoded)
        serialized_request = sio.getvalue()

        for i in range(self.MAX_RETRY):
            s = None
            try:
                s = socket.create_connection((self.host, self.port), timeout=10)
                s.sendall(bytes(serialized_request))
                response = temp_resp = s.recv(self.RESP_CHUNK_SIZE)
                while len(temp_resp) == self.RESP_CHUNK_SIZE:
                    temp_resp = s.recv(self.RESP_CHUNK_SIZE)
                    response += temp_resp

                return response
            except Exception:
                if i == (self.MAX_RETRY-1):
                    raise
            finally:
                if s is not None:
                    try:
                        # try to close the connection anyways
                        s.close()
                    except Exception:
                        pass

        raise Exception("Icap server refused to respond.")
