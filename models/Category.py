# models/category.py
from peewee import *
from .db import database

# Base Class
class BaseModel(Model):
    class Meta:
        database = database

# Category Class (費目・カテゴリー)
class Category(BaseModel):
    # 費目名 (例: 食費、交通費、給料、アルバイト代)
    name = CharField(max_length=255, unique=True)
    
    # 収支区分 (0=支出, 1=収入)
    # BooleanFieldはTrue/Falseですが、ここでは0/1の整数として扱うCharFieldまたはIntegerFieldを使用します。
    # 0/1で管理するならIntegerField、'支出'/'収入'の文字列で管理するならCharFieldが良いでしょう。
    # ここでは、わかりやすさのためIntegerField (0=支出, 1=収入) を採用します。
    classification = IntegerField(default=0)
    
    # 予算/目標額 (例: 食費は月3万)
    target_amount = IntegerField(default=0)
    
    class Meta:
        # テーブル名
        table_name = 'categories'
        # 費目名と収支区分の組み合わせが一意であることを保証することも考えられますが、
        # 今回は費目名自体をユニークにします。
        pass

# --- モデルの説明 ---
# name:       CharField - 文字列フィールド。費目名を保存します。
# classification: IntegerField - 整数フィールド。0を支出、1を収入として区別します。
# target_amount: IntegerField - 整数フィールド。予算や目標額を保存します。