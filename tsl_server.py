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
listen_addr = '127.0.0.1'
# Port of the server
listen_port = 8082
# The Server certificate
server_cert = 'server.crt'
# The Server RSA key
server_key = 'server.key'
# The client certificate
client_certs = 'client.crt'

# Load a context to do an auth with the client certificate
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# To accept a connection you will need an certificate
context.verify_mode = ssl.CERT_REQUIRED
# Load the server certificate
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
# Load all the clients certificate the can connect to the app
context.load_verify_locations(cafile=client_certs)

bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(5)

while True:
    PYTHON_LOGGER.info("Waiting for client")
    newsocket, fromaddr = bindsocket.accept()
    PYTHON_LOGGER.info("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
    conn = context.wrap_socket(newsocket, server_side=True)
    PYTHON_LOGGER.info("SSL established. Peer: {}".format(conn.getpeercert()))
    buf = b''  # Buffer to hold received client data
    try:
        while True:
            data = conn.recv(4096)
            if data:
                # Client sent us data. Append to buffer
                buf += data
            else:
                # No more data from client. Show buffer and close connection.
                PYTHON_LOGGER.info("Received from client: {}".format(buf))
                break
    finally:
        PYTHON_LOGGER.info("Closing connection")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
