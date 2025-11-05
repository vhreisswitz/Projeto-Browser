import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from .main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Infinity Browser Dark")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("InfinityBrowser")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(106, 90, 205))
    dark_palette.setColor(QPalette.Highlight, QColor(106, 90, 205))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())