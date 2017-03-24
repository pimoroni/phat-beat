![pHAT BEAT](phat-beat-logo.png)

Stereo amplifier, buttons and dual RGB VU meter for your Pi.

https://shop.pimoroni.com/products/phat-beat

## Installing

### Full install ( recommended ):

We've created a super-easy installation script that will install all pre-requisites and get your pHAT BEAT
up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop like so:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the following and follow the instructions:

```bash
curl https://get.pimoroni.com/phatbeat | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/phatbeat/`.

Alternatively, on Raspbian, download the `pimoroni-dashboard` and install your product by browsing to the relevant entry:

```bash
sudo apt-get install pimoroni
```

### Manual install:

#### Library install for Python 3:

on Raspbian:

```bash
sudo apt-get install python3-phatbeat
```
other environments: 

```bash
sudo pip3 install phatbeat
```

#### Library install for Python 2:

on Raspbian:

```bash
sudo apt-get install python-phatbeat
```
other environments: 

```bash
sudo pip2 install phatbeat
```

## Documentation & Support

* Buy product - https://shop.pimoroni.com/products/phat-beat
* Getting started - https://learn.pimoroni.com/tutorial/sandyj/soldering-phats
* Function reference - http://docs.pimoroni.com/phatbeat/
* GPIO Pinout - https://pinout.xyz/pinout/phat_beat
* Get help - http://forums.pimoroni.com/c/support

