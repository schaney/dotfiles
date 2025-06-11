#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
artpath=$dir/$(hostname).ascii

if [[ -f $artpath ]]; then
  picture="$(cat $dir/$(hostname).ascii)"
else
  picture="$(cat $dir/batman.ascii)"
fi
if command -v lolcat > /dev/null; then
  seed=$(( ($RANDOM % 256) + 1))
  freq=$(echo "scale=3; $(((RANDOM % 200) + 100))/1000" | bc)
  spread=$(echo "scale=3; $(((RANDOM % 1000) + 1))/100 + 0.1" | bc)
  echo "$picture" | lolcat --seed $seed -F $freq -t -p $spread
else
  color=$(( ($RANDOM % 256) + 1))
  echo "$(tput setaf $color)${picture}"
fi
echo
