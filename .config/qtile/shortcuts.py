from constants import ALT_KEY, BROWSER, TERMINAL, WINDOWS_KEY
from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
# Switch between windows

window_management = [
    Key(["control", "shift"], "h", lazy.layout.left(), desc="Move focus to left"),
    Key(["control", "shift"], "l", lazy.layout.right(), desc="Move focus to right"),
    Key(["control", "shift"], "j", lazy.layout.down(), desc="Move focus down"),
    Key(["control", "shift"], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        ["control", "shift"],
        "space",
        lazy.layout.next(),
        desc="Move window focus to other window",
    ),
    Key([WINDOWS_KEY], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [WINDOWS_KEY],
        "m",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [WINDOWS_KEY],
        "y",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
]

layout_management = [
    Key(
        [WINDOWS_KEY, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([WINDOWS_KEY], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [WINDOWS_KEY, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"
    ),
]

window_resizing = [
    KeyChord(
        [WINDOWS_KEY],
        "Return",
        [
            Key([], "h", lazy.layout.shuffle_left(), desc="Move window left"),
            Key([], "l", lazy.layout.shuffle_right(), desc="Move window right"),
            Key([], "j", lazy.layout.shuffle_down(), desc="Move window down"),
            Key([], "k", lazy.layout.shuffle_up(), desc="Move window up"),
            Key([], "q", lazy.window.kill(), desc="Kill focused window"),
            Key(
                ["shift"],
                "l",
                lazy.layout.grow_left(),
                lazy.layout.grow(),
                desc="Grow window left",
            ),
            Key(
                ["shift"],
                "h",
                lazy.layout.grow_right(),
                lazy.layout.shrink(),
                desc="Grow window right",
            ),
            Key(["shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
            Key(["shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
            Key(["shift"], "n", lazy.layout.normalize(), desc="Normalize window size"),
            Key([], "m", lazy.layout.maximize(), desc="Maximize window"),
        ],
        mode=True,
        name="Resize",
    ),
]

application_launchers = [
    Key([WINDOWS_KEY], "t", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([WINDOWS_KEY], "r", lazy.spawn("rofi -show drun"), desc="Launch Rofi drun"),
    Key([WINDOWS_KEY], "b", lazy.spawn("blueman-manager"), desc="Launch bluetooth-manager"),
    Key(
        [WINDOWS_KEY, "shift"],
        "r",
        lazy.spawn("rofi -show run"),
        desc="Launch Rofi run",
    ),
    Key(
        [ALT_KEY, "shift"],
        "1",
        lazy.spawn(BROWSER + ' --profile-directory="Default"'),
    ),
    Key(
        [ALT_KEY, "shift"],
        "2",
        lazy.spawn(BROWSER + ' --profile-directory="Profile 1"'),
    ),
    Key(
        [ALT_KEY, "shift"],
        "3",
        lazy.spawn(BROWSER + ' --profile-directory="Profile 2"'),
    ),
    Key([ALT_KEY, "shift"], "m", lazy.spawn("flatpak run com.spotify.Client")),
    Key([ALT_KEY, "shift"], "p", lazy.spawn("/home/anmol/Applications/Postman/Postman")),
    Key(
        [ALT_KEY, "shift"],
        "a",
        lazy.spawn("/home/anmol/Applications/arduino-ide_2.3.2_Linux_64bit.AppImage"),
    ),
    Key(
        [ALT_KEY, "shift"],
        "n",
        lazy.spawn("/home/anmol/Applications/Obsidian-1.5.8.AppImage"),
    ),
]

system_controls = [
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("/home/anmol/dotfiles/scripts/brightness.sh up"),
        desc="Raise brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("/home/anmol/dotfiles/scripts/brightness.sh down"),
        desc="Lower brightness",
    ),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take screenshot"),
    Key([ALT_KEY, "shift"], "s", lazy.spawn("flameshot gui"), desc="Take screenshot"),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("/home/anmol/dotfiles/scripts/volume.sh up"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("/home/anmol/dotfiles/scripts/volume.sh down"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("/home/anmol/dotfiles/scripts/volume.sh mute"),
        desc="Mute/Unmute volume",
    ),
    Key([WINDOWS_KEY], "x", lazy.spawn("playerctl next"), desc="Next track"),
    Key([WINDOWS_KEY], "z", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key(
        [WINDOWS_KEY],
        "space",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause music",
    ),
    Key([WINDOWS_KEY, "shift"], "l", lazy.spawn("i3lock"), desc="Lock screen"),
    Key([ALT_KEY, "shift"], "r", lazy.reload_config(), desc="Reload Qtile config"),
    Key([WINDOWS_KEY, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([WINDOWS_KEY, "shift"], "n", lazy.spawn("dunstctl set-paused toggle")),
    Key([WINDOWS_KEY, "shift"], "d", lazy.spawn("dunstctl close-all")),
    Key(
        [ALT_KEY, "shift"],
        "w",
        lazy.spawn(
            "/usr/bin/python3 /home/anmol/dotfiles/scripts/wallpaper_modifier.py"
        ),
    ),
]

group_navigation = [
    Key(
        [WINDOWS_KEY, "shift"],
        "w",
        lazy.screen.next_group(skip_empty=True),
        desc="Move to next group",
    ),
    Key(
        [WINDOWS_KEY, "shift"],
        "s",
        lazy.screen.prev_group(skip_empty=True),
        desc="Move to previous group",
    ),
    Key([ALT_KEY], "Tab", lazy.screen.toggle_group(), desc="Toggle between groups"),
]

scratch_pads = [
    Key(
        [WINDOWS_KEY],
        "f",
        lazy.group["scratchpad"].dropdown_toggle("file_manager"),
        desc="Launch File Explorer",
    ),
    Key(
        [],
        "F1",
        lazy.group["scratchpad"].dropdown_toggle("terminal"),
        desc="Launch Terminal",
    ),
    Key(
        [],
        "F3",
        lazy.group["scratchpad"].dropdown_toggle("ytmusic"),
        desc="Launch YT Music",
    ),
]

shortcut_keys = [
    *window_management,
    *layout_management,
    *window_resizing,
    *application_launchers,
    *system_controls,
    *group_navigation,
    *scratch_pads,
]
