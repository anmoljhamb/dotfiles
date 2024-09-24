#!/bin/bash

# This script allows you to change brightness:
# $./brightness.sh up
# $./brightness.sh down

function get_brightness {
    brightnessctl g | awk '{printf "%.0f", $1 / 255 * 100}'
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
        icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-off.svg"
        $DIR/notify-send.sh "$brightness""      " -i "$icon_name" -t 2000 -h int:value:"$brightness" -h string:synchronous:"─" --replace=555
    else
        if [ "$brightness" -lt "10" ]; then
            icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-low.svg"
        else
            if [ "$brightness" -lt "30" ]; then
                icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-low.svg"
            else
                if [ "$brightness" -lt "70" ]; then
                    icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-medium.svg"
                else
                    if [ "$brightness" -lt "100" ]; then
                        icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-high.svg"
                    else
                        icon_name="/usr/share/icons/Papirus-Light/48x48/status/notification-display-brightness-full.svg"
                    fi
                fi
            fi
        fi
    fi
    bar=$(seq -s "─" $(($brightness/5)) | sed 's/[0-9]//g')
    # Send the notification
    $DIR/notify-send.sh "$brightness""     ""$bar" -i "$icon_name" -t 2000 -h int:value:"$brightness" -h string:synchronous:"$bar" --replace=555
}

case $1 in
    up)
        # Increase brightness (+ 5%)
        brightnessctl set +5% > /dev/null
        send_notification
        ;;
    down)
        # Decrease brightness (- 5%)
        brightnessctl set 5%- > /dev/null
        send_notification
        ;;
    off)
        # Set brightness to 0 (off)
        brightnessctl set 0% > /dev/null
        send_notification
        ;;
esac
