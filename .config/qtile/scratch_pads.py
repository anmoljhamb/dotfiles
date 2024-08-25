from libqtile.config import DropDown, ScratchPad

from utils import calc_center

scratch_pads = [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "file_manager",
                "nemo",
                x=calc_center(0.4),
                width=0.6,
                height=0.6,
                opacity=0.9,
                on_focus_lost_hide=False,
            ),
        ],
    ),
]
