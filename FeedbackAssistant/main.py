# -*- coding: utf-8 -*-
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow

from FeedbackAssistant.assistant import Ui_FeedbackAssistant


DB = r"F:\jayden\projects\FeedbackAssistant\feedback.db"

class Assistant(Ui_FeedbackAssistant):
    def __init__(self, window):
        db = sqlite3.connect(DB)
        Ui_FeedbackAssistant.__init__(self)
        self.setupUi(window)

        self.table_hw.insertRow()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    assistant = Assistant(window)
    window.show()
    sys.exit(app.exec_())