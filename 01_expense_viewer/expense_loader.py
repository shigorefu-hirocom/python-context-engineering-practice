import pandas as pd


def load_expenses():
    # read_csv()はCSVを表形式のDataFrameとして読み込みます。
    expenses = pd.read_csv(
        "data/expenses.csv",
        encoding="utf-8",
        dtype={"金額": int},
    )

    for column in ["日付", "分類", "内容", "金額"]:
        if column not in expenses.columns:
            raise ValueError(f"CSVに「{column}」列がありません。")

    return expenses
