
# 📘 AuditLens V0.1

> A beautiful, Apple-style code auditing tool for security researchers and developers.  
> 快速管理注释、状态、项目切换，还你清晰的审计视野。

![image](https://github.com/user-attachments/assets/d53cf7ef-0e35-47b3-9858-aef3a61bcb0a)


---

## 🧩 功能概览

### 📁 顶部功能栏（Top Menu）

- **New** 新建审计项目  
  > 弹窗提示：`Choose a dir and code you want to audit`  
  支持选择本地目录，并通过后缀筛选源代码文件（如 `.js`, `.py` 等，分号隔开）。系统会递归扫描并统计行数，生成可视化审计列表。

- **Select** 项目切换  
  > 从下拉框中快速切换已存在项目（保存在 `./.program/` 文件夹中）

- **Save** 项目保存  
  > 将当前注释、状态等信息保存为 `.json` 文件，后续可导入继续工作。

- **Import** 历史导入  
  > 支持从 `.json` 文件导入历史记录，自动恢复注释、状态和排序信息。

---

### 🔍 审计主界面（Code Review Panel）

- 主界面为**滚动区域**，适配大项目不卡顿。
- 每个文件显示以下字段：
  - 📄 `File Path`：支持点击排序。
  - 📊 `LOC`：总代码行数，支持点击排序。
  - 🟢 `Status` 状态标签：
    - 灰色 `Not Started`
    - 橙色 `In Progress`
    - 绿色 `Done`
  - 💬 `Comment`：点击打开注释编辑界面。

#### ✍️ 注释编辑器

支持为每个文件添加多条注释：

```

\| source code

| ---------> Line 21: function xxxx |                     |
| --------------------------------- | ------------------- |
| your note                         | ← 可折叠的 markdown 编辑框 |
| --------------                    |                     |

```

若无注释，仅显示 “Add New” 按钮，点击弹出填写框：

- 起始行号
- 源代码片段

---

### 💾 数据持久化（Persistent Storage）

- 所有项目数据存储在本地 `.program/` 文件夹中。
- 可导出为 `.json`（未来支持 `.md` 格式）供审计文档备份与共享。

---

### 💬 鼓励语句（Footer）

底部自动显示一条激励语句，每次打开随机变化，默认为：

```

"Keep going, you're doing great!"
"Audit like a pro!"

````

支持自定义导入 `encouragements.txt` 文件，提供更多正能量。

---

## 🎨 Apple 风格设计

- 平滑滚动
- 精致控件与配色
- 动画自然流畅
- 图标美观，状态颜色友好直观

---

## 📦 安装依赖

```bash
pip install PyQt5 QScintilla
````

---

## 🚀 启动

```bash
python main.py
```


## 📸 截图

![image](https://github.com/user-attachments/assets/1f653400-fabf-4c3f-944b-303f165bb6d9)

![image](https://github.com/user-attachments/assets/0f7f38ab-9861-4852-a69e-1d6c0736e731)

---

## 🛠️ 作者 / 贡献

Made with ❤️ by AzraelNyx

欢迎 PR 和 issue，一起打造最好用的审计工具。


