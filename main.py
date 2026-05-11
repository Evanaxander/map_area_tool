"""
Map Area Tool - Entry point
Usage:
    python main.py                  # Open GUI with file dialog
    python main.py image.png        # Open GUI with specific image
"""

import sys
from PyQt5.QtWidgets import QApplication
from app.window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Map Area Tool")
    app.setStyle("Fusion")

    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(image_path=image_path)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
