# -*- mode: sh;-*-

export PATH=/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/usr/local/bin:$PATH
export EDITOR="ew"
export TERM=xterm-256color
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export MONO_PATH=/Library/Frameworks/Mono.framework/Versions/
export NODE_PATH=/usr/local/lib/node_modules
export AWS_DEFAULT_PROFILE=work
export KONSOLE_DBUS_SESSION=true

[ -z $ADZERK_SCRIPTS_PATH ] && export ADZERK_SCRIPTS_PATH=$HOME/dev/adzerk/cli-tools/scripts

source ~/.colors
source ~/.aliases

if [[ $ADZERK_SCRIPTS_PATH ]]; then
    PATH="$PATH:$ADZERK_SCRIPTS_PATH:$ADZERK_SCRIPTS_PATH/../micha"
fi

[ -d ~/.scripts ] && PATH="$PATH:$HOME/.scripts"

[ -f ~/dev/adzerk/.adzerk ] && source ~/dev/adzerk/.adzerk
[ -f ~/.git-completion.bash ] && source ~/.dotfiles/git-completion.bash
[ -f ~/.git-prompt.sh ] && source ~/.dotfiles/git-prompt.sh

command_exists () {
    type "$1" &> /dev/null ;
}

[ `uname` != "Darwin" ] && command_exists xset && xset m 0 0

# #U+039B

# __env_marker()
# {
#     if [ $ENV_IS_SET ]
#     then
#         echo "${c_red} (Λ)"
#     fi
# }


export PS1="${c_green}\h:${c_magenta}\w${c_blue}\$(__git_ps1 ' [%s]')${c_magenta} → ${c_reset}"


[ -f /Users/sean/.travis/travis.sh ] && source /Users/sean/.travis/travis.sh

~/.dotfiles/scripts/welcome.sh

sr () {
  for agent in /tmp/ssh-*/agent.*; do
    export SSH_AUTH_SOCK=$agent
    if ssh-add -l 2>&1 > /dev/null; then
      echo Found working SSH Agent:
      ssh-add -l
      return
    fi
  done
  echo Cannot find ssh agent - maybe you should reconnect and forward it?
}

gc ()
{
    local FROM="git@github.com:${1?}";
    local TO="$HOME/dev/${1?}";
    if [ -d "$TO" ]; then
       echo "Already done!";
    else
       git clone "$FROM" "$TO";
    fi;
    cd "$TO"
}

creds ()
{
    if [ $ENV_IS_SET ]
    then
        echo "env is already set :)"
    else
        eval "$(gpg -d ~/.creds.asc)"
    fi
}

function .. { # "cd up" - move up $1 directories
  local num;
  local dest;
  num=${1:-1}
  while [[ $num > 0 ]]; do
    dest="../${dest}"
    (( num-- ))
  done
  cd "${dest}"
}

bind 'set completion-ignore-case on'

# added by travis gem
[ -f /data/home/sean/.travis/travis.sh ] && source /data/home/sean/.travis/travis.sh

export NVM_DIR="/data/home/sean/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
