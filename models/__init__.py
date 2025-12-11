# models/__init__.py

from .db import database
from .user import User
# from .product import Product # 元のProductの行は削除またはコメントアウト
from .category import Category # Categoryのインポートを追加
from .order import Order

# すべてのモデルのリストを定義
MODELS = [
    User,
    Category, # Categoryに変更
    Order
]