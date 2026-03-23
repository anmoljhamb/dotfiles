#!/bin/bash
# delete_word.sh - intelligently send Ctrl+Backspace or native Alt+Backspace
# Use wtype to avoid Hyprland's sendshortcut issues.

active_class=$(hyprctl activewindow -j | jq -r '.class')

if [[ "$active_class" == "kitty" ]]; then
    # Kitty natively uses Alt+Backspace to delete a word.
    # To bypass Hyprland's `bind = ALT, Backspace`, we synthesize Escape then Backspace,
    # which is exactly what terminals recognize as Alt+Backspace.
    wtype -k escape -k backspace
elif [[ "$active_class" == "Alacritty" || "$active_class" == "wezterm" ]]; then
    wtype -k escape -k backspace
else
    # For GUI apps (browsers, editors), Ctrl+Backspace deletes a word.
    wtype -M ctrl -k backspace -m ctrl
fi
