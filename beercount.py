import viatrix
import tkinter as tk


beers = 0
casks = 0


def display_beers(device, beers):
    viatrix.message(device, 'A E A 1 E Bier: <AB>%d' % (beers))


def display_casks(device, casks):
    viatrix.message(device, 'B E A 1 E Fusten: <AB>%d' % (casks))


def count():
    global beers, casks

    #device = viatrix.Device.create()

    beers = int(input('Enter beers already sold: '))
    casks = int(input('Enter casks already emptied: '))

    def onKeyPress(event):
        global beers, casks

        try:
            char = ord(event.char)
        except TypeError:
            return

        if char == 32:
            beers += 1
            text.delete('1.0', '2.0')
            text.insert('0.0', 'Beers: %d\n' % (beers))
            #display_beers(device, beers)

        elif char == 13:
            casks += 1
            text.delete('2.0', '3.0')
            text.insert('2.0', 'Casks: %d\n' % (casks))
            #display_casks(device, casks)

    root = tk.Tk()

    root.attributes('-fullscreen', True)
    text = tk.Text(root, font=('Comic Sans MS', 12))
    text.pack()

    text.insert('1.0', 'Beers: %d\n' % (beers))
    text.insert('2.0', 'Casks: %d\n' % (casks))

    #display_beers(device, beers)
    #display_casks(device, casks)

    root.bind('<KeyPress>', onKeyPress)
    root.mainloop()

    #device.close()


if __name__ == '__main__':
    count()
