from libqtile.config import DropDown, ScratchPad

from constants import BROWSER, TERMINAL
from utils import calc_center

scratch_pads = [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "file_manager",
                "nemo",
                x=calc_center(0.6),
                width=0.6,
                height=0.6,
                opacity=0.9,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "terminal",
                TERMINAL,
                x=calc_center(0.7),
                y=calc_center(0.7),
                width=0.7,
                height=0.7,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "chatgpt",
                f"{BROWSER} -app=https://chat.openai.com --user-data-dir=.config/chromium/scratchpad-chatgpt",
                x=calc_center(0.7),
                y=calc_center(0.7),
                width=0.7,
                height=0.7,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "ytmusic",
                f"{BROWSER} -app=https://music.youtube.com --user-data-dir=.config/chromium/scratchpad-ytmusic",
                x=calc_center(0.7),
                y=calc_center(0.7),
                width=0.7,
                height=0.7,
                opacity=1,
                on_focus_lost_hide=False,
            ),
        ],
    ),
]
