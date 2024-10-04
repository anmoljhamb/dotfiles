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
$counter: ${1}
EOF
((counter++))
}

installPreReq(){
  notify "Intalling PreRequesites"
  pre_reqs=$(tr '\n' ' ' < ./pre-reqs.txt)
  echo "$pre_reqs" | xargs sudo apt install -y 
  pip install -r ~/dotfiles/requirements.txt --break-system-packages
}

installChrome(){
  notify "Intalling Chrome"
  chrome_url="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
  wget $chrome_url -O /tmp/google-chrome-stable_current_amd64.deb
  sudo apt install -y /tmp/google-chrome-stable_current_amd64.deb
  rm -f /tmp/google-chrome-stable_current_amd64.deb
}

setupGit(){
  notify "Setting up Git"
  ssh_file=~/.ssh/heyitsanmolj_github
  git config --global user.email "$EMAIL"
  git config --global user.name "$NAME"
  ssh-keygen -t ed25519 -C "$EMAIL" -f $ssh_file
  eval "$(ssh-agent -s)"
  ssh-add $ssh_file
  xclip -selection clipboard -i "$ssh_file.pub"
}

linkAll(){
  notify "Linking all dotfiles"
  python3 ~/dotfiles/link_all.py
}

setupNpm(){
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  # shellcheck source=/dev/null
  source ~/.bashrc
  nvm install --lts
}

setupNvim(){
  notify "Setup NeoVim"
  wget https://github.com/neovim/neovim/releases/download/v0.10.2/nvim.appimage -O ~/Applications/nvim.appimage
  chmod u+x ~/Applications/nvim.appimage
}

setupZsh(){
  notify "Setup ZSH"
  chsh -s /bin/zsh
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
  sudo dpkg-reconfigure locales
  rm ~/.zshrc
}

installFont(){
  notify "Installing Font"
  wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/CascadiaCode.zip -O /tmp/CascadiaCode.zip
  cd /tmp
  unzip CascadiaCode.zip -d font
  mkdir -p ~/.fonts
  mv /tmp/font/*.ttf ~/.fonts
}

setupAlacritty(){
  notify "Setting up Alacritty"
  curl https://sh.rustup.rs -sSf | sh
  # shellcheck source=/dev/null
  source ~/.zshrc
  git clone https://github.com/alacritty/alacritty.git
  cd alacritty
  rustup override set stable
  rustup update stable
  cargo build --release
  infocmp alacritty
  sudo cp target/release/alacritty /usr/local/bin
  sudo mkdir -p /usr/local/share/man/man1
  sudo mkdir -p /usr/local/share/man/man5
  scdoc < extra/man/alacritty.1.scd | gzip -c | sudo tee /usr/local/share/man/man1/alacritty.1.gz > /dev/null
  scdoc < extra/man/alacritty-msg.1.scd | gzip -c | sudo tee /usr/local/share/man/man1/alacritty-msg.1.gz > /dev/null
  scdoc < extra/man/alacritty.5.scd | gzip -c | sudo tee /usr/local/share/man/man5/alacritty.5.gz > /dev/null
  scdoc < extra/man/alacritty-bindings.5.scd | gzip -c | sudo tee /usr/local/share/man/man5/alacritty-bindings.5.gz > /dev/null
  mkdir -p ${ZDOTDIR:-~}/.zsh_functions\necho 'fpath+=${ZDOTDIR:-~}/.zsh_functions' >> ${ZDOTDIR:-~}/.zshrc
  cp extra/completions/_alacritty ${ZDOTDIR:-~}/.zsh_functions/_alacritty
  cd ..
  rm -rf ~/alacritty
}

setupTmux(){
  notify "Setting Up Tmux"
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
}

setupQtile(){
  notify "Setting up Qtile"
  mkdir -p ~/logs
  sudo wget https://raw.githubusercontent.com/qtile/qtile/refs/heads/master/resources/qtile.desktop -O /usr/share/xsessions/qtile.desktop
  sudo gpasswd -a $USER input
  newgrp input
  sudo apt-get install libinput-tools
  sudo apt-get install ruby
  sudo gem install fusuma
  echo "1" >> ~/dotfiles/Wallpapers/curr_wallpaper
  cd ~
  git clone https://github.com/vinceliuice/Tela-icon-theme.git
  cd Tela-icon-theme
  ./install.sh
  cd ..
  # cd ..
}

installGrubTheme(){
  notify "Installing Grub Theme"
  git clone https://github.com/vinceliuice/grub2-themes.git
  cd grub2-themes
  sudo ./install.sh -b -t tela
  cd ..
  rm -rf grub2-themes
}

if [[ $# -eq 0 ]]; then
  echo "Please provide a step name to run."
  exit 1
fi

step_to_run="$1"

case "$step_to_run" in
  installPreReq)
    installPreReq
    ;;
  installChrome)
    installChrome
    ;;
  setupGit)
    setupGit
    ;;
  linkAll)
    linkAll
    ;;
  setupNpm)
    setupNpm
    ;;
  setupNvim)
    setupNvim
    ;;
  setupZsh)
    setupZsh
    ;;
  intallFont)
    intallFont
    ;;
  setupAlacritty)
    setupAlacritty
    ;;
  setupTmux)
    setupTmux
    ;;
  setupQtile)
    setupQtile
    ;;
  installGrubTheme)
    installGrubTheme
    ;;
  *)
    echo "Unknown step: $step_to_run"
    echo "Available steps: installPreReq, installChrome, setupGit, linkAll, setupNpm, setupNvim, setupZsh, installFont, setupAlacritty, setupTmux, setupQtile, installGrubTheme"
    exit 1
    ;;
esac
