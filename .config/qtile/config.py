import os
import subprocess
from typing import Optional

from libqtile import hook, qtile
from libqtile.bar import Bar
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.layout.bsp import Bsp
from libqtile.layout.floating import Floating
from libqtile.layout.max import Max
from libqtile.layout.stack import Stack
from libqtile.layout.xmonad import MonadTall
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget.clock import Clock
from libqtile.widget.cpu import CPU
from libqtile.widget.currentlayout import CurrentLayout
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.net import Net
from libqtile.widget.systray import Systray
from libqtile.widget.textbox import TextBox
from libqtile.widget.window_count import WindowCount
from libqtile.widget.windowname import WindowName
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

MOD = "mod4"
terminal = guess_terminal()


nord_fox = {
    "bg": "#2e3440",
    "fg": "#b9bfca",
    "fg_gutter": "#4b5668",
    "black": "#3b4252",
    "red": "#bf616a",
    "green": "#a3be8c",
    "yellow": "#ebcb8b",
    "blue": "#81a1c1",
    "magenta": "#b48ead",
    "cyan": "#88c0d0",
    "white": "#e5e9f0",
    "orange": "#c9826b",
    "pink": "#bf88bc",
}

gruvbox = {
    "bg": "#282828",
    "fg": "#d4be98",
    "dark-red": "#ea6962",
    "red": "#ea6962",
    "dark-green": "#a9b665",
    "green": "#a9b665",
    "dark-yellow": "#e78a4e",
    "yellow": "#d8a657",
    "dark-blue": "#7daea3",
    "blue": "#7daea3",
    "dark-magenta": "#d3869b",
    "magenta": "#d3869b",
    "dark-cyan": "#89b482",
    "cyan": "#89b482",
    "dark-gray": "#665c54",
    "gray": "#928374",
    "fg4": "#766f64",
    "fg3": "#665c54",
    "fg2": "#504945",
    "fg1": "#3c3836",
    "bg0": "#32302f",
    "fg0": "#1d2021",
    "fg9": "#ebdbb2",
}


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
        [MOD],
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
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Spawns
    Key([MOD], "t", lazy.spawn(terminal), desc="Launch terminal"),
    Key([MOD], "f", lazy.spawn("nautilus"), desc="Launch File explorer"),
    Key(
        ["mod1", "shift"], "1", lazy.spawn("google-chrome --profile-directory=Default")
    ),
    Key(
        ["mod1", "shift"],
        "2",
        lazy.spawn('google-chrome --profile-directory="Profile 3"'),
    ),
    Key(
        ["mod1", "shift"],
        "3",
        lazy.spawn('google-chrome --profile-directory="Profile 2"'),
    ),
    Key(["mod1", "shift"], "s", lazy.spawn("flatpak run com.spotify.Client")),
    Key(
        ["mod1", "shift"],
        "m",
        lazy.spawn('google-chrome --profile-directory="Profile 2" music.youtube.com'),
    ),
    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([MOD, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),
    Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [MOD],
        "m",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    # Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key(["mod1", "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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
    # Key(
    #     [MOD], "n", lazy.spawn(["/bin/zsh", "-c", 'echo hello && notify-send "hello?"'])
    # ),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    # Decrease volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    # Toggle mute
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([MOD], "x", lazy.spawn("playerctl next")),
    Key([MOD], "z", lazy.spawn("playerctl previous")),
    Key([MOD], "space", lazy.spawn("playerctl play-pause")),
    # Key(["mod1", "shift"], "w", lazy.spawn("echo Hello World!")),
    # Groups.
    Key([MOD, "shift"], "w", lazy.screen.next_group(skip_empty=True)),
    Key([MOD, "shift"], "s", lazy.screen.prev_group(skip_empty=True)),
    # rofi
    Key(["mod1"], "tab", lazy.spawn("rofi -show window")),
    Key([MOD], "r", lazy.spawn("rofi -show drun")),
    Key([MOD, "shift"], "r", lazy.spawn("rofi -show run")),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = []

temp_groups = [
    ["1", "", "stack"],
    ["2", "󱃖", "monadtall"],
    ["3", "󱃖", "bsp"],
    ["4", "", "floating"],
    ["5", "󰎆", "stack"],
]

for name, label, _layout in temp_groups:
    groups.append(
        Group(
            name=name,
            layout=_layout.lower(),
            label=label,
        )
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # MOD1 + shift + letter of group = move focused window to group
            Key(
                [MOD, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


MARGIN = 6

layouts = [
    Stack(
        num_stacks=1,
        border_normal=nord_fox["black"],
        border_focus=nord_fox["cyan"],
        border_width=2,
        margin=MARGIN,
    ),
    Bsp(
        border_normal=nord_fox["black"],
        border_focus=nord_fox["cyan"],
        border_width=2,
        margin=MARGIN,
    ),
    Max(
        border_normal=nord_fox["black"],
        border_focus=nord_fox["cyan"],
        border_width=2,
        margin=MARGIN,
    ),
    MonadTall(
        ratio=0.72,
        border_normal=nord_fox["black"],
        border_focus=nord_fox["cyan"],
        margin=MARGIN,
        border_width=2,
        single_border_width=2,
        single_margin=MARGIN,
    ),
]

font_size = 16

widget_defaults = dict(
    font="CaskayiaCove Nerd Font",
    fontsize=font_size,
    padding=8,
)
extension_defaults = widget_defaults.copy()

icon_size = int(font_size * 1.2)

screens = [
    Screen(
        top=Bar(
            [
                GroupBox(
                    disable_drag=True,
                    active=nord_fox["white"],
                    inactive=nord_fox["black"],
                    highlight_method="line",
                    block_highlight_text_color=nord_fox["magenta"],
                    borderwidth=0,
                    highlight_color=nord_fox["bg"],
                    background=nord_fox["bg"],
                    fontsize=icon_size,
                    spacing=2,
                ),
                widget.Spacer(
                    8,
                    background=nord_fox["bg"],
                    decorations=[
                        PowerLineDecoration(path="rounded_right"),
                    ],
                ),
                widget.CurrentLayoutIcon(
                    background=nord_fox["red"],
                    foreground=nord_fox["white"],
                    margin=10,
                    scale=0.6,
                ),
                widget.Spacer(
                    4, background=nord_fox["red"], decorations=[PowerLineDecoration()]
                ),
                widget.TextBox(
                    "",
                    background=nord_fox["fg_gutter"],
                    foreground=nord_fox["white"],
                    fontsize=icon_size,
                ),
                WindowCount(
                    text_format="{num}",
                    background=nord_fox["fg_gutter"],
                    foreground=nord_fox["white"],
                    show_zero=True,
                    decorations=[PowerLineDecoration(path="rounded_left")],
                ),
                WindowName(background=nord_fox["bg"], foreground=nord_fox["fg"]),
                widget.Spacer(
                    4,
                    background=nord_fox["bg"],
                    decorations=[PowerLineDecoration(path="rounded_right")],
                ),
                widget.ThermalSensor(
                    background=nord_fox["black"],
                    foreground=nord_fox["pink"],
                ),
                CPU(
                    format="  {freq_current}GHz {load_percent:05.2f}%",
                    background=nord_fox["black"],
                    foreground=nord_fox["pink"],
                ),
                Memory(
                    format="  {MemUsed: .0f}{mm} {MemPercent:05.2f}%",
                    background=nord_fox["black"],
                    foreground=nord_fox["cyan"],
                ),
                Net(
                    format="{interface}: {down:6.2f}{down_suffix:<2}↓",
                    prefix="M",
                    interface="wlp3s0",
                    background=nord_fox["black"],
                    foreground=nord_fox["green"],
                ),
                left_half_circle(nord_fox["fg_gutter"], nord_fox["black"]),
                Systray(background=nord_fox["fg_gutter"]),
                right_half_circle(nord_fox["fg_gutter"], nord_fox["black"]),
                Clock(
                    background=nord_fox["black"],
                    foreground=nord_fox["white"],
                    format="     %Y-%m-%d %a %I:%M %p",
                ),
                widget.QuickExit(
                    background=nord_fox["black"],
                    foreground=nord_fox["white"],
                    default_text="󰿅  ",
                    countdown_format="{} ",
                ),
            ],
            # background=nord_fox['bg'],
            size=36,
            margin=8,
        )
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [MOD],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
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
        Match(wm_class="nitrogen"),  # gitk
    ],
)
# floating_layout.layout.confi
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])
    subprocess.Popen(["dunst"])
