# routes/category.py
from flask import Blueprint, render_template, request, redirect, url_for
from peewee import IntegrityError

# Categoryモデルをインポート
from models.category import Category

# Flaskのブループリントを作成
category_bp = Blueprint('category', __name__)

### 1. 費目/カテゴリーの一覧表示 (/category/list) ###
@category_bp.route('/list')
def category_list():
    """ 登録されている費目/カテゴリーの一覧を表示する """
    # データベースから全てのCategoryレコードを取得 (ID降順)
    categories = Category.select().order_by(Category.id.desc())
    
    # テンプレートにデータを渡してレンダリング
    return render_template(
        'category_list.html', 
        categories=categories,
        title='費目/カテゴリー一覧'
    )

### 2. 費目/カテゴリーの登録画面表示と登録処理 (/category/add) ###
@category_bp.route('/add', methods=['GET', 'POST'])
def category_add():
    """ 費目/カテゴリーの登録画面を表示し、POSTリクエストで登録処理を行う """
    message = None
    
    if request.method == 'POST':
        # フォームからデータを取得
        name = request.form.get('name')
        # classificationはラジオボタンから取得 (0 または 1)
        classification = request.form.get('classification')
        # target_amountはフォームから取得し、整数に変換 (失敗したら0)
        try:
            target_amount = int(request.form.get('target_amount', 0))
        except ValueError:
            target_amount = 0

        # データ検証 (名前が空でないこと)
        if not name:
            message = '費目名を入力してください。'
        else:
            try:
                # データベースに新しいCategoryレコードを作成
                Category.create(
                    name=name,
                    classification=classification,
                    target_amount=target_amount
                )
                # 登録成功後、一覧ページにリダイレクト
                return redirect(url_for('category.category_list'))
            except IntegrityError:
                message = f'費目名「{name}」は既に登録されています。'
            except Exception as e:
                message = f'登録中にエラーが発生しました: {e}'

    # GETリクエストの場合、またはPOSTでエラーが発生した場合
    return render_template(
        'category_add.html',
        message=message,
        title='費目/カテゴリー登録'
    )

### 3. 費目/カテゴリーの編集画面表示と更新処理 (/category/edit/<id>) ###
@category_bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    """ 指定されたIDの費目/カテゴリーを編集する """
    
    try:
        # IDに基づいてCategoryレコードを取得
        category = Category.get_by_id(category_id)
    except Category.DoesNotExist:
        # 存在しないIDの場合は一覧ページへリダイレクト
        return redirect(url_for('category.category_list'))
        
    message = None

    if request.method == 'POST':
        # フォームからデータを取得
        name = request.form.get('name')
        classification = request.form.get('classification')
        try:
            target_amount = int(request.form.get('target_amount', 0))
        except ValueError:
            target_amount = 0

        # データ検証 (名前が空でないこと)
        if not name:
            message = '費目名を入力してください。'
        else:
            try:
                # レコードの値を更新
                category.name = name
                category.classification = classification
                category.target_amount = target_amount
                category.save() # データベースに保存
                
                # 更新成功後、一覧ページにリダイレクト
                return redirect(url_for('category.category_list'))
            except IntegrityError:
                message = f'費目名「{name}」は既に他の費目に登録されています。'
            except Exception as e:
                message = f'更新中にエラーが発生しました: {e}'
        
    # GETリクエストの場合、またはPOSTでエラーが発生した場合
    return render_template(
        'category_edit.html',
        category=category, # 現在のデータをテンプレートに渡す
        message=message,
        title='費目/カテゴリー編集'
    )

### 4. 費目/カテゴリーの削除処理 (/category/delete/<id>) ###
@category_bp.route('/delete/<int:category_id>', methods=['POST'])
def category_delete(category_id):
    """ 指定されたIDの費目/カテゴリーを削除する """
    try:
        # IDに基づいてCategoryレコードを取得し、削除
        category = Category.get_by_id(category_id)
        category.delete_instance()
    except Category.DoesNotExist:
        # 削除対象が存在しなくても、エラーにはせず一覧に戻る
        pass 
    
    # 処理後、一覧ページにリダイレクト
    return redirect(url_for('category.category_list'))