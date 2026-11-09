import tkinter as tk
from tkinter import messagebox, ttk

from chart import show_chart
from expense_summary import (
    filter_expenses,
    get_categories,
    total_amount,
    totals_by_category,
)


def create_window(root, expenses):
    root.title("支出ビューア")
    root.geometry("760x440")
    root.minsize(600, 340)

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="支出一覧").pack(anchor="w", pady=(0, 8))

    controls = ttk.Frame(frame)
    controls.pack(fill="x", pady=(0, 8))
    ttk.Label(controls, text="分類").pack(side="left")
    category = tk.StringVar(master=root, value="すべて")
    selector = ttk.Combobox(
        controls,
        textvariable=category,
        values=["すべて"] + get_categories(expenses),
        state="readonly",
        width=14,
    )
    selector.pack(side="left", padx=8)

    table_frame = ttk.Frame(frame)
    table_frame.pack(fill="both", expand=True)

    # Treeviewの見出しと列を使って一覧を表として表示します。
    columns = ["日付", "分類", "内容", "金額"]
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    widths = [110, 100, 250, 100]
    for index in range(len(columns)):
        column = columns[index]
        table.heading(column, text=column)
        table.column(column, width=widths[index])
    table.column("金額", anchor="e")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side="left", fill="both", expand=True)

    status = tk.StringVar(master=root)
    ttk.Label(frame, textvariable=status).pack(anchor="w", pady=(8, 0))

    # 分類を選んだときはイベントが渡されます。起動時は引数なしで呼びます。
    def refresh_table(event=None):
        selected = filter_expenses(expenses, category.get())
        for row_id in table.get_children():
            table.delete(row_id)

        for row in selected.to_dict("records"):
            table.insert(
                "",
                "end",
                values=(row["日付"], row["分類"], row["内容"], f'{row["金額"]:,} 円'),
            )

        status.set(f"{len(selected)} 件    合計 {total_amount(selected):,} 円")

    def open_chart():
        selected = filter_expenses(expenses, category.get())
        if len(selected) == 0:
            messagebox.showinfo("支出グラフ", "表示するデータがありません。", parent=root)
            return

        show_chart(root, totals_by_category(selected))

    selector.bind("<<ComboboxSelected>>", refresh_table)
    ttk.Button(controls, text="グラフを表示", command=open_chart).pack(side="left")
    refresh_table()
