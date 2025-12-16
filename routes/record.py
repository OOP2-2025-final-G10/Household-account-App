from flask import Blueprint, render_template, request, redirect, url_for
from models import User, Record, Category
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('record', __name__, url_prefix='/records')


@order_bp.route('/')
def list():
    record = Record.select()
    return render_template('order_list.html', title='注文一覧', items=record)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        price = request.form['price']
        date = datetime.now()
        memo = request.form['memo']
        Record.create(user=user_id, category=category_id, price=price, date=date, memo=memo)
        return redirect(url_for('record.list'))
    
    users = Record.select()
    categories = Category.select()
    return render_template('record_add.html', users=users, categories=categories)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(record_id):
    record = Record.get_or_none(Record.id == record_id)
    if not record:
        return redirect(url_for('order.list'))

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
