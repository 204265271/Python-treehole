# sql.py
import mysql.connector
import time

# add your config here
config = {
    "username": "", 
    "password": "",
    "host":     "", 
}

MAX_K = 100

def init():
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 创建 treehole 数据库（如果不存在）
        cursor.execute("CREATE DATABASE IF NOT EXISTS treehole")
        print("数据库 'treehole' 已创建或已存在。")

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 创建 hole 表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS hole (
            hole_id INT AUTO_INCREMENT PRIMARY KEY,
            release_time DATETIME,
            user_id INT,
            content TEXT
        )
        """
        cursor.execute(create_table_query)
        print("表 'hole' 已创建或已存在。")
        
        # 创建 comment 表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS comment (
            comment_id INT AUTO_INCREMENT PRIMARY KEY,
            hole_id INT,
            release_time DATETIME,
            user_id INT,
            userNO INT,
            content TEXT,
            FOREIGN KEY (hole_id) REFERENCES hole(hole_id)
        )
        """
        cursor.execute(create_table_query)
        print("表 'comment' 已创建或已存在。")
        
        # 创建 comment_relation 表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS comment_relation (
            hole_id INT,
            user_id INT,
            userNO INT,
            PRIMARY KEY (hole_id, user_id),
            FOREIGN KEY (hole_id) REFERENCES hole(hole_id)
        )
        """
        cursor.execute(create_table_query)
        print("表 'comment_relation' 已创建或已存在。")
        
        # 创建 user 表
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            create_time DATETIME
        )
        """
        cursor.execute(create_table_query)
        print("表 'user' 已创建或已存在。")

        # 提交更改
        connection.commit()

    except mysql.connector.Error as err:
        print(f"[init]发生错误: {err}")
        # 回滚更改
        if 'connection' in locals() and connection.is_connected():
            connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")


def newest_holes(k):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 查询最新发布的 k 个 hole
        new_k = min(k, MAX_K)
        query = f"SELECT * FROM hole ORDER BY release_time DESC LIMIT {new_k}"
        cursor.execute(query)
        results = cursor.fetchall()

        # 打印查询结果
        return (len(results), results)

    except mysql.connector.Error as err:
        print(f"[newest_holes]发生错误: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            
def query_hole(hole_id):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 查询最新发布的 k 个 hole
        query = f"SELECT * FROM hole where hole_id = {hole_id}"
        cursor.execute(query)
        results = cursor.fetchall()

        # 打印查询结果
        return results

    except mysql.connector.Error as err:
        print(f"[query_hole]发生错误: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            

def get_comments_4_hole(hole_id):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 查询指定 hole_id 对应的所有 comment
        query = "SELECT * FROM comment WHERE hole_id = %s"
        cursor.execute(query, (hole_id,))
        comments = cursor.fetchall()

        return comments

    except mysql.connector.Error as err:
        print(f"[get_comments_4_hole]发生错误: {err}")
        return []
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            
def delete_comment(comment_id):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 删除指定 comment_id 的评论
        query = "DELETE FROM comment WHERE comment_id = %s"
        cursor.execute(query, (comment_id,))
        connection.commit()
        print(f"评论 {comment_id} 已删除。")

    except mysql.connector.Error as err:
        print(f"[delete_comment]发生错误: {err}")
        connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")

def delete_hole(hole_id):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 删除该 hole 对应的所有评论
        query_comment = "DELETE FROM comment WHERE hole_id = %s"
        cursor.execute(query_comment, (hole_id,))
        
        # 删除该 hole 对应的所有评论关系
        query_relation = "DELETE FROM comment_relation WHERE hole_id = %s"
        cursor.execute(query_relation, (hole_id,))

        # 删除该 hole
        query_hole = "DELETE FROM hole WHERE hole_id = %s"
        cursor.execute(query_hole, (hole_id,))
        
        connection.commit()
        print(f"树洞 {hole_id} 及其对应的评论已删除。")

    except mysql.connector.Error as err:
        print(f"[delete_hole]发生错误: {err}")
        connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            
def insert_hole(release_time, user_id, content):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("USE treehole")

        insert_query = "INSERT INTO hole (release_time, user_id, content) VALUES (%s, %s, %s)"
        data = (release_time, user_id, content)
        cursor.execute(insert_query, data)
        
        connection.commit()
        print("树洞插入成功。")
        new_hole_id = cursor.lastrowid
        print("树洞插入成功，新增树洞的 id 为:", new_hole_id)
        
        # 插入新行
        insert_query = "INSERT INTO comment_relation (hole_id, user_id, userNO) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (new_hole_id, user_id, 0))
        connection.commit()
        return new_hole_id
    
    except mysql.connector.Error as err:
        print(f"[insert_hole]发生错误: {err}")
        connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")

def insert_comment(hole_id, release_time, user_id, comment):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("USE treehole")

        insert_query = "INSERT INTO comment (hole_id, release_time, user_id, userNO, content) VALUES (%s, %s, %s, %s, %s)"
        data = (hole_id, release_time, user_id, findUserNO(hole_id, user_id), comment)
        cursor.execute(insert_query, data)
        
        connection.commit()
        new_comment_id = cursor.lastrowid
        print("评论插入成功，新增评论的 id 为:", new_comment_id)
        return new_comment_id
    except mysql.connector.Error as err:
        print(f"[insert_comment]发生错误: {err}")
        connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            
def find_holeID_4_comment(comment_id):
    try:
        # 建立数据库连接
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 切换到 treehole 数据库
        cursor.execute("USE treehole")

        # 查询最新发布的 k 个 hole
        query = f"SELECT hole_id FROM comment where comment_id = {comment_id}"
        cursor.execute(query)
        results = cursor.fetchall()

        # 打印查询结果
        if results:
            result, = results[0]
            return result
        else:
            return -1

    except mysql.connector.Error as err:
        print(f"[query_hole]发生错误: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            
def findUserNO(hole_id, user_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("USE treehole")

        # 先查询是否存在对应的行
        query = "SELECT userNO FROM comment_relation WHERE hole_id = %s AND user_id = %s"
        cursor.execute(query, (hole_id, user_id))
        result = cursor.fetchone()

        if result:
            return result[0]

        # 若不存在，查询该 hole_id 对应的最大 userNO
        query_max = "SELECT MAX(userNO) FROM comment_relation WHERE hole_id = %s"
        cursor.execute(query_max, (hole_id,))
        max_userNO = cursor.fetchone()[0]

        if max_userNO is None:
            new_userNO = 1
        else:
            new_userNO = int(max_userNO) + 1

        # 插入新行
        insert_query = "INSERT INTO comment_relation (hole_id, user_id, userNO) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (hole_id, user_id, new_userNO))
        connection.commit()

        return new_userNO

    except mysql.connector.Error as err:
        print(f"[findUserNO]发生错误: {err}")
        connection.rollback()
        return None
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")
            

# warning: don't use easily
def delete_tables():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("USE treehole")

        # 删除表的顺序需要注意，先删除有外键关联的表
        tables = ['comment', 'comment_relation', 'hole', 'user']
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"表 '{table}' 已删除。")
            except mysql.connector.Error as err:
                print(f"删除表 '{table}' 时发生错误: {err}")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"发生错误: {err}")
        connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("数据库连接已关闭。")