#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
batman="$(cat $dir/batman.ascii)"
if command -v lolcat > /dev/null; then
  echo "$batman" | lolcat --seed 3 -p 10000 -F 0.7
else
  echo "$(tput setaf 3)${batman}"
fi
echo
