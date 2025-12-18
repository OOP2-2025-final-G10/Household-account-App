import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request
from models import initialize_database, User, Category, Record
from routes import blueprints
from calendar import monthrange

app = Flask(__name__)

initialize_database()

current_user_id = 1
current_month = '2025-12'


for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    month = request.args.get('month', current_month)

    users = User.select()
    categories = Category.select()
    records = Record.select()

    month_records = filter_records_by_month(current_user_id, records, month)

    category_percentage_income = calc_category_percentage(current_user_id, categories, month_records, is_income=True)
    category_percentage_payment = calc_category_percentage(current_user_id, categories, month_records, is_income=False)
    total_income = calc_total_by_classification(current_user_id, month_records, is_income=True)
    total_payment = calc_total_by_classification(current_user_id, month_records, is_income=False)
    daily_income_payment = calc_daily_income_payment(current_user_id, month_records)

    return render_template(
        'index.html',
        title='ホーム',
        users=users,
        categories=categories,
        records=records,
        category_percentage=json.dumps(category_percentage_income),
        category_percentage_payment=json.dumps(category_percentage_payment),
        total_income=total_income,
        total_payment=total_payment,
        daily_income_payment=json.dumps(daily_income_payment)
    )

def calc_category_percentage(user_id, categories, records, is_income):
    """
    ユーザーごとのカテゴリ別収入または支出割合を計算します。

    Args:
        user_id (int): 対象ユーザーID
        categories (Iterable[Category]): 全カテゴリ
        records (Iterable[Record]): 対象月のレコード
        is_income (bool): True=収入, False=支出

    Returns:
        dict[str, float]: カテゴリ名をキー、割合（%）を値とする辞書
    """
    records = records.where(
        (Record.user == user_id) &
        (Record.category.classification == is_income)
    )

    category_totals = {}
    total_amount = 0

    for cat in categories:
        # classification が一致しないカテゴリは除外
        if cat.classification != is_income:
            continue

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
    total = 0

    for record in records:
        if record.user_id != user_id:
            continue

        if record.category.classification == is_income:
            total += record.price

    return total

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
        day_str = record.date.strftime('%Y-%m-%d')

        if day_str not in daily_data:
            daily_data[day_str] = {
                'income': 0,
                'payment': 0
            }

        if record.category.classification:
            daily_data[day_str]['income'] += record.price
        else:
            daily_data[day_str]['payment'] += record.price

    return daily_data

def filter_records_by_month(user_id, records, month_str):
    year, month = map(int, month_str.split('-'))
    last_day = monthrange(year, month)[1]

    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    return records.where(
        (Record.user == user_id) &
        (Record.date.between(start_date, end_date))
    )

@app.template_filter('prev_month')
def prev_month(month_str):
    dt = datetime.strptime(month_str, '%Y-%m')
    return (dt - relativedelta(months=1)).strftime('%Y-%m')

@app.template_filter('next_month')
def next_month(month_str):
    dt = datetime.strptime(month_str, '%Y-%m')
    return (dt + relativedelta(months=1)).strftime('%Y-%m')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
