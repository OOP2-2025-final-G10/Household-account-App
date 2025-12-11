from flask import Blueprint, render_template, request, redirect, url_for
# modelsモジュール全体からCategoryをインポート
from models import Category 

# Blueprintの定義（/categories/ というURLプレフィックスを設定）
bp = Blueprint('category', __name__, url_prefix='/categories')

# --- Category一覧表示 (/categories/) ---
@bp.route('/')
def category_list():
    # データベースからすべてのCategoryデータを取得
    categories = Category.select()
    # テンプレートにデータを渡してレンダリング
    return render_template('category_list.html', categories=categories)

# --- Category登録・編集フォーム (/categories/add, /categories/edit/1) ---
# category_idがNoneの場合は新規追加、指定されている場合は編集
@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def category_form(category_id=None):
    category = None
    
    # 編集モードの場合、既存データを取得
    if category_id:
        category = Category.get_or_none(Category.id == category_id)

    # POSTリクエスト（フォーム送信）時の処理
    if request.method == 'POST':
        # フォームから送られたデータを取得
        name = request.form['name']
        # typeとbudgetはHTMLから文字列として送られるため、Integerに変換
        type_val = int(request.form['type'])
        budget = int(request.form['budget'])

        if category_id:
            # 更新処理
            category.name = name
            category.type = type_val
            category.budget = budget
            category.save()
        else:
            # 新規作成処理
            Category.create(name=name, type=type_val, budget=budget)
        
        # 処理後、一覧画面にリダイレクト
        # Blueprint名('category')と関数名('category_list')を指定
        return redirect(url_for('category.category_list'))
    
    # GETリクエストの場合、フォームを表示
    # category_idがあれば編集フォーム、なければ追加フォームとして動作
    return render_template('category_add.html', category=category)