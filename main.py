import sys
import os
import json
import random
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QPushButton, QTextEdit, QScrollArea, QComboBox,
    QGroupBox, QHBoxLayout, QToolBar, QMessageBox, QDialog, QLineEdit,
    QDialogButtonBox, QFormLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QComboBox as QComboBoxEdit, QInputDialog,
    QSplitter, QProgressDialog
)
from PyQt5.QtGui import QFont, QColor,QIcon
from PyQt5.QtCore import Qt, QTimer,QThread
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from beautify import apply_global_styles,show_with_fade,create_colored_icon
from scan import ScanWorker


ENCOURAGEMENTS = [
    "Keep going, you're doing great!",
    "Every bug you squash makes you stronger!",
    "Small progress is still progress!",
    "Audit like a pro!"
]

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUtf8(True)

        lexer = QsciLexerPython()
        lexer.setDefaultFont(QFont("Courier", 11))
        self.setLexer(lexer)

        self.setMarginsFont(QFont("Courier", 10))
        self.setMarginWidth(0, "0000")
        self.setMarginLineNumbers(0, True)

        self.setAutoIndent(True)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2a2a2a"))

        self.setPaper(QColor("#1e1e1e"))
        self.setColor(QColor("#d4d4d4"))

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Note")

        self.line_input = QLineEdit()
        self.code_input = CodeEditor()
        self.code_input.setMinimumHeight(250)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("Line number:", self.line_input)
        layout.addLayout(form)
        layout.addWidget(QLabel("Source code:"))
        layout.addWidget(self.code_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return self.line_input.text(), self.code_input.text()

class AuditLens(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AuditLensV0.1")
        self.setGeometry(100, 100, 1000, 700)

        self.project_data = {}
        self.current_project = None
        self.table_data = []

        self.sort_asc = {
            "File Path": True,
            "LOC": True
        }

        # 每页显示文件数量
        self.page_size = 20
        self.current_page = 0

        self.setWindowIcon(QIcon("icon.png"))  # 支持 .ico、.png、.svg

        self.init_ui()

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 按钮
        new_btn = QPushButton("New")
        new_btn.clicked.connect(self.new_project)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_project)
        import_btn = QPushButton("Import")
        import_btn.clicked.connect(self.import_project)

        self.project_selector = QComboBox()
        self.project_selector.setMinimumWidth(200)
        self.project_selector.currentIndexChanged.connect(self.load_selected_project)

        toolbar.addWidget(new_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(import_btn)
        toolbar.addWidget(QLabel("Project:"))
        toolbar.addWidget(self.project_selector)

        # 设置滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())

        # 表格
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["File Path", "LOC", "Status", "Comment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_table)

        container = scroll_area.widget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(self.table)

        # 设置翻页控制按钮
        pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)

        container_layout.addLayout(pagination_layout)

        self.setCentralWidget(scroll_area)

        self.statusBar().showMessage(random.choice(ENCOURAGEMENTS))

        os.makedirs(".program", exist_ok=True)
        self.load_all_projects()

    def load_selected_project(self):
        self.current_page = 0  # 重置为第一页
        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(0)
        if not self.current_project:
            return

        # 获取当前项目的文件数据
        files = self.project_data.get(self.current_project, [])
        # 计算当前页的文件数据
        start_idx = self.current_page * self.page_size
        end_idx = min((self.current_page + 1) * self.page_size, len(files))

        for row_idx in range(start_idx, end_idx):
            file = files[row_idx]
            self.table.insertRow(row_idx - start_idx)
            self.table.setItem(row_idx - start_idx, 0, QTableWidgetItem(file['path']))
            self.table.setItem(row_idx - start_idx, 1, QTableWidgetItem(str(file['loc'])))

            status_cb = QComboBoxEdit()
            status_map = {
                "Not Started": QColor("gray"),
                "In Progress": QColor("orange"),
                "Done": QColor("green")
            }
            for status, color in status_map.items():
                icon = create_colored_icon(color)
                status_cb.addItem(icon, status)

            status_cb.setCurrentText(file['status'])
            status_cb.currentTextChanged.connect(partial(self.update_status, row_idx))
            self.table.setCellWidget(row_idx - start_idx, 2, status_cb)

            comment_btn = QPushButton(f"已有注释：{len(file['notes'])}")
            comment_btn.clicked.connect(partial(self.toggle_notes, row_idx))
            self.table.setCellWidget(row_idx - start_idx, 3, comment_btn)

        # 更新翻页按钮状态
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(end_idx < len(files))

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()

    def next_page(self):
        files = self.project_data.get(self.current_project, [])
        if (self.current_page + 1) * self.page_size < len(files):
            self.current_page += 1
            self.populate_table()

    def update_status(self, row, status):
        if self.current_project:
            self.project_data[self.current_project][row]['status'] = status

    def new_project(self):
        dialog = QFileDialog.getExistingDirectory(self, "Choose code directory")
        if not dialog:
            return

        suffixes, ok = QInputDialog.getText(self, "Input suffixes", "Separate by semicolon:", text=".py;.js")
        if not ok or not suffixes:
            return

        suffix_list = [s.strip() for s in suffixes.split(';')]
        self.base_dir = dialog
        project_name = os.path.basename(dialog)

        self.progress_dialog = QProgressDialog("Scanning files...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowTitle("Scanning")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.canceled.connect(self.cancel_scan)
        self.progress_dialog.show()

        self.scan_thread = QThread()
        self.worker = ScanWorker(dialog, suffix_list)
        self.worker.moveToThread(self.scan_thread)

        self.worker.progress.connect(lambda path, loc: self.progress_dialog.setLabelText(f"Scanning: {path}"))
        self.worker.finished.connect(self.finish_scan)
        self.scan_thread.started.connect(self.worker.run)
        self.scan_thread.start()

    def cancel_scan(self):
        if hasattr(self, 'worker'):
            self.worker.cancel()
        if hasattr(self, 'scan_thread'):
            self.scan_thread.quit()
            self.scan_thread.wait()
        self.progress_dialog.close()

    def finish_scan(self, files):
        self.scan_thread.quit()
        self.scan_thread.wait()
        self.progress_dialog.close()

        project_name = os.path.basename(self.base_dir)
        self.project_data[project_name] = files
        if self.project_selector.findText(project_name) == -1:
            self.project_selector.addItem(project_name)
        self.project_selector.setCurrentText(project_name)
        self.current_project = project_name
        self.populate_table()


    def toggle_notes(self, row):
        file = self.project_data[self.current_project][row]
        notes = file['notes']

        note_dialog = QDialog(self)
        note_dialog.setWindowTitle(file['path'])
        note_dialog.resize(1000, 700)
        layout = QVBoxLayout(note_dialog)

        for note in notes:
            layout.addWidget(QLabel(f"Line {note['line']}:"))
            code_editor = CodeEditor()
            code_editor.setText(note['code'])
            code_editor.setReadOnly(True)
            code_editor.setMinimumHeight(120)
            layout.addWidget(code_editor)

            comment_edit = QTextEdit(note['comment'])
            comment_edit.setMinimumHeight(120)
            layout.addWidget(comment_edit)

        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(partial(self.add_new_note, row, note_dialog))
        layout.addWidget(add_btn)

        show_with_fade(dialog=note_dialog)
        note_dialog.exec_()

    def add_new_note(self, row, dialog):
        add = AddNoteDialog(self)
        if add.exec_() == QDialog.Accepted:
            line, code = add.get_data()
            self.project_data[self.current_project][row]['notes'].append({"line": line, "code": code, "comment": ""})
            self.populate_table()
            dialog.close()
            self.toggle_notes(row)

    def save_project(self):
        if not self.current_project:
            return
        path = os.path.join(".program", f"{self.current_project}.json")
        with open(path, 'w') as f:
            json.dump(self.project_data[self.current_project], f, indent=2)
        QMessageBox.information(self, "Saved", f"Project '{self.current_project}' saved.")

    def import_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import JSON", filter="JSON (*.json)")
        if file_path:
            name = os.path.splitext(os.path.basename(file_path))[0]
            with open(file_path, 'r') as f:
                self.project_data[name] = json.load(f)
            if self.project_selector.findText(name) == -1:
                self.project_selector.addItem(name)
            self.project_selector.setCurrentText(name)
            self.current_project = name
            self.populate_table()

    def load_all_projects(self):
        for file in os.listdir(".program"):
            if file.endswith(".json"):
                name = file[:-5]
                with open(os.path.join(".program", file), 'r') as f:
                    self.project_data[name] = json.load(f)
                if self.project_selector.findText(name) == -1:
                    self.project_selector.addItem(name)

    def sort_table(self, logicalIndex):
        if not self.current_project:
            return
        col_name = self.table.horizontalHeaderItem(logicalIndex).text()
        if col_name not in ["File Path", "LOC"]:
            return
        reverse = not self.sort_asc[col_name]
        self.sort_asc[col_name] = reverse
        self.project_data[self.current_project].sort(
            key=lambda x: x['path'] if col_name == "File Path" else x['loc'],
            reverse=reverse
        )
        self.populate_table()

    def cell_clicked(self, row, column):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_global_styles()
    win = AuditLens()
    win.show()
    sys.exit(app.exec_())
