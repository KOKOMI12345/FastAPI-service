import pymysql
import json
import logging
from settings import *
from database_pool.db_pool_log import config_log

logging.basicConfig(level=logging.INFO)

class DataBase_pool:
    '''
    这个是基于queue配置的基本数据库连接池,可以使用这个来减小数据库的
    连接开销以增强性能
    '''
    def __init__(self, size=5):
        self.size = size
        self._pool = []
        self.logger = logging.getLogger("ConnPool")
        logger_handler = config_log()
        self.logger.addHandler(logger_handler)
        
    def init_pool(self):
        '''初始化数据库连接池'''
        with open(f'{settings.DATABASE}') as f:
            database_conn = json.load(f)
        
        for i in range(self.size):
            conn = pymysql.connect(
                host=database_conn['host'],
                port=database_conn['port'],
                user=database_conn['user'],
                passwd=database_conn['password'],
                db=database_conn['database'],
                charset=database_conn['charset']
            )
            self._pool.append(conn)
            
    def get_conn(self):
        '''获取从数据库连接池拿取1个数据库连接'''
        if len(self._pool) == 0:
            self.logger.error("连接池耗尽")
            return None
        if len(self._pool) < (self.size / 2):
            self.logger.warn("警告,连接池资源过半")
        conn = self._pool.pop()
        self.logger.info(f"获取到连接,当前剩余连接数:{len(self._pool)}")
        return conn
        
    def release_conn(self, conn):
        '''有借有还,用完了连接别忘了归还回来!'''
        if len(self._pool) <= 0:
            self._pool = []
        self._pool.append(conn)
        self.logger.info(f"释放连接,当前剩余连接数:{len(self._pool)}")

