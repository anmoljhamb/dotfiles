#!/bin/bash
# Save clipboard image to file with auto-naming + optional rename via rofi
# Clicking the notification opens the screenshot folder
# Usage: Triggered via keybinding after taking a screenshot to clipboard

# Check if clipboard contains an image
MIME=$(wl-paste --list-types 2>/dev/null | grep -E '^image/' | head -1)

if [ -z "$MIME" ]; then
    notify-send "Screenshot" "No image found in clipboard" -t 2000
    exit 1
fi

# Determine file extension from MIME type
case "$MIME" in
    image/png)  EXT="png" ;;
    image/jpeg) EXT="jpg" ;;
    image/webp) EXT="webp" ;;
    image/bmp)  EXT="bmp" ;;
    *)          EXT="png" ;;
esac

# Auto-generate filename and save immediately
SAVE_DIR="$HOME/Pictures/Screenshots"
mkdir -p "$SAVE_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="screenshot_${TIMESTAMP}.${EXT}"
SAVE_PATH="$SAVE_DIR/$FILENAME"

wl-paste > "$SAVE_PATH"

if [ $? -ne 0 ] || [ ! -f "$SAVE_PATH" ]; then
    notify-send "Screenshot" "Failed to save" -t 2000
    exit 1
fi

# Offer optional rename via rofi (just the filename, no path)
NEW_NAME=$(echo "$FILENAME" | rofi -dmenu -p "📸 Rename" \
    -theme-str 'window {width: 40%;}' \
    -theme-str 'entry {placeholder: "Press Enter to keep default...";}')

# If user typed a new name (and didn't cancel), rename the file
if [ -n "$NEW_NAME" ] && [ "$NEW_NAME" != "$FILENAME" ]; then
    # Add extension if user didn't include one
    if [[ "$NEW_NAME" != *.* ]]; then
        NEW_NAME="${NEW_NAME}.${EXT}"
    fi
    mv "$SAVE_PATH" "$SAVE_DIR/$NEW_NAME"
    SAVE_PATH="$SAVE_DIR/$NEW_NAME"
    FILENAME="$NEW_NAME"
fi

# If user pressed Escape in rofi, file stays with the auto-generated name

# Show notification with "Open Folder" action button
# Runs in background so the script can exit immediately
(
    ACTION=$(notify-send "Screenshot saved ✓" "$FILENAME" \
        -i "$SAVE_PATH" \
        -t 5000 \
        -A "open=📂 Open Folder" \
        --wait)

    if [ "$ACTION" = "open" ]; then
        dolphin "$SAVE_DIR" &>/dev/null
    fi
) &

exit 0
