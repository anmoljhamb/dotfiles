#!/bin/bash

# This script allows you to change brightness:
# $./brightness.sh up
# $./brightness.sh down

function get_brightness {
    local current=$(brightnessctl g)
    local max=$(brightnessctl m)
    awk -v cur="$current" -v max="$max" 'BEGIN { printf "%.0f", cur / max * 100 }'
}

function is_brightness_off {
    brightness=$(get_brightness)
    if [ "$brightness" -eq 0 ]; then
        return 0  # Brightness is off
    else
        return 1  # Brightness is not off
    fi
}

function send_notification {
    DIR=$(dirname "$0")
    brightness=$(get_brightness)

    if [ "$brightness" = "0" ]; then
        icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-low.svg"
    else
        if [ "$brightness" -lt "10" ]; then
            icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-low.svg"
        else
            if [ "$brightness" -lt "30" ]; then
                icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-low.svg"
            else
                if [ "$brightness" -lt "70" ]; then
                    icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-high.svg"
                else
                    if [ "$brightness" -lt "100" ]; then
                        icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-high.svg"
                    else
                        icon_name="/usr/share/icons/breeze-dark/actions/24/brightness-high.svg"
                    fi
                fi
            fi
        fi
    fi
    # Send the notification without text body to trigger slider widget in swaync
    $DIR/notify-send.sh -i "$icon_name" -t 2000 -h int:value:"$brightness" -h string:synchronous:"brightness" --replace=555 "Brightness" ""
}

case $1 in
    up)
        # Increase brightness (+ 10%)
        brightnessctl set +10% > /dev/null
        send_notification
        ;;
    down)
        # Decrease brightness (- 10%)
        brightnessctl set 10%- > /dev/null
        send_notification
        ;;
    off)
        # Set brightness to 0 (off)
        brightnessctl set 0% > /dev/null
        send_notification
        ;;
esac
