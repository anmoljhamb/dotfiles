export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(git zsh-autosuggestions)

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

alias vim="nvim"
alias d="deactivate"
alias editzsh="vim ~/.zshrc"
alias editvim="cd ~/.config/nvim && vim ."
alias soz="source ~/.zshrc"
# alias cd="z"
alias gac="git add . && git commit -am "
alias tmux="tmux -u"
alias ts="tmux_sessionizer"
alias ta='tmux attach-session -t "$(tmux ls 2>/dev/null | cut -d: -f1 | fzf)"'
alias tk='tmux kill-session -t "$(tmux ls 2>/dev/null | cut -d: -f1 | fzf)"'
alias td="tmux detach"
alias tl="tmux ls"
alias sva="source .venv/bin/activate"
alias cve="python3 -m venv .venv"
alias pir="pip install -r requirements.txt"
alias cab="conda activate base"
alias ctcb="xclip -selection clipboard"
alias dcu="docker compose up"
alias dcl="docker compose logs"
alias dclf="docker compose logs --follow"
alias dcub="docker compose up --build"
alias dcd="docker compose down"
alias dir="exa -l"
alias ls="exa -l"

export PATH="$PATH:/home/anmol/.local/bin"
export PATH="$PATH:/home/anmol/bin"
export PATH="$PATH:/home/anmol/go/bin"


# Load Angular CLI autocompletion.
# source <(ng completion script)
fpath+=${ZDOTDIR:-~}/.zsh_functions

source <(fzf --zsh)

export PATH=/Users/consultadd/.opencode/bin:$PATH
export PATH="$HOME/.local/bin:$PATH"

# pnpm
export PNPM_HOME="/Users/consultadd/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end
#
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
