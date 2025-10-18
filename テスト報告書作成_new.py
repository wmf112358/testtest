import tkinter as tk

root = tk.Tk()
root.title("Ita仕様書自動作成")
root.geometry("800x400")
root.configure(bg="white")

selected_index = tk.IntVar(value=0)
nav_buttons_text = ["基本情報入力", "PGMパターン選択", "テストケース編集"]
font_style = ("ＭＳ ゴシック", 10)

def create_navbar(parent, selected_index):
    nav_frame = tk.Frame(parent, width=180, bg="#0078D7")
    nav_frame.pack(side="left", fill="y")
    for i, text in enumerate(nav_buttons_text):
        bg_color = "#005A9E" if selected_index.get() == i else "#0078D7"
        btn = tk.Button(nav_frame, text=text, bg=bg_color, fg="white", relief="flat",
                        font=font_style, anchor="w", padx=20)
        btn.pack(fill="x", pady=5)

def show_screen1():
    for widget in root.winfo_children():
        widget.destroy()
    selected_index.set(0)
    create_navbar(root, selected_index)
    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.pack(side="left", fill="both", expand=True)
    tk.Label(main_frame, text="基本情報", font=("ＭＳ ゴシック", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 20))
    fields = ["担当者", "最終更新者", "最終承認者"]
    for i, field in enumerate(fields):
        tk.Label(main_frame, text=field, bg="white", anchor="e", width=12, font=font_style).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(main_frame, width=25, font=font_style).grid(row=i+1, column=1, padx=5, pady=5)
        tk.Label(main_frame, text="会社略称", bg="white", anchor="e", width=12, font=font_style).grid(row=i+1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(main_frame, width=25, font=font_style).grid(row=i+1, column=3, padx=5, pady=5)
    tk.Button(main_frame, text="次へ", width=10, bg="#0078D7", fg="white", font=font_style, command=show_screen2).grid(row=5, column=3, sticky="e", pady=30)

def show_screen2():
    for widget in root.winfo_children():
        widget.destroy()
    selected_index.set(1)
    create_navbar(root, selected_index)
    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.pack(side="left", fill="both", expand=True)
    tk.Button(main_frame, text="<< 戻る", bg="#0078D7", fg="white", font=font_style, command=show_screen1).grid(row=0, column=3, sticky="e", pady=(0, 10))
    categories = {
        "ACP": ["パッチ", "オンライン"],
        "部品": ["共通部品", "業務部品"],
        "DBI": ["参照", "参照"]
    }
    for i, (category, buttons) in enumerate(categories.items()):
        tk.Label(main_frame, text=category, font=("ＭＳ ゴシック", 12, "bold"), bg="white").grid(row=i+1, column=0, sticky="w", pady=10)
        for j, btn_text in enumerate(buttons):
            tk.Button(main_frame, text=btn_text, width=12, font=font_style).grid(row=i+1, column=j+1, padx=10)

show_screen1()
root.mainloop()
