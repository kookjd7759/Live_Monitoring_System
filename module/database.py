import pymysql
import json
import os

class DB():
    def __connect(self):
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

    def __init__(self):
        self.DB = self.__connect()
    
    def execute_query(self, query):
        with self.DB.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        return result

    def search_recent_one(self):
        return self.execute_query("SELECT * FROM raw_yjsensing ORDER BY idx DESC LIMIT 1")

    def search_date(self, date):
        result = {
            'worked': None,
            'start_time': None,
            'end_time': None,
            'time_list(sec)': None
        }

        query_one = f"""
            SELECT * FROM raw_yjsensing
            WHERE collecttime >= '{date}' AND collecttime < DATE_ADD('{date}', INTERVAL 1 DAY)
            LIMIT 1
        """
        isWorked = self.execute_query(query_one) != None
        result['worked'] = isWorked

        if isWorked:
            query_firstTime = f"""
                SELECT TIME(collecttime) FROM raw_yjsensing
                WHERE collecttime >= '{date}' AND collecttime < DATE_ADD('{date}', INTERVAL 1 DAY)
                ORDER BY collecttime ASC
                LIMIT 1
            """
            first_time = self.execute_query(query_firstTime)

            query_endTime = f"""
                SELECT TIME(collecttime) FROM raw_yjsensing
                WHERE collecttime >= '{date}' AND collecttime < DATE_ADD('{date}', INTERVAL 1 DAY)
                ORDER BY collecttime DESC
                LIMIT 1
            """
            end_time = self.execute_query(query_endTime)

            query_times = f"""
            SELECT TIME(collecttime) as time_value FROM raw_yjsensing
            WHERE collecttime >= '{date}' AND collecttime < DATE_ADD('{date}', INTERVAL 1 DAY)
            ORDER BY collecttime ASC
            """
            time_list = []
            with self.DB.cursor() as cursor:
                cursor.execute(query_times)
                times = cursor.fetchall()
                for row in times:
                    delta = row['time_value']
                    total_seconds = int(delta.total_seconds())
                    time_list.append(total_seconds)

            result['start_time'] = first_time["TIME(collecttime)"]
            result['end_time'] = end_time["TIME(collecttime)"]
            result['time_list(sec)'] = time_list
        
        return result


if __name__ == "__main__":
    print('start !')
    database = DB()
    data = database.search_date('2025-04-14')
    for key in data:
        print(f'{key}, {data[key]}')