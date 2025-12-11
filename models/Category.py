from peewee import *
from .db import BaseModel # db.pyから基本モデルをインポート

class Category(BaseModel):
    # 費目名 (例: 食費、給料)
    name = CharField(unique=True)         
    # 収支区分 (0: 支出, 1: 収入)
    type = IntegerField(default=0)
    # 予算/目標額
    budget = IntegerField(default=0)
    
    class Meta:
        # データベース内のテーブル名を 'categories' に設定
        table_name = 'categories'