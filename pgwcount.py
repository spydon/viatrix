import viatrix
import time
from datetime import datetime
import random
from math import ceil

def display_pgw_amount(device, amount):
    viatrix.message(device, 'B E A 5 E %d SEK' % (amount))


def count():
    device = viatrix.Device.create()
    viatrix.message(device, 'A E A 5 E Recv. today:')
    viatrix.message(device, 'C A A 2 A  ')

    data = [0, 16, 60, 127, 283, 394,
            519, 612, 777, 815, 926,
            1027, 1122, 1232, 1416, 1529, 1622,
            1899, 2312, 2456, 2698, 2967, 4012]

    try:
        refresh = int(input('Enter refresh time (default: 20): '))
    except ValueError:
        refresh = 20

    viatrix.schedule(device, 'CAB')
    amount = 0
    while(True):
        now = datetime.now()
        hour = now.hour
        next_hour = (hour+1)%len(data)
        minute = now.minute
        second = now.second
        max_amount = data[next_hour]
        max_step = ((max_amount-data[hour])/(3600/refresh))*2

        if(amount+max_step > max_amount):
            max_step = max_amount-amount

        if(minute == 0 and second <= refresh):
            amount = data[hour]
        else:
            amount += random.randint(0, int(max_step))

        display_pgw_amount(device, amount)
        time.sleep(refresh)
        print(amount)

    device.close()


if __name__ == '__main__':
    count()
