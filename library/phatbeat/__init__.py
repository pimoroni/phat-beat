import atexit
import time
from sys import exit

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")


__version__ = '0.0.1'

DAT = 23
CLK = 24
NUM_PIXELS = 16
CHANNEL_PIXELS = 8
BRIGHTNESS = 7

BTN_FASTFWD = 5
BTN_REWIND = 13
BTN_PLAYPAUSE = 6
BTN_VOLUP = 16
BTN_VOLDN = 26
BTN_ONOFF = 12

BUTTONS = [BTN_REWIND, BTN_FASTFWD, BTN_PLAYPAUSE, BTN_VOLUP, BTN_VOLDN, BTN_ONOFF]

pixels = [[0,0,0,BRIGHTNESS]] * NUM_PIXELS

_button_repeat = {}
_button_handlers = {}
_clear_on_exit = True

def _exit():
    if _clear_on_exit:
        clear()
        show()
    GPIO.cleanup()

def on(buttons, handler=None, repeat=True):
    """Attach a handler function to one or more buttons.

    Can be used as a decorator, or optionally supplied a handler param.

    :param buttons: Individual button pin or list of pins to watch
    :param handler: Optional handler function
    ;param repeat: Whether the handler should be repeated if the button is held

    """

    buttons = buttons if isinstance(buttons, list) else [buttons]

    for button in buttons:
        _button_repeat[button] = repeat

    if handler is not None:
        for button in buttons:
            _button_handlers[button] = handler

    else:
        def attach_handler(handler):
            for button in buttons:
                _button_handlers[button] = handler

        return attach_handler
    

def set_brightness(brightness, channel = None):
    """Set the brightness of all pixels

    :param brightness: Brightness: 0.0 to 1.0

    """

    if brightness < 0 or brightness > 1:
        raise ValueError("Brightness should be between 0.0 and 1.0")

    if channel is None or channel == 0:
        for x in range(CHANNEL_PIXELS):
            pixels[x][3] = int(31.0 * brightness) & 0b11111

    if channel is None or channel == 1:
        for x in range(CHANNEL_PIXELS):
            pixels[x + (CHANNEL_PIXELS)][3] = int(31.0 * brightness) & 0b11111

def clear(channel = None):
    """Clear the pixel buffer"""

    if channel is None or channel == 0:
        for x in range(CHANNEL_PIXELS):
            pixels[x][0:3] = [0,0,0]

    if channel is None or channel == 1:
        for x in range(CHANNEL_PIXELS):
            pixels[x + (CHANNEL_PIXELS)][0:3] = [0,0,0]

def _write_byte(byte):
    for x in range(8):
        GPIO.output(DAT, byte & 0b10000000)
        GPIO.output(CLK, 1)
        byte <<= 1
        GPIO.output(CLK, 0)

# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
# for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
def _eof():
    GPIO.output(DAT, 0)
    for x in range(36):
        GPIO.output(CLK, 1)
        GPIO.output(CLK, 0)

def _sof():
    GPIO.output(DAT,0)
    for x in range(32):
        GPIO.output(CLK, 1)
        GPIO.output(CLK, 0)

def _handle_button(pin):
    if pin in _button_handlers.keys() and callable(_button_handlers[pin]):
        _button_handlers[pin](pin)

        if not _button_repeat[pin]:
            return

        delay = 0.25
        ramp_rate = 0.90

        for x in range(50):
            time.sleep(0.01)
            if GPIO.input(pin):
                return

        while not GPIO.input(pin):
            _button_handlers[pin](pin)
            time.sleep(delay)
            delay *= ramp_rate
            delay = max(0.01, delay)

def show():
    """Output the buffer to the displays"""

    _sof()

    for pixel in pixels:
        r, g, b, brightness = pixel
        _write_byte(0b11100000 | brightness)
        _write_byte(b)
        _write_byte(g)
        _write_byte(r)

    _eof()

def set_all(r, g, b, brightness=None, channel=None):
    """Set the RGB value and optionally brightness of all pixels

    If you don't supply a brightness value, the last value set for each pixel be kept.

    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
    :param channel: Optionally specify which bar to set: 0 or 1

    """

    if channel is None or channel == 0:
        for x in range(CHANNEL_PIXELS):
            set_pixel(x, r, g, b, brightness)

    if channel is None or channel == 1:
        for x in range(CHANNEL_PIXELS):
            set_pixel(x + (CHANNEL_PIXELS), r, g, b, brightness)

def set_pixel(x, r, g, b, brightness=None, channel=None):
    """Set the RGB value, and optionally brightness, of a single pixel
    
    If you don't supply a brightness value, the last value will be kept.

    :param x: The horizontal position of the pixel: 0 to 7
    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
    :param channel: Optionally specify which bar to set: 0 or 1

    """

    if brightness is None:
        brightness = pixels[x][3]
    else:
        brightness = int(31.0 * brightness) & 0b11111

    if channel in [0, 1]:
        if x >= CHANNEL_PIXELS:
            raise ValueError("Index should be < {} when displaying on a specific channel".format(CHANNEL_PIXELS))

        x += channel * (CHANNEL_PIXELS)

    pixels[x] = [int(r) & 0xff,int(g) & 0xff,int(b) & 0xff,brightness]


def set_clear_on_exit(value=True):
    """Set whether the displays should be cleared upon exit

    By default the displays will turn off on exit, but calling::

        phatbeat.set_clear_on_exit(False)

    Will ensure that it does not.

    :param value: True or False (default True)

    """

    global _clear_on_exit
    _clear_on_exit = value

atexit.register(_exit)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([DAT,CLK],GPIO.OUT)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for button in BUTTONS:
    GPIO.add_event_detect(button, GPIO.FALLING, callback=_handle_button, bouncetime=200)
