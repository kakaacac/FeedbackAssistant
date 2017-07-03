# -*- coding: utf-8 -*-
import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QUndoStack, QTabBar
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QEvent

from assistant import Ui_FeedbackAssistant
from add_feedback import Ui_Add
from customized import DisplayTextChangedCommand, MainWindow


DB = r"feedback.db"

class Assistant(Ui_FeedbackAssistant, MainWindow):
    TABLE_TYPE_NAME_MAPPING = {
        1: "作业完成",
        2: "课内表现",
        3: "日后改进"
    }

    def __init__(self, db=DB):
        super().__init__()
        self.setupUi(self)

        self.TABLE_TYPE_OBJECT_MAPPING = {
            1: self.table_hw,
            2: self.table_pfm,
            3: self.table_ipv
        }

        self.appendStack = QUndoStack()
        self.init_db(db)
        self.setup_tables()

        # signals
        for tid, obj in self.TABLE_TYPE_OBJECT_MAPPING.items():
            obj.itemChanged.connect(self.change_content(tid, obj))
        self.table_hw.itemClicked.connect(self.append_text([self.table_ipv, self.table_pfm]))
        self.table_pfm.itemClicked.connect(self.append_text([self.table_hw, self.table_ipv]))
        self.table_ipv.itemClicked.connect(self.append_text([self.table_hw, self.table_pfm]))
        self.button_undo.clicked.connect(self.display.undo)
        self.button_redo.clicked.connect(self.display.redo)
        self.button_delete.clicked.connect(self.delete_content)
        self.button_add.clicked.connect(self.add_feedback_dialog)
        self.button_copy.clicked.connect(self.copy_to_clipboard)
        self.display.textChanged.connect(self.clear_copied_label)
        self.button_append_redo.clicked.connect(self.appendStack.redo)
        self.button_append_undo.clicked.connect(self.appendStack.undo)
        self.button_clear.clicked.connect(self.clear_text)

        self.tabBar = self.content.tabBar()
        self.tabBar.installEventFilter(self)

    def init_db(self, db=DB):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        table = self.query("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
        if len(table) == 0:
            sql = """
            CREATE TABLE feedback (
            id integer PRIMARY KEY,
            created_at text,
            updated_at text,
            content text NOT NULL,
            status integer DEFAULT 1,
            type integer NOT NULL,
            total_used integer DEFAULT 0
            )"""
            self.execute(sql)

    def execute(self, sql, *args):
        self.cur.execute(sql, args)
        self.conn.commit()

    def query(self, sql, *args):
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    def read_data(self, query=None):
        if query is None:
            query = "SELECT * FROM feedback WHERE status=1 ORDER BY created_at DESC"
        return self.query(query)

    def setup_tables(self):
        grouped_data = {tid: [] for tid in self.TABLE_TYPE_OBJECT_MAPPING}
        for row in self.read_data():
            grouped_data[row["type"]].append(row)

        self.item_mapping = {tid: [] for tid in self.TABLE_TYPE_OBJECT_MAPPING}

        for table_id, rows in grouped_data.items():
            table_obj = self.TABLE_TYPE_OBJECT_MAPPING[table_id]
            while table_obj.rowCount() > 0:
                table_obj.removeRow(0)
            table_obj.setRowCount(len(rows))

            for index, row in enumerate(rows):
                item = QTableWidgetItem(row["content"])
                table_obj.setItem(index, 0, item)
                item.setToolTip("Append text \"{}\"".format(row["content"]))
                self.item_mapping[table_id].append(row["id"])

    def change_content(self, tid, obj):
        def callback(item):
            row_id = self.item_mapping[tid][item.row()]
            content = str(item.text())
            sql = "UPDATE feedback SET content=?, updated_at=? WHERE id={}".format(row_id)
            self.execute(sql, content, now())

        return callback

    def get_selected_item(self):
        for table_id, table in self.TABLE_TYPE_OBJECT_MAPPING.items():
            selected = table.selectedItems()
            if len(selected) > 0:
                return table_id, selected[0]
        return None, None

    def append_all_text(self):
        _, item = self.get_selected_item()
        if item:
            text = item.text()
            self.display.setText(self.display.toPlainText() + text)

            command = DisplayTextChangedCommand(self.display, self.appendStack)
            self.appendStack.push(command)

    def clear_text(self):
        self.display.setText("")
        command = DisplayTextChangedCommand(self.display, self.appendStack)
        self.appendStack.push(command)

    def append_text(self, clear_tables):
        def callback(item):
            for obj in clear_tables:
                obj.clearSelection()

            text = item.text()
            self.display.setText(self.display.toPlainText() + text)
            command = DisplayTextChangedCommand(self.display, self.appendStack)
            self.appendStack.push(command)

        return callback

    def delete_content(self):
        table_id, item = self.get_selected_item()
        if item:
            question = "Are you sure you want to delete \"{}\"?".format(item.text())
            reply = QMessageBox.question(self.button_delete, "FeedbackAssistant", question,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                row_id = self.item_mapping[table_id][item.row()]
                sql = "DELETE FROM feedback WHERE id={}".format(row_id)
                self.execute(sql)

                self.item_mapping[table_id].pop(item.row())

                table = item.tableWidget()
                table.removeRow(item.row())

    def add_feedback_dialog(self):
        dialog = QDialog()
        add_feedback = AddFeedback(dialog, self)
        dialog.show()
        dialog.exec_()

    def copy_to_clipboard(self):
        text = self.display.toPlainText()
        if len(text) > 0:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
            self.label_copy.setText("Copyied!")

    def clear_copied_label(self):
        if self.label_copy.text():
            self.label_copy.setText("")

    def eventFilter(self, obj, event):
        if obj == self.tabBar:
            if event.type() == QEvent.HoverMove:
                index = self.tabBar.tabAt(event.pos())
                self.content.setCurrentIndex(index)
                return True
            else:
                return QTabBar.eventFilter(self, obj, event)
        return  QMainWindow.eventFilter(self, obj, event)


class AddFeedback(Ui_Add):
    INDEX_TABLE_MAPPING = {
        0: 1,
        1: 2,
        2: 3
    }

    def __init__(self, dialog, mainWindow):
        super().__init__()
        self.setupUi(dialog)
        self.mainWindow = mainWindow

        # signals
        self.confirm.accepted.connect(self.add_feedback)

    def add_feedback(self):
        index = self.type_select.currentIndex()
        table_id = self.INDEX_TABLE_MAPPING[index]
        content = self.content.toPlainText()
        if len(content) > 0:
            t = now()
            sql = "INSERT INTO feedback (created_at, updated_at, content, type) values (?, ?, ?, ?)"
            self.mainWindow.execute(sql, t, t, content, table_id)
            self.mainWindow.item_mapping[table_id].insert(0, self.mainWindow.cur.lastrowid)

            table = self.mainWindow.TABLE_TYPE_OBJECT_MAPPING[table_id]
            table.insertRow(0)
            table.setItem(0, 0, QTableWidgetItem(content))


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = Assistant()
    assistant.show()
    sys.exit(app.exec_())