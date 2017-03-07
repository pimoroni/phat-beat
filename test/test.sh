#!/bin/sh

echo "testing audio"

speaker-test -l5 -c2 -t wav
sleep 1

aplay ./test.wav
sleep 1

if command -v mpg321 > /dev/null; then
    mgp321 ./test.mp3
    sleep 1
fi

echo "testing VU meter"
python ./test.py

exit 0
