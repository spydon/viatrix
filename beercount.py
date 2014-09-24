import viatrix
import tkinter as tk


beers = 0


def display_beers(device, beers):
    viatrix.message(device, 'A E A 1 E Bier: <AB>%d' % (beers))


def display_crates(device, crates):
    viatrix.message(device, 'B E A 1 E Krat: <AB>%d' % (crates))


def count():
    global beers, crates

    device = viatrix.Device.create()

    try:
        beers = int(input('Enter beers already sold (default 0): '))
    except ValueError:
        beers = 0

    try:
        refresh = int(input('Enter refresh time (default: 5000): '))
    except ValueError:
        refresh = 5000

    def onKeyPress(event):
        global beers

        if event.char in [' ', '-']:
            if event.char == ' ':
                beers += 1
            elif event.char == '-':
                beers -= 1

            text.delete('1.0', '2.0')
            text.insert('1.0', 'Beers: %d\n' % (beers))

            crates = beers / 24
            text.delete('2.0', '3.0')
            text.insert('2.0', 'Crates: %d\n' % (crates))

    def update():
        display_beers(device, beers)

        crates = beers / 24
        display_crates(device, crates)

        root.after(refresh, update)

    root = tk.Tk()

    root.attributes('-fullscreen', True)
    text = tk.Text(root, font=('Comic Sans MS', 12))
    text.pack()

    crates = beers / 24

    text.insert('1.0', 'Beers: %d\n' % (beers))
    text.insert('2.0', 'Crates: %d\n' % (crates))

    display_beers(device, beers)
    display_crates(device, crates)

    root.bind('<KeyPress>', onKeyPress)
    root.after(refresh, update)

    root.mainloop()

    device.close()


if __name__ == '__main__':
    count()
