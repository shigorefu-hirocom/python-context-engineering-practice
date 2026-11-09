import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# 日本語フォントの設定が異なる環境でも読めるように、グラフには英語のラベルを使います。
CHART_LABELS = {
    "食費": "Food",
    "交通費": "Transport",
    "日用品": "Daily goods",
    "娯楽": "Entertainment",
}


def show_chart(parent, totals):
    labels = []
    amounts = []
    for category, amount in totals.items():
        labels.append(CHART_LABELS.get(category, f"Category {len(labels) + 1}"))
        amounts.append(amount)

    window = tk.Toplevel(parent)
    window.title("分類別の支出")
    window.geometry("640x360")

    figure = Figure(figsize=(6, 3), tight_layout=True)
    axes = figure.add_subplot(111)
    axes.bar(labels, amounts, color="#42788d")
    axes.set_ylabel("Amount (JPY)")
    axes.set_ylim(bottom=0)

    # Matplotlibで作った図をTkinterのウィンドウに表示します。
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
