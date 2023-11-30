'''连接池配置'''
from connections import *
from settings import *
db_logger = db_pool_log.config_log()
database_pool = db_pool.DataBase_pool(size=int(settings.MAX_DATABASE_CONN))
database_pool.init_pool()



def get_cursor():
    conn = database_pool.get_conn()
    cursor = conn.cursor()
    return cursor, conn