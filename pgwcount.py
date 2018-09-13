import viatrix
import time
from datetime import datetime
import random
from math import ceil
import string
import locale

def display_pgw_amount(device, page, amount):
    format_amount = '{:,}'.format(amount).replace(',', '.')
    viatrix.message(device, '%s A A 1 K %skr' % (page, format_amount))


def count():
    device = viatrix.Device.create()
    buffer = list(string.ascii_uppercase)[2:]
    refresh = 38.25

    viatrix.clear_all(device)
    time.sleep(1)

    viatrix.message(device, 'A E A 1 A  ')
    viatrix.message(device, 'B E A 2 E Recv. today:')

    data = [1086864, 1616272, 1999652, 2275432, 2522875, 2853205,
            3477041, 4682007, 6858673, 10048661, 13789367, 17544148,
            20730371, 23947612, 27063455, 29984401, 32888173, 35855263,
            39095658, 42512301, 46663195, 51570386, 55430182, 56000222]

    is_first = True
    start_hour = datetime.now().hour
    start_minute = datetime.now().minute+0.001
    amount = int(data[start_hour]+((data[start_hour+1]-data[start_hour])/(60/start_minute)))
    while(True):
        now = datetime.now()
        hour = now.hour
        next_hour = (hour+1)%len(data)
        minute = now.minute
        second = now.second
        max_amount = data[next_hour]
        max_step = ((max_amount-data[hour])/(3600/1))*2

        for page in buffer:
            if(amount+max_step > max_amount):
                max_step = max_amount-amount

            if(minute == 0 and second <= refresh):
                amount = data[hour]
            else:
                amount += random.randint(0, int(max_step))

            display_pgw_amount(device, page, amount)

        viatrix.schedule(device, string.ascii_uppercase)
        if(is_first):
            time.sleep(3)
            is_first = False
        time.sleep(refresh)

    device.close()


if __name__ == '__main__':
    count()
