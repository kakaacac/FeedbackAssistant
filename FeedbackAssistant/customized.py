# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QUndoCommand, QTabWidget, QTabBar, QMainWindow
from PyQt5.QtCore import QEvent


__all__ = ["DisplayTextChangedCommand", "InteractiveTabWidget"]

class DisplayTextChangedCommand(QUndoCommand):
    def __init__(self, display, stack):
        super().__init__()
        self.display = display
        self.stack = stack
        self.display_text = self.display.toPlainText()

    def undo(self):
        index = self.stack.index()
        pre_command = self.stack.command(index - 2)
        if pre_command:
            self.display.setText(pre_command.display_text)
        else:
            self.display.setText("")

    def redo(self):
        self.display.setText(self.display_text)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eventFilter(self, obj, event):
        if obj == self.tabBar:
            if event.type() == QEvent.MouseMove:
                index = self.tabBar.tabAt(event.pos())
                self.content.setCurrentIndex(index)
                return True
            else:
                return QTabBar.eventFilter(self.content, obj, event)
        return  QMainWindow.eventFilter(self, obj, event)



