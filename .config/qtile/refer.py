# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.swap_left().when(layout="monadtall"),
        lazy.layout.shuffle_left().when(layout="columns"),
        desc="Move window to the left",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.swap_right().when(layout="monadtall"),
        lazy.layout.shuffle_right().when(layout="columns"),
        desc="Move window to the left",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    # MonadTall growing stuff
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "o", lazy.layout.maximize().when(layout="monadtall")),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "r", lazy.layout.reset().when(layout="monadtall")),
    Key([mod, "shift"], "space", lazy.layout.flip().when(layout="monadtall")),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(["control", "mod1"], "t", lazy.spawn(terminal)),
    # Toggle between different layouts as defined below
    Key(
        [mod],
        "Tab",
        lazy.next_layout(),
        lazy.widget["layout_icon"].update("").when(layout="max"),
        lazy.widget["layout_icon"].update("").when(layout="monadtall"),
    ),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key chords
    KeyChord(
        [mod],
        "r",
        [
            Key([], "f", lazy.spawn("firefox")),
            Key([], "i", lazy.spawn("idea.sh")),
            Key([], "e", lazy.spawn("nautilus")),
            Key([], "o", lazy.spawncmd("Run")),
        ],
        name="Run",
    ),
    KeyChord(
        [mod],
        "p",
        [
            Key([], "s", lazy.spawn("shutdown -h now")),
            Key([], "l", lazy.spawn("qshell:self.qtile.shutdown()")),
        ],
        name="Power",
    ),
    # Brightness / Volume
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl s 10%-"),
        lazy.spawn("notify-send -u low 'Brightness -10%'"),
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl s 10%+"),
        lazy.spawn("notify-send -u low 'Brightness +10%'"),
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.widget["volume"].mute(),
        lazy.spawn("notify-send -u low 'Volume toggled'"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.widget["volume"].decrease_vol(),
        lazy.spawn("notify-send -u low 'Volume decreased'"),
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.widget["volume"].increase_vol(),
        lazy.spawn("notify-send -u low 'Volume increased'"),
    ),
    # Toggle WidgetBox containing controls / taskbar / system monitor
    Key([mod], "c", lazy.widget["controls"].toggle()),
    Key([mod], "b", lazy.widget["taskbar"].toggle()),
    Key([mod], "g", lazy.widget["graphs"].toggle()),
    # Screenshot
    Key(
        [],
        "F2",
        lazy.spawn(
            "scrot '%d-%m-%Y-%H-%M-%S_$wx$h.png' -e 'mv $f ~/Pictures/Screenshots/'"
        ),
        lazy.spawn(
            "notify-send -u low 'Screenshot taken!' 'Saved in ~/Pictures/Screenshots/'"
        ),
    ),
]

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

highlight_color = "#bc9171"
highlight_color = "#8da3a6"
controls_width = 40
window_margin = 8
spacer_width = 13

layouts = [
    layout.MonadTall(
        border_focus=highlight_color,
        border_width=2,
        change_ratio=0.04,
        margin=window_margin,
    ),
    layout.Max(
        border_focus=highlight_color,
        border_width=2,
        margin=window_margin,
    ),
]

widget_background = "#324e52"

