import pymysql
import json
import time

def connect():
    with open('config/DB.json', 'r', encoding='utf-8') as file:
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

def latest_data():
    conn = connect()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM raw_yjsensing ORDER BY idx DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
    conn.close()
    return result

if __name__ == "__main__":
    while True:
        data = latest_data()
        if data:
            for key, value in data.items():
                if key == 'idx':
                    print('idx : ', end='')
                print(f'{value}, ', end='')
            print('')
        time.sleep(1)