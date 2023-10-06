# TO-DO
#     Improve GUI (
#         Theme Switch
#         About page
#     )
#     Error notification (
#
#     )
#     User input RegEx (
#
#     )
#
#     TO-DO
#     TO-DO
#     TO-DO
#     TO-DO

from gui import GUI
from fun import FUN

class VerbosityMeter(GUI, FUN):
    def __init__(self) -> None:
        super().__init__()

if __name__ == "__main__":
    ROOT = VerbosityMeter()
    ROOT.WINDOW.mainloop()