decor_groups = {
    "decorations": [
        RectDecoration(
            colour=widget_background,
            filled=True,
            radius=10,
            group=True,
        )
    ],
    "padding": 9,
}

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font Mono",
    fontsize=15,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="~/Pictures/Wallpapers/mountains.png",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                widget.TextBox("", fontsize=30, name="layout_icon", **decor_groups),
                widget.Spacer(spacer_width),
                widget.Spacer(7, **decor_groups),
                widget.GroupBox(
                    borderwidth=3,
                    highlight_color=["#5b6b69", "#4e6361"],
                    highlight_method="line",
                    inactive="#AAAAAA",
                    this_current_screen_border=highlight_color,
                    **decor_groups,
                    padding_x=5,
                ),
                widget.Spacer(7, **decor_groups),
                widget.Spacer(spacer_width),
                widget.WidgetBox(
                    widgets=[
                        widget.LaunchBar(
                            progs=[
                                (
                                    "/snap/firefox/3358/default256.png",
                                    "firefox",
                                    "Firefox",
                                ),
                                (
                                    "/usr/share/code/resources/app/resources/linux/code.png",
                                    "code",
                                    "VS Code",
                                ),
                                (
                                    "/opt/idea-IC-232.10072.27/bin/idea.png",
                                    "idea.sh",
                                    "IntelliJ IDEA",
                                ),
                            ],
                            **decor_groups,
                            padding_x=12,
                            padding_y=-1,
                            icon_size=25,
                        ),
                        widget.Sep(
                            padding_x=5,
                            foreground=highlight_color,
                            linewidth=2,
                            **decor_groups,
                        ),
                        widget.LaunchBar(
                            progs=[
                                (
                                    "~/Pictures/icons/BW/system-shutdown.png",
                                    "shutdown -h now",
                                    "Shut down",
                                ),
                                (
                                    "~/Pictures/icons/BW/system-reboot.png",
                                    "reboot",
                                    "Reboot",
                                ),
                                (
                                    "~/Pictures/icons/BW/system-log-out.png",
                                    "qshell:self.qtile.shutdown()",
                                    "Log out",
                                ),
                            ],
                            **decor_groups,
                            padding_x=12,
                            padding_y=-2,
                            icon_size=25,
                        ),
                        widget.Sep(
                            padding_x=5,
                            foreground=highlight_color,
                            linewidth=2,
                            **decor_groups,
                        ),
                        widget.Systray(
                            icon_size=22, background="#000000", **decor_groups
                        ),
                        widget.Spacer(9, **decor_groups),
                        widget.Spacer(spacer_width),
                    ],
                    close_button_location="left",
                    text_closed="󰏌",
                    text_open="󰅘",
                    fontsize=30,
                    name="taskbar",
                    **decor_groups,
                ),
                widget.Spacer(spacer_width),
                widget.WindowName(
                    max_chars=20,
                    **decor_groups,
                    width=210,
                    empty_group_string="󰍹 Desktop",
                ),
                widget.Spacer(),
                widget.Chord(**decor_groups),
                widget.Prompt(**decor_groups),
                widget.Spacer(spacer_width),
                widget.WidgetBox(
                    widgets=[
                        widget.TextBox("󰻠", fontsize=30, **decor_groups),
                        widget.CPUGraph(
                            border_color=highlight_color,
                            border_width=1,
                            line_width=2,
                            graph_color=highlight_color,
                            line_color=highlight_color,
                            fill_color=highlight_color + ".6",
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.TextBox("󰍛", fontsize=30, **decor_groups),
                        widget.MemoryGraph(
                            border_color=highlight_color,
                            border_width=1,
                            line_width=2,
                            graph_color=highlight_color,
                            line_color=highlight_color,
                            fill_color=highlight_color + ".6",
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.TextBox("󰛶", fontsize=30, **decor_groups),
                        widget.NetGraph(
                            border_color=highlight_color,
                            border_width=1,
                            line_width=2,
                            graph_color=highlight_color,
                            line_color=highlight_color,
                            bandwidth_type="up",
                            fill_color=highlight_color + ".6",
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.TextBox("󰛴", fontsize=30, **decor_groups),
                        widget.NetGraph(
                            border_color=highlight_color,
                            border_width=1,
                            line_width=2,
                            graph_color=highlight_color,
                            line_color=highlight_color,
                            bandwidth_type="down",
                            fill_color=highlight_color + ".6",
                            **decor_groups,
                        ),
                    ],
                    close_button_location="right",
                    text_closed="󱕎",
                    text_open="󰅘",
                    fontsize=30,
                    name="graphs",
                    **decor_groups,
                ),
                widget.Spacer(spacer_width),
                widget.WidgetBox(
                    widgets=[
                        widget.TextBox(
                            "",
                            fontsize=28,
                            name="wifi-text",
                            **decor_groups,
                        ),
                        widget.Spacer(-5, **decor_groups),
                        widget.Wlan(
                            interface="wlp58s0",
                            format="{percent:2.0%} {essid}",
                            max_chars=10,
                            update_interval=20,
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.Volume(
                            emoji=True,
                            emoji_list=["󰸈", "", "", ""],
                            fontsize=25,
                            step=10,
                            update_interval=0.1,
                            **decor_groups,
                        ),
                        widget.Spacer(-5, **decor_groups),
                        widget.GenPollCommand(
                            width=controls_width + 15,
                            cmd="amixer sget Master | egrep '\[[0-9]{1,3}%\]' | awk -F'\[|\]' '{print $2}'",
                            shell=True,
                            update_interval=0.1,
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.TextBox(
                            "󰃠", fontsize=25, name="backlight-text", **decor_groups
                        ),
                        widget.Spacer(-5, **decor_groups),
                        widget.Backlight(
                            width=controls_width + 15,
                            backlight_name="intel_backlight",
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.Battery(
                            width=controls_width + 32,
                            unknown_char="󰂑",
                            charge_char="󰂏",
                            discharge_char="󰂌",
                            full_char="󱈑",
                            format="{char} {percent:2.0%}",
                            show_short_text=False,
                            low_percentage=0.25,
                            notify_below=25,
                            update_interval=20,
                            **decor_groups,
                        ),
                        widget.Spacer(spacer_width, **decor_groups),
                        widget.TextBox(
                            "󰢑", fontsize=25, name="temp-text", **decor_groups
                        ),
                        widget.Spacer(-5, **decor_groups),
                        widget.ThermalSensor(update_interval=20, **decor_groups),
                        widget.Spacer(5, **decor_groups),
                    ],
                    close_button_location="right",
                    text_closed="󰧭",
                    text_open="󰅘",
                    fontsize=30,
                    name="controls",
                    start_opened=True,
                    **decor_groups,
                ),
                widget.Spacer(spacer_width),
                widget.Clock(format="%a %d.%m.%y %H:%M", **decor_groups),
            ],
            38,
            background="#00000000",
            margin=[0, window_margin, window_margin, window_margin],
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
