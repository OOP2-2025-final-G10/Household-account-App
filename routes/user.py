from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの定義
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def list():
    # ユーザー全件取得
    users = User.select()
    return render_template('user_list.html', title='ユーザー一覧', items=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        # 名前が空でないか確認（簡易チェック）
        if name:
            User.create(name=name)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    # IDに一致するユーザーを取得（なければ一覧へ戻る）
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        name = request.form['name']
        if name:
            user.name = name
            user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)