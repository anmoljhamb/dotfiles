from libqtile.bar import Bar
from libqtile.widget.clock import Clock
from libqtile.widget.cpu import CPU
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.net import Net
from libqtile.widget.window_count import WindowCount
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

from constants import ICON_SIZE
from theme import nord_fox

custom_bar = Bar(
    [
        widget.Spacer(8, background=nord_fox["bg"]),
        GroupBox(
            disable_drag=True,
            active=nord_fox["white"],
            inactive=nord_fox["black"],
            highlight_method="line",
            block_highlight_text_color=nord_fox["magenta"],
            borderwidth=0,
            highlight_color=nord_fox["bg"],
            background=nord_fox["bg"],
            fontsize=ICON_SIZE,
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
            scale=0.5,
        ),
        widget.Spacer(
            4, background=nord_fox["red"], decorations=[PowerLineDecoration()]
        ),
        widget.Spacer(4, background=nord_fox["fg_gutter"]),
        widget.TextBox(
            "",
            background=nord_fox["fg_gutter"],
            foreground=nord_fox["white"],
            fontsize=ICON_SIZE,
        ),
        WindowCount(
            text_format="{num}",
            background=nord_fox["fg_gutter"],
            foreground=nord_fox["white"],
            show_zero=True,
            # decorations=[PowerLineDecoration(path="rounded_left")],
        ),
        widget.Spacer(
            2,
            background=nord_fox["fg_gutter"],
            decorations=[PowerLineDecoration(path="rounded_left")],
        ),
        widget.WindowName(
            width=210,
            background=nord_fox["bg"],
            foreground=nord_fox["fg"],
            decorations=[PowerLineDecoration(path="rounded_left")],
        ),
        widget.Spacer(),
        widget.Spacer(
            12,
            # background=nord_fox["black"],
            decorations=[PowerLineDecoration(path="rounded_right")],
        ),
        Clock(
            background=nord_fox["bg"],
            foreground=nord_fox["white"],
            format="     %d %b, %H:%M",
        ),
        widget.Spacer(
            12,
            background=nord_fox["bg"],
            decorations=[PowerLineDecoration(path="rounded_left")],
        ),
        widget.Spacer(),
        widget.Spacer(
            4,
            # foreground=nord_fox["bg"],
            # background=nord_fox["black"],
            decorations=[PowerLineDecoration(path="rounded_right")],
        ),
        widget.ThermalSensor(
            background=nord_fox["bg"],
            foreground=nord_fox["pink"],
        ),
        CPU(
            format="  {freq_current}GHz {load_percent:05.2f}%",
            background=nord_fox["bg"],
            foreground=nord_fox["pink"],
        ),
        Memory(
            format="  {MemUsed: .0f}{mm} {MemPercent:05.2f}%",
            background=nord_fox["bg"],
            foreground=nord_fox["cyan"],
        ),
        Net(
            format="{interface}: {down:6.2f}{down_suffix:<2}↓",
            prefix="M",
            interface="wlp3s0",
            background=nord_fox["bg"],
            foreground=nord_fox["green"],
        ),
        widget.Spacer(
            8,
            background=nord_fox["bg"],
            decorations=[PowerLineDecoration(path="rounded_right")],
        ),
        widget.Wlan(
            interface="wlp3s0",
            background=nord_fox["fg_gutter"],
            format="󰤨     {essid}   {percent:03.0%}",
            disconnected_message="󰤭",
        ),
        widget.Spacer(8, background=nord_fox["fg_gutter"]),
        widget.PulseVolume(
            emoji=True,
            emoji_list=["󰝟", "󰕿", "󰖀", "󰕾"],
            background=nord_fox["fg_gutter"],
        ),
        widget.UPowerWidget(
            fill_charge=nord_fox["green"],
            background=nord_fox["fg_gutter"],
        ),
        widget.Spacer(
            8,
            background=nord_fox["fg_gutter"],
            decorations=[PowerLineDecoration(path="rounded_left")],
        ),
        widget.Spacer(10, background=nord_fox["black"]),
        widget.QuickExit(
            countdown_start=3,
            background=nord_fox["black"],
            foreground=nord_fox["white"],
            default_text="󰿅",
            countdown_format="{}",
            fontsize=ICON_SIZE,
        ),
        widget.Spacer(16, background=nord_fox["black"]),
    ],
    background="#00000000",
    size=36,
    margin=8,
)
