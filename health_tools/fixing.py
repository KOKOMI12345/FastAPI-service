import pymysql
import sys
sys.path.append("G:/furina_api")
import json
from settings import settings as settings
from logger import logs
class CreateDB_model:
    '''
    你可以在static文件夹中的sql文件写自己的sql模型,这里只是运用模型而已
    '''
    def __init__(self):
        self.logger = logs.config_log(log_name=__name__)
        self.database_conn = None
        self.conn = None
        self.cursor = None

    def create(self):
        try:
            
            with open(f'{settings.DATABASE}', 'r') as f:
                self.database_conn = json.load(f)

            self.conn = pymysql.connect(
                host=self.database_conn['host'],
                port=self.database_conn['port'],
                user=self.database_conn['user'],
                passwd=self.database_conn['password'],
                db=self.database_conn['database'],
                charset=self.database_conn['charset']
            )

            self.cursor = self.conn.cursor()
            with open(f'{settings.DB_MODEL}', 'r') as sql_code:
                sql_model = sql_code.read()
                self.cursor.execute(sql_model)
                self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            self.logger.error(f"创建数据库模型失败，原因为: {e}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

DB_creater = CreateDB_model()
DB_creater.create()