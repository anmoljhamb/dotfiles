#!/bin/bash

NAME="Anmol Jhamb"
EMAIL="talktoanmol@outlook.com"
counter=1

confirm() {
    local prompt_message="$1"  # First argument is the message
    local function_to_call="$2"  # Second argument is the function name

    read -r -p "$prompt_message (Press Enter to proceed, type 's' to skip) " response

    if [[ "$response" != "s" ]]; then
        # Call the function if the user doesn't skip
        "$function_to_call"
    else
        echo "Step skipped."
    fi
}

notify(){
  cat << EOF
---
${1}: ${2}
EOF
((counter++))
}

installPreReq(){
  notify $counter "Intalling PreRequesites"
  pre_reqs=$(tr '\n' ' ' < ./pre-reqs.txt)
  echo "$pre_reqs" | xargs sudo apt install -y 
  pip install -r ~/dotfiles/requirements.txt --break-system-packages
}

installChrome(){
  notify $counter "Intalling Chrome"
  chrome_url="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
  wget $chrome_url -O /tmp/google-chrome-stable_current_amd64.deb
  sudo apt install -y /tmp/google-chrome-stable_current_amd64.deb
  rm -f /tmp/google-chrome-stable_current_amd64.deb
}

setupGit(){
  notify $counter "Setting up Git"
  ssh_file=~/.ssh/heyitsanmolj_github
  git config --global user.email "$EMAIL"
  git config --global user.name "$NAME"
  ssh-keygen -t ed25519 -C "$EMAIL" -f $ssh_file
  eval "$(ssh-agent -s)"
  ssh-add $ssh_file
  xclip -selection clipboard -i "$ssh_file.pub"
}

linkAll(){
  notify $counter "Linking all dotfiles"
  python3 ~/dotfiles/link_all.py
}

setupNpm(){
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  # shellcheck source=/dev/null
  source ~/.bashrc
  nvm install --lts
}

setupNvim(){
  notify $counter "Setup NeoVim"
  wget https://github.com/neovim/neovim/releases/download/v0.10.2/nvim.appimage -O ~/Applications/nvim.appimage
  chmod u+x ~/Applications/nvim.appimage
}

setupZsh(){
  notify $counter "Setup ZSH"
  chsh -s /bin/zsh
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
  sudo dpkg-reconfigure locales
  rm ~/.zshrc
}

confirm "Install PreRequesites?" installPreReq
confirm "Install Google Chrome?" installChrome
confirm "Setup git?" setupGit
confirm "Setup npm?" setupNpm
confirm "Setup nvim?" setupNvim
confirm "Setuo zsh?" setupZsh
confirm "Link All Dotfiles?" linkAll
