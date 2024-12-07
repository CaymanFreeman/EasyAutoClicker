import multiprocessing
import sys

import pyautogui
from PyQt5.QtWidgets import QApplication

from gui.window_logic import AppWindow


def main():
    pyautogui.MINIMUM_DURATION = 0.0
    pyautogui.PAUSE = 0.0
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()
    main()
