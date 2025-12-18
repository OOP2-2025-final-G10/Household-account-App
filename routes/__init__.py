from .user import user_bp
from .category import product_bp
from .record import record_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  record_bp
]