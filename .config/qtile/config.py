import logging
import os
import subprocess
from typing import Optional

from libqtile import hook, qtile
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.layout.bsp import Bsp
from libqtile.layout.floating import Floating
from libqtile.layout.max import Max
from libqtile.layout.stack import Stack
from libqtile.layout.xmonad import MonadTall
from libqtile.lazy import lazy
from libqtile.widget.textbox import TextBox

from constants import (ALT_KEY, BROWSER, FONT_SIZE, GROUPS, KP, LAYOUTS,
                       TERMINAL, WINDOWS_KEY)
from custom_bar import custom_bar
from theme import nord_fox

logging.basicConfig(
    filename="/home/anmol/logs/qtile.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.debug("This is a debug message")


def left_half_circle(fg_color, bg_color: Optional["str"] = None):
    return TextBox(
        text="\uE0B6", fontsize=35, foreground=fg_color, background=bg_color, padding=0
    )


def right_half_circle(fg_color, bg_color: Optional["str"] = None):
    return TextBox(
        text="\uE0B4", fontsize=35, background=bg_color, foreground=fg_color, padding=0
    )


def lower_left_triangle(bg_color, fg_color: Optional["str"] = None):
    return TextBox(
        text="\u25e2", padding=0, fontsize=50, background=bg_color, foreground=fg_color
    )


def left_arrow(bg_color, fg_color: Optional["str"] = None):
    return TextBox(
        text="\uE0B2", padding=0, fontsize=25, background=bg_color, foreground=fg_color
    )


def right_arrow(bg_color, fg_color: Optional["str"] = None):
    return TextBox(
        text="\uE0B0", padding=0, fontsize=35, background=bg_color, foreground=fg_color
    )


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
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
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    # Grow windows. If current window is on the edge of screen and direction
    KeyChord(
        [WINDOWS_KEY],
        "Return",
        [
            Key(
                [],
                "h",
                lazy.layout.shuffle_left(),
            ),
            Key(
                [],
                "l",
                lazy.layout.shuffle_right(),
            ),
            Key([], "j", lazy.layout.shuffle_down()),
            Key([], "k", lazy.layout.shuffle_up()),
            Key([], "q", lazy.window.kill()),
            Key(["control"], "h", lazy.layout.left(), desc="Move focus to left"),
            Key(["control"], "l", lazy.layout.right(), desc="Move focus to right"),
            Key(["control"], "j", lazy.layout.down(), desc="Move focus down"),
            Key(["control"], "k", lazy.layout.up(), desc="Move focus up"),
            Key(["shift"], "l", lazy.layout.grow_left(), lazy.layout.grow()),
            Key(["shift"], "h", lazy.layout.grow_right(), lazy.layout.shrink()),
            Key(["shift"], "j", lazy.layout.grow_down()),
            Key(["shift"], "k", lazy.layout.grow_up()),
            Key(["shift"], "n", lazy.layout.normalize()),
            Key([], "m", lazy.layout.maximize()),
        ],
        mode=True,
        name="Resize",
    ),
    # will be to screen edge - window would shrink.
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [WINDOWS_KEY, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Spawns
    Key(
        [],
        "F1",
        lazy.spawn(f"{TERMINAL} -e /home/anmol/dotfiles/scripts/tmux_sessionizer"),
        desc="Launch terminal",
    ),
    Key([ALT_KEY], "Tab", lazy.screen.toggle_group(), desc="Toggle Group"),
    Key([WINDOWS_KEY], "t", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([WINDOWS_KEY], "f", lazy.spawn("nemo"), desc="Launch File explorer"),
    Key(
        [WINDOWS_KEY, "shift"],
        "n",
        lazy.spawn("dunstctl set-paused toggle"),
    ),
    Key(
        [WINDOWS_KEY, "shift"],
        "d",
        lazy.spawn("dunstctl close-all"),
    ),
    Key(
        [ALT_KEY, "shift"],
        "1",
        lazy.spawn(
            BROWSER + ' --profile-directory="Profile 4"',
        ),
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
    Key(
        [ALT_KEY, "shift"],
        "p",
        lazy.spawn("/home/anmol/Downloads/Postman/Postman"),
    ),
    Key(
        [ALT_KEY, "shift"],
        "a",
        lazy.spawn("/home/anmol/Applications/arduino-ide_2.3.2_Linux_64bit.AppImage"),
    ),
    Key(
        [ALT_KEY, "shift"],
        "w",
        lazy.spawn(
            "/usr/bin/python3 /home/anmol/dotfiles/scripts/wallpaper_modifier.py"
        ),
    ),
    Key(
        [ALT_KEY, "shift"],
        "n",
        lazy.spawn("/home/anmol/Applications/Obsidian-1.5.8.AppImage"),
    ),
    # Key(
    #     [ALT_KEY, "shift"],
    #     "m",
    #     lazy.spawn(
    #         browser + ' --profile-directory="Profile 2" --app=https://music.youtube.com'
    #     ),
    # ),
    # Toggle between different layouts as defined below
    Key([WINDOWS_KEY], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [WINDOWS_KEY, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"
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
    Key([WINDOWS_KEY, "shift"], "l", lazy.spawn("i3lock")),
    Key([ALT_KEY, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([WINDOWS_KEY, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([WINDOWS_KEY], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # COmmands to control stuff on laptop
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +3%"),
        desc="Raise brightness level by 3%",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 3-% "),
        desc="Lower brightness level by 3%",
    ),
    # Key([], ""),
    # Key(
    #     [WINDOWS_KEY], "n", lazy.spawn(["/bin/zsh", "-c", 'echo hello && notify-send "hello?"'])
    # ),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([ALT_KEY, "shift"], "s", lazy.spawn("flameshot gui")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    # Decrease volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    # Toggle mute
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([WINDOWS_KEY], "x", lazy.spawn("playerctl next")),
    Key([WINDOWS_KEY], "z", lazy.spawn("playerctl previous")),
    Key([WINDOWS_KEY], "space", lazy.spawn("playerctl play-pause")),
    # Key([ALT_KEY, "shift"], "w", lazy.spawn("echo Hello World!")),
    # Groups.
    Key([WINDOWS_KEY, "shift"], "w", lazy.screen.next_group(skip_empty=True)),
    Key([WINDOWS_KEY, "shift"], "s", lazy.screen.prev_group(skip_empty=True)),
    # rofi
    # Key([ALT_KEY], "tab", lazy.spawn("rofi -show window")),
    Key([WINDOWS_KEY], "r", lazy.spawn("rofi -show drun")),
    Key([WINDOWS_KEY, "shift"], "r", lazy.spawn("rofi -show run")),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", ALT_KEY],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = []

temp_groups = [*GROUPS]

for name, label, _layout, apps, matches in temp_groups:
    groups.append(
        Group(
            name=name,
            layout=_layout.lower(),
            label=label,
            spawn=apps,
            matches=matches,
        )
    )


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [WINDOWS_KEY],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [WINDOWS_KEY],
                f"KP_{KP[i.name]}",
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # WINDOWS_KEY1 + shift + letter of group = move focused window to group
            Key(
                [WINDOWS_KEY, "shift"],
                f"KP_{KP[i.name]}",
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
            Key(
                [WINDOWS_KEY, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


MARGIN = 6


widget_defaults = dict(
    font="CaskayiaCove Nerd Font",
    fontsize=FONT_SIZE,
    padding=8,
)

layouts = [*LAYOUTS]

extension_defaults = widget_defaults.copy()
screens = [
    Screen(top=custom_bar),
]

# Drag floating layouts.
mouse = [
    Drag(
        [WINDOWS_KEY],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [WINDOWS_KEY],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([WINDOWS_KEY], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = Floating(
    border_normal=nord_fox["bg"],
    border_focus=nord_fox["cyan"],
    border_width=2,
    float_rules=[
        *Floating.default_float_rules,
        Match(wm_class="pavucontrol"),
        # Match(role="pop-up"),  # gitk
        Match(wm_class="shotwell"),  # gitk
        Match(wm_class="Nemo"),  # gitk
        Match(wm_class="blueman-manager"),  # gitk
        Match(wm_class="gnome-screenshot"),  # gitk
        Match(wm_class="cinnamon-settings"),  # gitk
        Match(wm_class="cinnamon-settings calendar"),  # gitk
        Match(wm_class="cinnamon-settings network"),  # gitk
        Match(wm_class="gnome-calendar"),
        Match(wm_class="gnome-calculator"),
    ],
)
# floating_layout = # floating_layout.layout.confi
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
wmname = "LG3D"

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])
    subprocess.Popen(["dunst"])
