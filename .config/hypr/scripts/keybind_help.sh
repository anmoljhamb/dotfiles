#!/bin/bash
# Keybinding cheatsheet - shows all keybindings in a searchable rofi menu
# Parses keybindings.conf and uses comments as descriptions

CONFIG="$HOME/.config/hypr/keybindings.conf"

if [ ! -f "$CONFIG" ]; then
    notify-send "Keybind Help" "Config not found: $CONFIG" -t 3000
    exit 1
fi

# Parse bindings with their descriptions from comments
awk '
BEGIN { comment = ""; section = "" }

# Track section headers (comments followed by blank or bind lines)
/^# / {
    text = substr($0, 3)
    # If this looks like a section header (no previous comment pending)
    if (comment == "") {
        comment = text
    } else {
        # Chain comments (multi-line comment, keep the last one)
        comment = text
    }
    next
}

/^bind/ {
    # Remove bind prefix variants: bind, binde, bindm, bindl, bindel
    line = $0
    sub(/^bind[a-z]* = /, "", line)

    # Split by comma - format: MOD, KEY, dispatcher, params...
    n = split(line, parts, ",")
    mod = parts[1]
    key = parts[2]

    # Trim whitespace
    gsub(/^ +| +$/, "", mod)
    gsub(/^ +| +$/, "", key)

    # Build action string from remaining parts
    action = ""
    for (i = 3; i <= n; i++) {
        gsub(/^ +| +$/, "", parts[i])
        if (action == "") action = parts[i]
        else action = action " " parts[i]
    }

    # Skip submap internal bindings display clutter - mark them
    # Use comment as description if available, otherwise use the raw action
    desc = (comment != "") ? comment : action

    # Clean up modifier names for readability
    gsub(/\$mainMod/, "SUPER", mod)
    gsub(/SHIFT/, "Shift", mod)
    gsub(/CTRL/, "Ctrl", mod)
    gsub(/ALT/, "Alt", mod)

    # Format and print
    printf "%-35s  →  %s\n", mod " + " key, desc

    comment = ""
    next
}

# Reset comment on non-comment, non-bind, non-empty lines
/^[^#]/ && !/^bind/ && !/^[[:space:]]*$/ {
    comment = ""
}

# Also reset on blank lines (section break)
/^[[:space:]]*$/ {
    # Keep comment if it is a section header about to be followed by binds
    # Actually reset to avoid stale comments
    # comment = ""  # Uncomment to reset on blank lines
}
' "$CONFIG" | rofi -dmenu -i -p "🔍 Keybindings" \
    -no-custom \
    -theme-str 'window {width: 70%; height: 80%;}' \
    -theme-str 'listview {lines: 30;}' \
    -theme-str 'element {padding: 4px 8px;}' \
    -theme-str 'entry {placeholder: "Type to search...";}' \
    -mesg "Press Escape to close"
