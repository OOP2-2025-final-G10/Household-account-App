from flask import Blueprint, render_template, request, redirect, url_for
from models import Category

# Blueprintの作成
product_bp = Blueprint('category', __name__, url_prefix='/categories')


@product_bp.route('/')
def list():
    category = Category.select()
    # 費目一覧を表示
    return render_template('category_list.html', title='費目一覧', items=category)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']

        # HTMLフォームのname属性 "classfication" (スペルミス) を受け取る
        classfication_val = request.form['classfication']
        
        # データベースの正しい列名 "classification" に保存する
        # "1"なら収入(True), "0"なら支出(False)として変換して保存
        is_income = (classfication_val == '1')
        
        Category.create(name=name, classification=is_income)
        
        return redirect(url_for('category.list'))
    
    return render_template('category_add.html')


# HTMLのURL指定に合わせて <int:product_id> を受け取るように修正
@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    # 受け取った product_id を使ってデータを取得
    category = Category.get_or_none(Category.id == product_id)
    if not category:
        return redirect(url_for('category.list'))

    if request.method == 'POST':
        category.name = request.form['name']
        
        # 編集時も同様に "classfication" を受け取り "classification" に保存
        classfication_val = request.form['classfication']
        category.classification = (classfication_val == '1')
        
        category.save()
        return redirect(url_for('category.list'))

    return render_template('category_edit.html', category=category)