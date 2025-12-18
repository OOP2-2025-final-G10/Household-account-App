from flask import Blueprint, render_template, request, redirect, url_for
from models import User, Record, Category
from datetime import datetime

# Blueprintの作成
record_bp = Blueprint('record', __name__, url_prefix='/records')


@record_bp.route('/')
def list():
    record = Record.select()
    return render_template('record_list.html', title='記録一覧', items=record)


@record_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        price = request.form['price']
        date = datetime.now()
        memo = request.form['memo']
        Record.create(user=user_id, category=category_id, price=price, date=date, memo=memo)
        return redirect(url_for('record.list'))
    
    # 【修正箇所1】以前は Record.select() になっていました。User.select() に直します。
    users = User.select()
    categories = Category.select()
    return render_template('record_add.html', users=users, categories=categories)


# 【修正箇所2】URL変数の <int:order_id> に合わせて、関数の引数も order_id に統一しました
@record_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit(record_id):
    # 引数に合わせて order_id で検索するように修正
    record = Record.get_or_none(Record.id == record_id)
    if not record:
        return redirect(url_for('record.list'))

    if request.method == 'POST':
        record.user_id = request.form['user_id']
        record.category_id = request.form['category_id']
        record.price = request.form['price']
        record.date = datetime.now()
        record.memo = request.form['memo']
        record.save()
        return redirect(url_for('record.list'))

    users = User.select()
    categories = Category.select()
    return render_template('record_edit.html', record=record, users=users, categories=categories)