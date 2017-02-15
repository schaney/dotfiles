# -*- mode: sh;-*-

export PATH=$HOME/.scripts:$HOME/local/bin:/opt/local/bin:/opt/local/sbin:/usr/local/sbin:/usr/local/bin:$PATH
export EDITOR="emacsclient -a \"\" -t"
export TERM=xterm-256color
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export MONO_PATH=/usr/lib/mono
export NODE_PATH=/usr/local/lib/node_modules
export KONSOLE_DBUS_SESSION=true
export HISTFILESIZE=100000000
export HISTSIZE=$HISTFILESIZE
export HISTCONTROL=ignoreboth
export HISTTIMEFORMAT='%F %T '
export PROMPT_COMMAND='history -a'
[ -z $ADZERK_SCRIPTS_PATH ] && export ADZERK_SCRIPTS_PATH=$HOME/dev/adzerk/cli-tools/scripts

source ~/.colors
source ~/.aliases

if [[ $ADZERK_SCRIPTS_PATH ]]; then
    PATH="$PATH:$ADZERK_SCRIPTS_PATH:$ADZERK_SCRIPTS_PATH/../micha:$ADZERK_SCRIPTS_PATH/../jarrod"
fi

[ -d ~/.scripts ] && export PATH="$PATH:$HOME/.scripts"
[ -d /usr/local/opt/go/bin ] && export GOPATH=/usr/local/opt/go/bin
[ -d /usr/local/opt/go/libexec/bin ] && export PATH=$PATH:/usr/local/opt/go/libexec/bin
[ -f ~/dev/adzerk/.adzerk ] && source ~/dev/adzerk/.adzerk
[ -f ~/.git-completion.bash ] && source ~/.dotfiles/git-completion.bash
[ -f ~/.git-prompt.sh ] && source ~/.dotfiles/git-prompt.sh

command_exists () {
    type "$1" &> /dev/null ;
}

[ `uname` != "Darwin" ] && [ $DISPLAY ] && command_exists xset && xset m 0 0 &> /dev/null

PROMPT_COMMAND=__prompt_command # Func to gen PS1 after CMDs

__prompt_command() {
    local EXIT="$?"
    PS1=""
    local sep="➤"
    if [ $EXIT != 0 ]; then
        PS1+="${c_red}${sep} \h"
    else
        PS1+="${c_green}${sep} \h"
    fi

    if [ $ADZERK_ENV_IS_SET ]
    then
        local redishcolor=$c_orange
    else
        local redishcolor=$c_purple
    fi
    PS1+="${redishcolor} ${sep} \w${c_blue}\$(__git_ps1 ' ${sep} [%s]')${redishcolor} ${c_yellow}${sep}${c_reset}  "
}



[ -f /Users/sean/.travis/travis.sh ] && source /Users/sean/.travis/travis.sh

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

hg () {
    history | grep "$1"
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
    ssh-add ~/.ssh/{id_rsa,*.pem}
    if [ $ADZERK_ENV_IS_SET ]
    then
        echo "env is already set :)"
    else
        eval "$(gpg -d ~/.creds.asc)"
    fi
}

function set-aws-keys {
    export AWS_ACCESS_KEY=$1
    export AWS_ACCESS_KEY_ID=$1
    export AWS_SECRET_KEY=$2
    export AWS_SECRET_KEY_ID=$2
    export AWS_SECRET_ACCESS_KEY=$2
    export AWS_SECRET_ACCESS_KEY_ID=$2
}

function aws-keys {
    if [[ "$1" == "reporting" ]]; then
        echo "setting reporting account keys"
        set-aws-keys $REPORTING_AWS_KEY $REPORTING_AWS_SECRET
    elif [[ "$1" == "personal" ]]; then
        echo "setting personal account keys"
        set-aws-keys $PERSONAL_AWS_KEY $PERSONAL_AWS_SECRET
    else
        echo "setting adzerk account keys"
        set-aws- $ADZERK_AWS_ACCESS_KEY $ADZERK_AWS_SECRET_KEY
    fi
}

fixcamera ()
{
    sudo killall AppleCameraAssistant; sudo killall VDCAssistant
}

fixssh ()
{
    eval $(tmux show-env |sed -n 's/^\(SSH_[^=]*\)=\(.*\)/export \1="\2"/p')
}

ee ()
{
    eval `sed 's/^/export /' $1`
}
[ `uname` != "Darwin" ] && complete -F _minimal ee

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

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

~/.dotfiles/scripts/welcome.sh
