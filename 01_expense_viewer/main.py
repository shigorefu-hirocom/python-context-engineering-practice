import tkinter as tk

from expense_loader import load_expenses
from window import create_window


def main():
    try:
        expenses = load_expenses()
    except (OSError, ValueError) as error:
        print(f"支出データを読み込めませんでした。{error}")
        return

    root = tk.Tk()
    create_window(root, expenses)
    root.mainloop()


if __name__ == "__main__":
    main()
