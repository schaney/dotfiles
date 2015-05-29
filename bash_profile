source ~/.creds
source ~/.aliases
source ~/dev/adzerk/.adzerk
source ~/.colors

if [ -f ~/.git-completion.bash ]; then
  . ~/.dotfiles/scripts/git-completion.bash
fi

if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi

export PATH=/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/usr/local/bin:$PATH
export EDITOR="subl -n -w"
export TERM=xterm-color
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export PS1="${c_green}\h:${c_magenta}\w${c_blue}\$(__git_ps1 ' [%s]')${c_magenta} → ${c_reset}"

[ -f /Users/sean/.travis/travis.sh ] && source /Users/sean/.travis/travis.sh

~/.dotfiles/scripts/welcome.sh

