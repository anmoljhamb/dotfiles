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

confirm "Install PreRequesites?" installPreReq
confirm "Install Google Chrome?" installChrome
confirm "Setup git?" setupGit
