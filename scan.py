from PyQt5.QtCore import QObject, pyqtSignal
import os


class ScanWorker(QObject):
    progress = pyqtSignal(str, int)  # 相对路径, 行数
    finished = pyqtSignal(list)  # 扫描完成，返回 file list

    def __init__(self, base_dir, suffix_list):
        super().__init__()
        self.base_dir = base_dir
        self.suffix_list = suffix_list
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        results = []
        for root, _, files in os.walk(self.base_dir):
            for name in files:
                if self._cancel:
                    return
                if any(name.endswith(suf) for suf in self.suffix_list):
                    try:
                        full_path = os.path.join(root, name)
                        with open(full_path, 'r', errors='ignore') as f:
                            loc = sum(1 for _ in f)
                        rel_path = os.path.relpath(full_path, self.base_dir)
                        self.progress.emit(rel_path, loc)
                        results.append({"path": rel_path, "loc": loc, "status": "Not Started", "notes": []})
                    except Exception as e:
                        continue
        self.finished.emit(results)


