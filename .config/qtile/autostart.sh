#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}


run nm-applet &
blueman-applet &
/bin/python3 ~/dotfiles/scripts/wallpaper_modifier.py &
picom --config $HOME/.config/picom/picom.conf &
# flatpak run org.jellyfin.JellyfinServer &
