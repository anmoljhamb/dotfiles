#!/bin/bash

echo "Updating and Upgrading"

apt update && apt upgrade

echo "Changing Shell"

apt install zsh

chsh

sudo apt install git

echo "Installing NVIM"

wget https://github.com/neovim/neovim/releases/download/v0.11.2/nvim-linux-x86_64.appimage
mkdir -p ~/Applications
mv nvim-linux-x86_64.appimage ~/Applications/nvim.appimage

export PATH=$PATH:~/Applications

sudo apt install luarocks python3 python3-pip python3-venv fzf ripgrep
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

nvm install --lts
mkdir -p ~/.config
git clone https://github.com/anmoljhamb/nvim-config.git ~/.config/nvim

echo "Setting up OhMyZsh"

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

sudo apt install zoxide

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
cp ~/dotfiles/.zshrc ~/.zshrc

echo "setting up the locale"
nvim.appimage /etc/local.gen
local-gen
sudo update-locale LANG=en_US.UTF-8

sudo apt install tmux
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
cp ~/dotfiles/.tmux.conf ~/
