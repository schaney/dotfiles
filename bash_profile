export PATH=/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/usr/local/bin:$PATH
export EDITOR="subl -n -w"
export TERM=xterm-color
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export ADZERK_SCRIPTS_PATH=$HOME/dev/cli-tools/scripts
export MONO_PATH=/Library/Frameworks/Mono.framework/Versions/
export NODE_PATH=/usr/local/lib/node_modules
export AWS_DEFAULT_PROFILE=work

source ~/.aliases
source ~/.creds
source ~/dev/adzerk/.adzerk
source ~/.colors

export PS1="${c_green}\h:${c_magenta}\w${c_blue}\$(__git_ps1 ' [%s]')${c_magenta} → ${c_reset}"

if [ -f ~/.git-completion.bash ]; then
  . ~/.dotfiles/git-completion.bash
fi

if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi

[ -f /Users/sean/.travis/travis.sh ] && source /Users/sean/.travis/travis.sh

~/.dotfiles/scripts/welcome.sh


[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
