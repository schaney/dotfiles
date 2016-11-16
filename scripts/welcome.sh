#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cat $dir/batman.ascii | lolcat --seed 3 -p 10000 -F 0.7
echo
