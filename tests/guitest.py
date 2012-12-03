from entrypoint2 import entrypoint
from mangui import wxgui


@entrypoint
def run():
    wxgui.main(
        #         'grep'
        #         'man'
        #         'python'
        'ls'
    )
