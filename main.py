from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(1200, 200, 480, 640)
        self.setWindowTitle("Notepad")
        self.grabShortcut()
        self.initUI()

    def grabShortcut(self):
        # Adding tabs to the main window using a shortcut
        self.NewTabShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+T"), self)
        self.NewTabShortcut.activated.connect(self.addTab)

        # Removing tabs from the main window using a shortcut
        self.RemoveTabShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        self.RemoveTabShortcut.activated.connect(self.removeTab)

        # Renaming tabs from the main window using a shortcut
        self.RenameTabShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.RenameTabShortcut.activated.connect(self.renameTab)

        # Saving tabs from the main window using a shortcut
        self.SaveTabShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        self.SaveTabShortcut.activated.connect(self.saveTab)

        # Opening a file from the main window using a shortcut
        self.OpenFileShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self)
        self.OpenFileShortcut.activated.connect(self.openFile)

    def initUI(self):
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu("&File")
        self.fileMenu.addAction("&New tab", self.addTab)
        self.fileMenu.addAction("&Open file", self.openFile)
        self.fileMenu.addAction("&Save tab", self.saveTab)
        self.fileMenu.addAction("&Close tab", self.removeTab)
        self.fileMenu.addAction("&Exit", self.close)

        self.editMenu = self.menuBar.addMenu("&Edit")
        self.editMenu.addAction("&Rename tab", self.renameTab)

    def addTab(self):
        self.tabs.addTab(
            QtWidgets.QTextEdit(), "New tab"  # Add a new tab with a text editor
        )

    def removeTab(self):
        if self.tabs.count() > 0:
            self.tabs.removeTab(self.tabs.currentIndex())
        else:
            QMessageBox.about(self, "Error", "There are no more tabs to close")
            sys.exit()

    def saveTab(self):
        if self.tabs.count() > 0:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save file", "", "Text files (*.txt);;All files (*.*)"
            )
            if filename:
                head_tail = os.path.split(filename)
                self.tabs.setTabText(self.tabs.currentIndex(), str(head_tail[1]))
                with open(filename, "w") as f:
                    my_text = self.tabs.currentWidget().toPlainText()
                    f.write(my_text)
        else:
            QMessageBox.about(self, "Error", "There are no tabs to save")

    def openFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "", "Text files (*.txt);;All files (*.*)"
        )
        if filename:
            with open(filename, "r") as f:
                text = f.read()
                head_tail = os.path.split(filename)
                self.tabs.addTab(QtWidgets.QTextEdit(text), head_tail[1])

    def renameTab(self):
        if self.tabs.count() > 0:
            TabName, ok = QtWidgets.QInputDialog.getText(
                self, "Rename tab", "Enter a new name for the tab:"
            )
            if TabName == "":
                QMessageBox.about(self, "Error", "The name cannot be empty")
                self.renameTab()
            else:
                self.tabs.setTabText(self.tabs.currentIndex(), str(TabName))
        else:
            QMessageBox.about(self, "Error", "There are no tabs to rename")

    def close(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
