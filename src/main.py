# TO-DO



from gui import GUI
from fun import FUN

class VerbosityMeter(GUI, FUN):
    def __init__(self) -> None:
        super().__init__()
        FUN.__init__(self)


if __name__ == "__main__":
    ROOT = VerbosityMeter()
    ROOT.WINDOW.mainloop()
