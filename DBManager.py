import pymysql.cursors


class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    def __init__(self):
        DBManager.create_DB()
        DBManager.create_department()
        DBManager.create_univ()
        return

    @staticmethod
    def create_DB():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'CREATE DATABASE IF NOT EXISTS sookmyung'
            cursor.execute(sql)
            conn.commit()
        return

    @staticmethod
    def create_univ():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                   CREATE TABLE IF NOT EXISTS univ( 
                    id int(11) NOT NULL,
                    large_category varchar(50) NOT NULL,
                    small_category varchar(50) NOT NULL, 
                    title varchar(200) NOT NULL,
                    content varchar(5000)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
            '''
            cursor.execute(sql)
        return

    @staticmethod
    def create_department():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                    CREATE TABLE IF NOT EXISTS department( 
                    id int(11) NOT NULL,
                    large_category varchar(50) NOT NULL,
                    small_category varchar(50) NOT NULL, 
                    title varchar(200) NOT NULL,
                    content varchar(5000) 
                   ) ENGINE=InnoDB DEFAULT CHARSET=utf8
            '''
            cursor.execute(sql)
            conn.commit()
        return

    @staticmethod
    def insert_univ(id, large_category, small_category, title, content):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO univ (id, large_category, small_category, title, content) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (str(id), large_category, small_category, title, content))
        conn.commit()
        # 1 (last insert id)
        return

    @staticmethod
    def select_univ():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM univ'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                print(row)
            # (1, 'test@test.com', 'my-passwd')
        return

    @staticmethod
    def delete_univ_all():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'DELETE FROM univ'
            cursor.execute(sql)
            conn.commit()
        return

    @staticmethod
    def insert_department(id, large_category, small_category, title, content):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO department (id, large_category, small_category, title, content) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (str(id), large_category, small_category, title, content))
        conn.commit()
        # 1 (last insert id)
        return

    @staticmethod
    def select_department():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM department'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                print(row)
            # (1, 'test@test.com', 'my-passwd')
        return

    @staticmethod
    def delete_department_all():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'DELETE FROM department'
            cursor.execute(sql)
            conn.commit()
        return