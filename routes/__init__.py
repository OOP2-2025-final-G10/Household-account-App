# routes/__init__.py (衝突解決後)

# 各ルーティングファイルからブループリントをインポート
from .user import user_bp
from .product import product_bp # mainブランチにあったproduct_bpを維持
from .category import category_bp # あなたが追加したcategory_bpを維持
from .order import order_bp

# 全てのブループリントのリスト
BLUEPRINTS = [
    user_bp,
    # category_bpとproduct_bpを両方リストに含める
    product_bp,
    category_bp, 
    order_bp,
]