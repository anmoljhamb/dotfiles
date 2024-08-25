from libqtile.config import Match
from libqtile.layout.bsp import Bsp
from libqtile.layout.floating import Floating
from libqtile.layout.max import Max
from libqtile.layout.stack import Stack
from libqtile.layout.xmonad import MonadTall

from theme import nord_fox

WINDOWS_KEY = "mod4"
ALT_KEY = "mod1"

FONT_SIZE = 16
ICON_SIZE = int(FONT_SIZE * 1.2)
MARGIN = 6
TERMINAL = "alacritty"
BROWSER = "google-chrome"

KP = {
    "1": "End",
    "2": "Down",
    "3": "Next",
    "4": "Left",
    "5": "Begin",
    "6": "Right",
    "7": "Home",
    "8": "Up",
    "9": "Prior",
    "0": "Insert",
}

GROUPS = [
    ["1", "", "stack", None, None],
    [
        "2",
        "",
        "stack",
        None,
        [
            Match(wm_class="zoom"),
        ],
    ],
    ["3", "󱃖", "monadtall", [TERMINAL], None],
    ["4", "󱃖", "monadtall", [TERMINAL], None],
    [
        "5",
        "󰎆",
        "stack",
        [
            "flatpak run com.spotify.Client",
        ],
        [
            Match(wm_class="spotify"),
            Match(wm_class="crx_cinhimbnkkaeohfgghhklpknlkffjgod"),
        ],
    ],
    ["6", "", "floating", None, None],
    [
        "7",
        "󰭻",
        "stack",
        None,
        [
            Match(wm_class="crx_hnpfjngllnobngcgfapefoaidbinmjnm"),
            Match(wm_class="discord"),
        ],
    ],
    [
        "8",
        "󱞁",
        "stack",
        None,
        Match(wm_class="obsidian"),
    ],
]

LAYOUTS = [
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
    Floating(
        border_normal=nord_fox["bg"],
        border_focus=nord_fox["cyan"],
        border_width=2,
        float_rules=[
            *Floating.default_float_rules,
            Match(wm_class="Nemo"),  # gitk
        ],
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
