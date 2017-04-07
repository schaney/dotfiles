#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if command -v lolcat > /dev/null; then
  cat $dir/batman.ascii | lolcat --seed 3 -p 10000 -F 0.7
fi
echo
