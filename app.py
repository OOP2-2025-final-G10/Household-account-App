from flask import Flask, render_template
from models import initialize_database, User, Category, Record
from routes import blueprints

app = Flask(__name__)

initialize_database()

current_user_id = 1
current_month = '2024-06'


for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    users = User.select()
    categories = Category.select()
    records = Record.select()

    category_percentage = calc_category_percentage(current_user_id, categories, records)
    total_income = calc_total_by_classification(current_user_id, records, is_income=True)
    total_payment = calc_total_by_classification(current_user_id, records, is_income=False)
    daily_income_payment = calc_daily_income_payment(current_user_id, records)

    return render_template(
        'index.html',
        title='ホーム',
        users=users,
        categories=categories,
        records=records,
        category_percentage=category_percentage,
    )

def calc_category_percentage(user_id, categories, records):
    """
    ユーザーごとのカテゴリ別支出（または収入）割合を計算します。

    Args:
        user_id (int): 対象ユーザーID
        categories (Iterable[Category]): 全カテゴリ
        records (Iterable[Record]): 全レコード

    Returns:
        dict[str, float]: カテゴリ名をキー、割合（%）を値とする辞書
    """
    records = records.where(Record.user == user_id)
    category_totals = {}
    total_amount = 0

    for cat in categories:
        cat_records = [
            r for r in records
            if r.category == cat
        ]

        cat_total = sum(r.price for r in cat_records)
        category_totals[cat.name] = cat_total
        total_amount += cat_total

    category_percentages = {}
    for name, amount in category_totals.items():
        category_percentages[name] = (
            (amount / total_amount) * 100 if total_amount > 0 else 0
        )

    return category_percentages

def calc_total_by_classification(user_id, records, is_income):
    """
    収入または支出の合計金額を計算します。
    
    Args:
        user_id (int): 対象ユーザーID
        records (Iterable[Record]): 全レコード
        is_income (bool): True=収入, False=支出
    
    Returns:
        int | float: 合計金額
    """
    records = records.where(
        (Record.user == user_id) &
        (Record.category.classification == is_income)
    )

    return sum(record.price for record in records)

def calc_daily_income_payment(user_id, records):
    """
    日付ごとの収入・支出を集計します。

    Args:
        user_id (int): 対象ユーザーID
        records (Iterable[Record]): 全レコード

    Returns:
        dict[date, dict]:
        {
            date: {
            'income': 金額,
            'payment': 金額
            }
        }
    """
    records = records.where(Record.user == user_id)

    daily_data = {}

    for record in records:
        day = record.date  #date型（YYYY-MM-DD）

        if day not in daily_data:
            daily_data[day] = {
                'income': 0,
                'payment': 0
            }

        if record.category.classification:
            daily_data[day]['income'] += record.price
        else:
            daily_data[day]['payment'] += record.price

    return daily_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
