import logging
import os
import subprocess

from libqtile import hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.layout.floating import Floating
from libqtile.lazy import lazy

from constants import ALT_KEY, FONT_SIZE, GROUPS, KP, LAYOUTS, WINDOWS_KEY
from custom_bar import custom_bar
from scratch_pads import scratch_pads
from shortcuts import shortcut_keys
from theme import nord_fox

logging.basicConfig(
    filename="/home/anmol/logs/qtile.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.debug("This is a debug message")


keys = [*shortcut_keys]

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

groups.extend(scratch_pads)

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
