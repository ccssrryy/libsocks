import socket

import struct

from libsocks.core import constants

from libsocks.core.impl import HandshakeDoneState


def check_request(test_case, context, req_data):
    test_case.assertIsInstance(context.state, HandshakeDoneState)
    test_case.assertEqual(req_data[1][0], context.ver)
    test_case.assertEqual(req_data[1][1], context.cmd)
    test_case.assertEqual(req_data[1][2], constants.RSV)
    test_case.assertEqual(req_data[1][3], context.atyp)
    test_case.assertEqual(context.dst_addr, socket.inet_ntop(socket.AF_INET, req_data[1][4: -2]))
    test_case.assertEqual(context.dst_port, struct.unpack(">H", req_data[1][-2:])[0])
