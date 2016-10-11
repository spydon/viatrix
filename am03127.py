# -*- encoding: utf-8 -*-
# implementation of the serial protocol used by
# AM03127 LED signs. Based on the document
# AM004 - 03128/03127 LED Display Board Communication
# Version 2.2, Date Aug. 13, 2005

# My LED board is a "Mc Crypt 590996 / 590998"
# LED Light Writing Board


def ascii_range(c, first, last):
    if type(c) != str or len(c) != 1:
        return False
    if ord(c) < ord(first) or ord(c) > ord(last):
        return False
    return True

special_map = {
    u'\n': ' ',
    u'\r': '',
}


def send_page_msg(line=1, page='A', lead=None, disp='A', wait=5, lag=None,
                  msg=''):
    default_lead_lag = 'E'

    if not lead:
        lead = default_lead_lag
    if not lag:
        lag = default_lead_lag

    if line < 1 or line > 8:
        raise RuntimeError('Line not in range 1..8')
    if not ascii_range(page, 'A', 'Z'):
        raise RuntimeError('Page not in range A..Z')
    if not ascii_range(lead, 'A', 'S'):
        raise RuntimeError('Lead not in range A..S')
    if not (disp in 'ABCDEQRSTUabcdeqrstu'):
        raise RuntimeError('Display not one of {ABCDEQRSTUabcdeqrstu}')
    if wait < 0 or wait > 25:
        raise RuntimeError('Waittime not in range 0..25sec (0=0.5 sec)')
    if not ascii_range(lag, 'A', 'S'):
        raise RuntimeError('Lag not in range A..S')
    return '<L%d><P%c><F%c><M%c><W%c><F%c>' % (line, page, lead, disp,
                                               chr(wait + 65), lag) + msg


def send_schedule(order='A'):
    return '<TA>00010100009912312359%s' % (order)


def encode_msg(board_id, data):
    if board_id < 0 or board_id > 255:
        raise RuntimeError('Board ID not in range 0..255')
    chksum = 0
    for c in data:
        chksum ^= ord(c)
    return ('<ID%02X>' % (board_id) + data + '%02X<E>' % (chksum)).encode()


def sync_transceive(port, board_id, data):
    port.timeout = 1
    port.write(encode_msg(board_id, data))

    replies = ['ACK', 'NACK']
    buf = ''

    while True:
        c = port.read(1).decode('utf-8')
        if c == '':
            return 'TIMEOUT'
        buf = buf + c

        valid_start = False
        for r in replies:
            if len(buf) > len(r):
                continue
            if buf == r[0:len(buf)]:
                valid_start = True
                if len(buf) == len(r):
                    return buf
        if not valid_start:
            return buf  # invalid


def sync_set_sign_id(port, board_id):
    port.setTimeout(1)
    port.write('<ID><%02X><E>' % (board_id))

    buf = port.read(2)

    if len(buf) < 2:
        raise RuntimeError('Timeout reading from port.')

    if buf == '%02X' % (board_id):
        return True
    return False
