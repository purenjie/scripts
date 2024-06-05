import pymysql


class MysqlDB:

    def __init__(self, host, port, db, user,password, connect_timeout=20, read_timeout=20, write_timeout=20):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            db=db,
            user=user,
            passwd=password,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            write_timeout=write_timeout
        )
    
    def fetch(self, sql):
        res = None
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as e:
            print('数据库查询失败！\n'+str(e))
        cur.close()
        return res

    def execute(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('数据库操作失败！\n'+str(e))
            self.conn.rollback()
        cur.close()

    def quit(self):
        self.conn.close()

host = "9.134.194.121"
port = 3306
db = "museum"
user = "root"
password = "password"

client = MysqlDB(host, port, db, user, password)

query_one_sql = 'select * from museum where museum_id = 20888'
query_many_sql = 'select * from museum where museum_id in ("20888", "20184")'
execute_sql = '''
INSERT INTO `museum` (`museum_id`, `name`, `description`, `open_time`, `logo`, `phone`, `city`, `tag`, `qrcode`, `notice`, `operator`, `album`)
VALUES
	('11111', '中国印学博物馆11', 'desc11', '12:00', 'logo', '110', 'city', 'tag', 'qrcode', 'notice', 'operator', 'album');
'''

print(client.fetch(query_one_sql))
print(client.fetch(query_many_sql))
print(client.execute(execute_sql))
