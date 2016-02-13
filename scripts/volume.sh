#!/bin/bash

pactl list sinks | grep "Volume" | tail -n 2 | head -n 1 | awk '{print $5}'
