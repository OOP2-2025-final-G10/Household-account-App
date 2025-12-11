from flask import Blueprint, render_template, request, redirect, url_for
from models import Category

# Blueprintの作成
product_bp = Blueprint('category', __name__, url_prefix='/categories')


@product_bp.route('/')
def list():
    category = Category.select()
    return render_template('product_list.html', title='カテゴリー一覧', items=category)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        classfication = request.form['classfication']
        Category.create(name=name, classfication=classfication)
        return redirect(url_for('category.list'))
    
    return render_template('category_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(category_id):
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return redirect(url_for('category.list'))

    if request.method == 'POST':
        category.name = request.form['name']
        category.price = request.form['classfication']
        category.save()
        return redirect(url_for('category.list'))

    return render_template('category_edit.html', category=category)