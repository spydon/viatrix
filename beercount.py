import viatrix
import tkinter as tk


beers = 0
crates = 0


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
        crates = int(input('Enter crates already emptied (default 0): '))
    except ValueError:
        crates = 0

    def onKeyPress(event):
        global beers, crates

        if event.char in [' ', '-']:
            if event.char == ' ':
                beers += 1
            elif event.char == '-':
                beers -= 1
            text.delete('1.0', '2.0')
            text.insert('0.0', 'Beers: %d\n' % (beers))
            display_beers(device, beers)

            new_crates = beers / 24
            if new_crates != crates:
                crates = new_crates
                text.delete('2.0', '3.0')
                text.insert('2.0', 'Crates: %d\n' % (crates))
                display_crates(device, crates)

    root = tk.Tk()

    root.attributes('-fullscreen', True)
    text = tk.Text(root, font=('Comic Sans MS', 12))
    text.pack()

    text.insert('1.0', 'Beers: %d\n' % (beers))
    text.insert('2.0', 'Crates: %d\n' % (crates))

    display_beers(device, beers)
    display_crates(device, crates)

    root.bind('<KeyPress>', onKeyPress)
    root.mainloop()

    device.close()


if __name__ == '__main__':
    count()
