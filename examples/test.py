#!/usr/bin/env python

import time

import phatbeat


@phatbeat.on(phatbeat.BTN_ONOFF)
def fast_forward(pin):
    print("FF pressed!")

try:
    while True:
        phatbeat.set_all(0,255,0,channel=0)
        phatbeat.set_all(255,0,0,channel=1)
        phatbeat.show()
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
