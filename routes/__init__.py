from .user import user_bp
from .category import product_bp
from .record import order_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp
]
