"""
QUANTIX // AI Stocks Backtesting & Research Station
Entry point. Run with: python main.py
"""

import sys
from PySide6 import QtWidgets, QtCore
from app.ui.main_window import MainWindow

def main():
    # High DPI scaling enabled
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("QUANTIX Backtesting Station")
    app.setOrganizationName("QuantixAI")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

