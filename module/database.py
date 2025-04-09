import pymysql
import json
import os

class DB():
    def __init__(self):
        self.DB = self.connect()
    
    def connect(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_path, 'config', 'DB.json')
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        conn = pymysql.connect(
            host=data["host"],
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn

    def excute_query(self, query):
        with self.DB.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        print('query end')
        return result

    def search_recent_one(self):
        return self.excute_query("SELECT * FROM raw_yjsensing ORDER BY idx DESC LIMIT 1")

    def search_date_one(self, date):
        return self.excute_query(f"SELECT * FROM raw_yjsensing WHERE DATE(collecttime) = '{date}' LIMIT 1")


if __name__ == "__main__":
    database = DB()
    print(database)