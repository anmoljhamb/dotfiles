#!/bin/bash

NAME="Anmol Jhamb"
EMAIL="talktoanmol@outlook.com"
counter=1

notify(){
  cat << EOF
---
${1}: ${2}
EOF
}

installPreReq(){
  notify $counter "Intalling PreRequesites"
  pre_reqs=$(tr '\n' ' ' < ./pre-reqs.txt)
  echo "$pre_reqs" | xargs sudo apt install -y 
  ((counter++))
}

installChrome(){
  notify $counter "Intalling Chrome"
  chrome_url="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
  wget $chrome_url -O /tmp/google-chrome-stable_current_amd64.deb
  sudo apt install -y /tmp/google-chrome-stable_current_amd64.deb
  rm -f /tmp/google-chrome-stable_current_amd64.deb
  ((counter++))
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
  ((counter++))
}

installPreReq
installChrome
setupGit
