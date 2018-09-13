import viatrix

def setup():
    device = viatrix.Device.create()

    viatrix.message(device, 'A E A 25 K     1/D/27 ')
    viatrix.message(device, 'B K A 25 K     1/D/27 ')
    viatrix.message(device, 'C K A 25 K     1/D/27 ')
    viatrix.message(device, 'D K A 25 E     1/D/27 ')
    viatrix.message(device, 'E E A 2 E Se upp f<U76>r d<U76>rrarna')
    viatrix.message(device, 'F J A 2 J <AC>D<U76>rrarna st<U64>ngs')
    viatrix.message(device, 'G L A 1 D <AC>CARP var h<U64>r <3')

    s = 'ABCDEF'
    carp = 'G'
    viatrix.schedule(device, s*6 + carp)
    device.close()


if __name__ == '__main__':
    setup()
