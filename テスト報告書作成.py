import tkinter as tk
from tkinter import filedialog, ttk

def select_file(entry):
    filename = filedialog.askopenfilename()
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def select_folder(entry):
    foldername = filedialog.askdirectory()
    if foldername:
        entry.delete(0, tk.END)
        entry.insert(0, foldername)

def update_acp_options(event):
    selected_category = acp_category.get()
    acp_combobox['values'] = acp_options[selected_category]
    acp_combobox.set('')

root = tk.Tk()
root.title("報告書作成フォーム")

# Section 1: File selection
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

labels = ["IPO ファイル", "テスト報告書フォマード", "成果物格納"]
entries = []

for i, label_text in enumerate(labels):
    row = tk.Frame(file_frame)
    row.pack(fill="x", pady=2)
    label = tk.Label(row, text=label_text, width=20, anchor='w')
    label.pack(side="left")
    entry = tk.Entry(row, width=50)
    entry.pack(side="left", padx=5)
    entries.append(entry)
    if label_text == "成果物格納":
        button = tk.Button(row, text="選択", command=lambda e=entry: select_folder(e))
    else:
        button = tk.Button(row, text="選択", command=lambda e=entry: select_file(e))
    button.pack(side="left")

# Section 2: リスト with dropdowns
list_frame = tk.LabelFrame(root, text="リスト")
list_frame.pack(fill="x", padx=10, pady=10)

tk.Label(list_frame, text="カテゴリ選択:", anchor='w').pack(fill="x", padx=10, pady=2)

acp_category = ttk.Combobox(list_frame, values=["バッチACP", "部品", "オンラインACP"], state="readonly")
acp_category.pack(fill="x", padx=10)
acp_category.bind("<<ComboboxSelected>>", update_acp_options)

tk.Label(list_frame, text="コード選択:", anchor='w').pack(fill="x", padx=10, pady=2)

acp_options = {
    "バッチACP": ["UZ0Q01", "UZ0Q06", "UZ0Q07"],
    "部品": ["UZ8K01", "UZ2B01"],
    "オンラインACP": ["UZ0C01", "UZ0C03", "UZ0C09", "UZ0C10"]
}

acp_combobox = ttk.Combobox(list_frame, state="readonly")
acp_combobox.pack(fill="x", padx=10)

# Section 3: Report creation button
tk.Button(root, text="報告書作成", width=20).pack(pady=10)

# Section 4: テスト報告書情報入力
info_frame = tk.LabelFrame(root, text="テスト報告書情報入力")
info_frame.pack(fill="x", padx=10, pady=10)

info_labels = ["VER", "最終承認者", "会社略称", "担当者", "担当者所属", "新規作成日"]
for label_text in info_labels:
    row = tk.Frame(info_frame)
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label_text, width=15, anchor='w').pack(side="left")
    tk.Entry(row, width=50).pack(side="left", padx=5)

root.mainloop()

