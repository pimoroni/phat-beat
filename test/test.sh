#!/bin/sh

echo "testing audio"

speaker-test -l1 -c2 -t wav
sleep 1

aplay ./test.wav
sleep 1

if command -v mpg321 > /dev/null; then
    mpg321 ./test.mp3
    sleep 1
fi

echo "testing gpio control..."
echo "press all buttons along the side of the pHAT..."
echo "press the power button on the pHAT to exit..."
sleep 1

echo "testing VU meter"
python ./test.py

exit 0
