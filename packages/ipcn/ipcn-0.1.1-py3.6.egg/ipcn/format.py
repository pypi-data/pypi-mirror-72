#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import struct


def ip2long(ip_str):
    ip = socket.ntohl(struct.unpack('I', socket.inet_aton(ip_str))[0])
    return ip


def long2ip(ip_long):
    ip = socket.inet_ntoa(struct.pack('I', socket.htonl(ip_long)))
    return ip
