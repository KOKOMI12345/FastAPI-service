import logging
import colorlog
import os
#这个是我自己优化的日志堆栈,用到的模块再上面
def config_log():
   #颜色配置!
   log_color_config = {
    'DEBUG': 'reset',
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
    'RESET': 'reset'
    }
   log_folder = './main_log/database_log'
   if os.path.exists(log_folder):
      pass
   else:
      os.makedirs(log_folder, exist_ok=True)

   logger = logging.getLogger('track-log')

   console_handler = logging.StreamHandler()
   file_hander = logging.FileHandler(filename='main_log/database_log/database_log.log', mode='a',encoding='utf-8')

   logger.setLevel(logging.DEBUG)
   console_handler.setLevel(logging.DEBUG)
   file_hander.setLevel(logging.INFO)

   file_formatter = logging.Formatter(
      #格式转换(文件)
      fmt='[%(asctime)s.%(msecs)03d] | %(levelname)-8s | %(filename)s | %(funcName)s | line:%(lineno)-5d | %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
    )
   console_formatter = colorlog.ColoredFormatter(
      #格式转换(输出再控制台!)
      fmt='[%(asctime)s.%(msecs)03d] | %(log_color)s%(levelname)-8s%(reset)s | %(filename)s | %(funcName)s | line:%(log_color)s%(lineno)d%(reset)s | %(log_color)s%(message)s%(reset)s',
      datefmt='%Y-%m-%d %H:%M:%S',
      log_colors=log_color_config
    )


   console_handler.setFormatter(console_formatter)
   file_hander.setFormatter(file_formatter)
   
   if not logger.handlers:
       logger.addHandler(console_handler)
       logger.addHandler(file_hander)

   console_handler.close()
   file_hander.close()
   return logger
