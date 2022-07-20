#!/bin/bash
#use this to backup your current keybindings.
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

export DCONF_DUMP="$SCRIPT_DIR/dconf-dump"
echo "Backing up keyboard shortcuts to $DCONF_DUMP ..."
mkdir -p $DCONF_DUMP

export RESTORE_SCRIPT="$DCONF_DUMP/restore.sh"
echo '#!/bin/bash
# Auto-generated script to restore shortcuts
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
' > $RESTORE_SCRIPT

# Build this list by looking at output from: gsettings list-recursively | grep keybindings
for ELEM in desktop/wm/keybindings mutter/keybindings mutter/wayland/keybindings settings-daemon/plugins/media-keys
do
    export OUTPUT_FILE="$DCONF_DUMP/$ELEM.conf"
    export ORIGIN="/org/gnome/$ELEM/"
    
    export PARENT=$(dirname $OUTPUT_FILE)
    mkdir -p $PARENT
    dconf dump $ORIGIN > "$OUTPUT_FILE"
    
    export INPUT_FILE="$ELEM.conf"
    echo "dconf load $ORIGIN < \$SCRIPT_DIR/$INPUT_FILE" >> $RESTORE_SCRIPT
done