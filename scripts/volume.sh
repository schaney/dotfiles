#!/bin/bash

if [[ `awk -F"[][]" '/dB/ { print $6 }' <(amixer sget Master)` == "off" ]]
then
    echo "MUTE"
else
    awk -F"[][]" '/dB/ { print $2 }' <(amixer sget Master)
fi
