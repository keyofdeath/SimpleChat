#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import socket
import ssl

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/tsl_server.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

# Address of the server
host_addr = '127.0.0.1'
# Port of the server
host_port = 8082
# Host name of the server
server_sni_hostname = 'example.com'
# The Server certificate
server_cert = 'server.crt'
# The client certificate
client_cert = 'client.crt'
# The RSA key of the client
client_key = 'client.key'

# Load a context to do an auth with the server certificate
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
# Load the client certification
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
# Disp the server certificate
PYTHON_LOGGER.info("SSL established. Peer: {}".format(conn.getpeercert()))
PYTHON_LOGGER.info("Sending: 'Hello, world!")
conn.send(b"Hello, world!")
PYTHON_LOGGER.info("Closing connection")
conn.close()
