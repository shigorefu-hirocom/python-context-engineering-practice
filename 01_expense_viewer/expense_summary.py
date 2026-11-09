def get_categories(expenses):
    categories = []
    for category in expenses["分類"].tolist():
        if category not in categories:
            categories.append(category)
    return categories


def filter_expenses(expenses, category):
    if category == "すべて":
        return expenses

    # 分類が一致する行だけを取り出します。
    return expenses[expenses["分類"] == category]


def total_amount(expenses):
    return expenses["金額"].sum()


def totals_by_category(expenses):
    totals = {}

    # recordsを指定すると、各行が辞書になったリストを取得できます。
    for row in expenses.to_dict("records"):
        category = row["分類"]
        if category not in totals:
            totals[category] = 0
        totals[category] += row["金額"]

    return totals
