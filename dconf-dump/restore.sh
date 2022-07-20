#!/bin/bash
# Auto-generated script to restore shortcuts
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

dconf load /org/gnome/desktop/wm/keybindings/ < $SCRIPT_DIR/desktop/wm/keybindings.conf
dconf load /org/gnome/mutter/keybindings/ < $SCRIPT_DIR/mutter/keybindings.conf
dconf load /org/gnome/mutter/wayland/keybindings/ < $SCRIPT_DIR/mutter/wayland/keybindings.conf
dconf load /org/gnome/settings-daemon/plugins/media-keys/ < $SCRIPT_DIR/settings-daemon/plugins/media-keys.conf
