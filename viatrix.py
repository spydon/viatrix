import serial
import am03127 as am


class Device:
    def __init__(self, dev, m_id):
        self.dev = dev
        self.m_id = m_id
        self.tty = serial.Serial(dev, 9600)

    def close(self):
        self.tty.close()

    @staticmethod
    def get_data():
        dev = input('Device, or press enter for default (/dev/ttyUSB0): ')
        m_id = input('ID, or press enter for default (1): ')

        if dev == '':
            dev = '/dev/ttyUSB0'
        if m_id == '':
            m_id = 1
        else:
            m_id = int(m_id)

        return dev, m_id

    @classmethod
    def create(cls):
        dev, m_id = cls.get_data()
        return cls(dev, m_id)


def help():
    print('Type commands like:')
    print('help\t\t\t\t\t\t\tDisplays this message')
    print('msg <Page=A> <Lead=E> <Disp=A> <Wait=5> <Lag=E> <Msg>\tDisplays '
          'message with given args')
    print('scd <Order=A>\t\t\t\t\t\t\t\t\tSets page schedule')
    print('exit\t\t\t\t\t\t\tExits')
    print()


def message(device, args):
    msg_args = args.split(' ', maxsplit=5)

    page = msg_args[0]
    lead = msg_args[1]
    disp = msg_args[2]
    wait = int(msg_args[3])
    lag = msg_args[4]
    msg = msg_args[5]

    data = am.send_page_msg(1, page, lead, disp, wait, lag, msg)
    am.sync_transceive(device.tty, device.m_id, data)


def schedule(device, args):
    order = args
    if not order:
        order = 'A'

    data = am.send_schedule(order)
    am.sync_transceive(device.tty, device.m_id, data)


def cli():
    device = Device.create()

    print()

    help()

    while True:
        try:
            line = input('> ').split(' ', maxsplit=1)
        except EOFError:
            print('exit')
            line = ['exit']

        cmd = line[0]
        try:
            args = line[1]
        except IndexError:
            args = None

        if cmd == 'help':
            help()
        elif cmd == 'msg':
            message(device, args)
        elif cmd == 'scd':
            schedule(device, args)
        elif cmd == 'exit':
            break

    device.close()


if __name__ == '__main__':
    cli()
