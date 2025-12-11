# routes/__init__.py

from .user import bp as user_bp
# from .product import bp as product_bp # Productのインポートを削除またはコメントアウト
from .category import bp as category_bp # Categoryのインポートを追加
from .order import bp as order_bp

def init_app(app):
    """
    アプリケーションインスタンス(app)にすべてのBlueprintを登録する関数
    """
    app.register_blueprint(user_bp)
    # app.register_blueprint(product_bp) # Productの登録を削除またはコメントアウト
    app.register_blueprint(category_bp) # Categoryの登録を追加
    app.register_blueprint(order_bp)