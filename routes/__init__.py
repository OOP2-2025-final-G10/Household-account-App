# routes/__init__.py

# 各ルーティングファイルからブループリントをインポート
from .user import user_bp
# from .product import product_bp # Categoryに置き換えるためコメントアウトまたは削除を推奨
from .category import category_bp # <-- この行を追加
from .order import order_bp

# 全てのブループリントのリスト
BLUEPRINTS = [
    user_bp,
    # product_bp, # Categoryに置き換えるためコメントアウトまたは削除を推奨
    category_bp, # <-- この行を追加
    order_bp,
]