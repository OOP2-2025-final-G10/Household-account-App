# models/__init__.py

# 他のモデルをインポート
from .user import User
from .product import Product # サンプルアプリのProductはCategoryに置き換えられますが、
                            # ひとまず全て残しておき、後でCategoryに差し替えます。
from .order import Order

# Categoryモデルをインポート
from .category import Category # <-- この行を追加

# db.pyからdatabaseオブジェクトをインポート
from .db import database

# データベースにテーブルを作成するモデルをリスト化
# Categoryモデルも追加します
MODELS = [
    User,
    Product, # (Categoryへの変更を想定して、一旦残します)
    Category, # <-- この行を追加
    Order,
]

def init_database():
    """ データベースを初期化し、テーブルが存在しない場合は作成する """
    database.connect()
    # MODELSリスト内のすべてのテーブルを作成（既に存在する場合はスキップ）
    database.create_tables(MODELS) 
    database.close()