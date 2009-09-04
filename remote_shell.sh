if [ $USER = "root" ]; then
	PS_COLOR="31m";
else
	PS_COLOR="32m";
	export TMPDIR="$HOME/.tmp";
fi
export PS1="\n[01;$PS_COLOR\u@\h[0m : \t : [01;34m\w[0m\n\$ "

export EDITOR="emacs";
export BLOCKSIZE=K;
export PAGER="less";

### default arguments to commands
alias ls="ls -F -G";
alias rm="rm -i";
alias cp="cp -i";
alias mv="mv -i";

### helpers
alias l="ls";
alias sl="ls";
alias lss="ls --hide=*~"
alias la="ls -a";
alias ll="ls -l";
alias lal="ls -al";
alias lsd="ls -l | grep ^d";
alias psg="ps ax | grep";
alias clpy="rm -f *~ *pyc"
alias pwdd="pwd -P";
alias sudoo="sudo /bin/bash -l";
