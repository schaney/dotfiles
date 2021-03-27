#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
picture="$(cat $dir/$(hostname).ascii)"
if command -v lolcat > /dev/null; then
  echo "$picture" | lolcat --seed 3 -F .12
else
  echo "$(tput setaf 3)${picture}"
fi
echo
