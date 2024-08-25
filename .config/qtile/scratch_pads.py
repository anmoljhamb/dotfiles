from libqtile.config import DropDown, ScratchPad

scratch_pads = [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "file_manager",
                "nemo",
                x=0.1,
                width=0.6,
                height=0.6,
                opacity=0.9,
                on_focus_lost_hide=False,
            ),
        ],
    ),
]
