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
    # クエリパラメータから表示月を取得
    month = request.args.get('month', current_month)

    users = User.select()
    categories = Category.select()
    records = Record.select()

    # --- 全ユーザーの統計データを集計 ---
    all_user_data = {}
    for u in users:
        # ユーザー×月のレコード抽出
        u_month_records = filter_records_by_month(u.id, records, month)
        
        # 円グラフ用：カテゴリ別割合
        u_income_pct = calc_category_percentage(u.id, categories, u_month_records, is_income=True)
        u_payment_pct = calc_category_percentage(u.id, categories, u_month_records, is_income=False)
        
        # 棒グラフ用：合計金額
        u_total_income = calc_total_by_classification(u.id, u_month_records, is_income=True)
        u_total_payment = calc_total_by_classification(u.id, u_month_records, is_income=False)

        all_user_data[u.id] = {
            'name': u.name,
            'income_pct': u_income_pct,
            'payment_pct': u_payment_pct,
            'total_income': u_total_income,
            'total_payment': u_total_payment
        }

    return render_template(
        'index.html',
        title='ホーム',
        users=users,
        current_month=month,
        # JSON形式でHTML側のJavaScriptに渡す
        all_user_data_json=json.dumps(all_user_data)
    )

def calc_category_percentage(user_id, categories, records, is_income):
    # 特定ユーザーと収支区分でフィルタ
    filtered_records = [
        r for r in records 
        if r.user_id == user_id and r.category.classification == is_income
    ]

    category_totals = {}
    total_amount = 0

    for cat in categories:
        if cat.classification != is_income:
            continue
        
        cat_total = sum(r.price for r in filtered_records if r.category_id == cat.id)
        if cat_total > 0:
            category_totals[cat.name] = cat_total
            total_amount += cat_total

    # 割合の計算
    category_percentages = {}
    for name, amount in category_totals.items():
        category_percentages[name] = round((amount / total_amount) * 100, 1) if total_amount > 0 else 0

    return category_percentages

def calc_total_by_classification(user_id, records, is_income):
    total = sum(r.price for r in records if r.user_id == user_id and r.category.classification == is_income)
    return total

def filter_records_by_month(user_id, records, month_str):
    year, month = map(int, month_str.split('-'))
    last_day = monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)
    return records.where((Record.user == user_id) & (Record.date.between(start_date, end_date)))

# テンプレートフィルタ
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