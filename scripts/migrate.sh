#!/bin/bash

NAME="Anmol Jhamb"
EMAIL="talktoanmol@outlook.com"

installPreReq(){
  cat << EOF
---
1. Installing prerequisites.
EOF

  pre_reqs=$(tr '\n' ' ' < ./pre-reqs.txt)
  echo "$pre_reqs" | xargs sudo apt install 
}

setupGit(){
  cat << EOF
---
2. Setting Up git.
EOF
  ssh_file=~/.ssh/heyitsanmolj_github
  git config --global user.email "$EMAIL"
  git config --global user.name "$NAME"
  ssh-keygen -t ed25519 -C "$EMAIL" -f $ssh_file
  eval "$(ssh-agent -s)"
  ssh-add $ssh_file
  xclip -selection clipboard -i "$ssh_file.pub"
}

installPreReq
setupGit
