# models/__init__.py (衝突を解決した後)

# 他のモデルをインポート
from .user import User
from .product import Product 
from .order import Order

# Categoryモデルをインポート
from .category import Category 

# データベースにテーブルを作成するモデルをリスト化
MODELS = [
    User,
    Product,
    Category, # <-- あなたの変更を統合
    Order,
]

def init_database():
    """ データベースを初期化し、テーブルが存在しない場合は作成する """
    database.connect()
    # MODELSリスト内のすべてのテーブルを作成（既に存在する場合はスキップ）
    database.create_tables(MODELS) 
    database.close()