# setup_db.py

from models import User, Category, Order 
from models.db import database 

def setup_database():
    """データベースのテーブルを初期化し、初期データを投入する関数"""
    if database.is_closed():
        database.connect()
    
    # テーブルの削除と再作成 (Categoryを含める)
    # OrderにはまだUserとCategoryへのリレーション定義がないため、現状このまま
    database.drop_tables([User, Category, Order]) 
    database.create_tables([User, Category, Order])
    print("データベーステーブルを初期化しました。")

    # --- Userデータの挿入 (User担当が修正するまで仮データ) ---
    users_data = [
        {'name': '父', 'target_savings': 50000},
        {'name': '母', 'target_savings': 30000},
    ]
    User.insert_many(users_data).execute()
    print("Userテーブルに初期データを挿入しました。")

    # --- Categoryデータの挿入 (あなたの初期データ) ---
    categories_data = [
        {'name': '食費', 'type': 0, 'budget': 40000}, # 支出
        {'name': '交通費', 'type': 0, 'budget': 10000}, # 支出
        {'name': '給与', 'type': 1, 'budget': 350000}, # 収入
        {'name': '趣味', 'type': 0, 'budget': 20000}, # 支出
    ]
    Category.insert_many(categories_data).execute()
    print("Categoryテーブルに初期データを挿入しました。")
    
    database.close()

if __name__ == '__main__':
    setup_database()