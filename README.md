# <img src="https://github.com/user-attachments/assets/a2004f55-f5e2-48c5-84f8-e435f9cb5b7c" width="50" alt="GitHub Icon"> AuditLens V0.1

> A beautiful, Apple-style code auditing tool for security researchers and developers.
> Quickly manage comments, status, and project switching — for a clearer audit perspective.
<div style="text-align: center;">

[中文版](./readme-cn.md)

</div>

## 🧩 Feature Overview

### 📁 Top Menu

* **New** Create a new audit project

  > Prompt: `Choose a dir and code you want to audit`
  > Select a local directory and filter source code files by extensions (e.g., `.js`, `.py`, separated by semicolons).
  > The system recursively scans and counts lines to generate a visual audit list.

* **Select** Switch projects

  > Quickly switch between existing projects from a dropdown (stored in the `./.program/` folder)

* **Save** Save current project

  > Save current comments, status, and progress into a `.json` file for future continuation.

* **Import** Import history

  > Load previous audit sessions from `.json` files — automatically restoring comments, status, and sort order.

---

### 🔍 Code Review Panel

* Scrollable main area optimized for large projects without lag.
* Each file displays the following fields:

  * 📄 `File Path`: Click to sort.
  * 📊 `LOC`: Total lines of code. Sortable.
  * 🟢 `Status` label:

    * Gray: `Not Started`
    * Orange: `In Progress`
    * Green: `Done`
  * 💬 `Comment`: Click to open the comment editor.

#### ✍️ Comment Editor

Supports multiple comments per file:

```
| source code

| ---------> Line 21: function xxxx |                     |
| --------------------------------- | ------------------- |
| your note                         | ← collapsible markdown input |
| --------------                    |                     |
```

If no comment exists, only an “Add New” button is displayed. Clicking it brings up an input form:

* Start line number
* Source code snippet

---

### 💾 Persistent Storage

* All project data is saved locally in the `.program/` folder.
* Can be exported to `.json` (support for `.md` coming soon) for backups and sharing.

---

### 💬 Encouragements (Footer)

A motivational quote is shown at the bottom, randomly chosen on each launch. Default quotes include:

```
"Keep going, you're doing great!"
"Audit like a pro!"
```

You can import a custom `encouragements.txt` file to add more personalized messages.

---

## 🎨 Apple-Style UI Design

* Smooth scrolling
* Delicate widgets and color schemes
* Naturally fluid animations
* Beautiful icons and intuitive status colors

---

## 📦 Install Dependencies

```bash
pip install PyQt5 QScintilla
```

---

## 🚀 Launch

```bash
python main.py
```

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/1f653400-fabf-4c3f-944b-303f165bb6d9)
![image](https://github.com/user-attachments/assets/0f7f38ab-9861-4852-a69e-1d6c0736e731)

---

## 🛠️ Author / Contributions

Made with ❤️ by **AzraelNyx**
PRs and issues are welcome — let’s build the best auditing tool together!
