#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}


run nm-applet &
blueman-applet &
~/dotfiles/scripts/change_wallpaper
picom --config $HOME/.config/picom/picom.conf &
