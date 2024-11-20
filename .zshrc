export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(git zsh-autosuggestions ssh-agent)

source $ZSH/oh-my-zsh.sh

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

export VISUAL=nvim
export EDITOR=nvim
export PATH=~/dotfiles/scripts:$PATH
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

eval "$(zoxide init zsh)"

# alias nvim="nvim.appimage"
alias vim="nvim"
alias editzsh="vim ~/.zshrc"
alias editvim="cd ~/.config/nvim && vim ."
alias soz="source ~/.zshrc"
# alias cd="z"
alias sdi="sudo dnf install"
alias gac="git add . && git commit -am "
alias tmux="tmux -u"
alias ts="tmux_sessionizer"
alias sva="source .venv/bin/activate"
alias cab="conda activate base"
alias ctcb="xclip -selection clipboard"
alias gfrh="git fetch && git reset --hard origin/dev"

export PATH=$PATH:/home/anmol/.spicetify
export PATH=$PATH:/home/anmol/Applications
export PATH=$PATH:/home/anmol/Android/Sdk/platform-tools
export PATH=/home/anmol/.pub-cache/bin:$PATH
export PATH=$PATH:/snap/bin
export PATH=$PATH:/sbin/
export PATH=$PATH:/home/anmol/Applications/squashfs-root/usr/bin
export PATH=$PATH:/usr/local/go/bin
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export FAQSERVER="159.89.165.219"
export BBB_SERVER="157.245.98.120"
# export TERM=xterm-256color

# Created by `pipx` on 2024-01-28 21:14:25
export PATH="$PATH:/home/anmol/.local/bin"
export PATH="$PATH:/home/anmol/bin"
export PATH="$PATH:/home/anmol/go/bin"

# . "$HOME/.cargo/env"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/anmol/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/anmol/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/anmol/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/anmol/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
# Automatically add SSH key to the SSH agent
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval $(ssh-agent -s)
    ssh-add ~/.ssh/faq-chatbot
    ssh-add ~/.ssh/id_ed25519
    ssh-add ~/.ssh/id_rsa
fi

# bun completions
[ -s "/home/anmol/.bun/_bun" ] && source "/home/anmol/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
export PATH="/home/anmol/Applications/apache-maven-3.9.8/bin:$PATH"


# Load Angular CLI autocompletion.
# source <(ng completion script)
fpath+=${ZDOTDIR:-~}/.zsh_functions
