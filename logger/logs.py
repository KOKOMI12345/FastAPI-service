import logging
import colorlog
import os
#这个是我自己优化的日志堆栈,用到的模块再上面
def config_log(log_name: str):
   #颜色配置!
   log_color_config = {
    'DEBUG': 'reset',
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
    'RESET': 'reset'
    }
   log_folder = './main_log/track_log'
   if os.path.exists(log_folder):
      pass
   else:
      os.makedirs(log_folder, exist_ok=True)

   logger = logging.getLogger(f'{log_name}')

   console_handler = logging.StreamHandler()
   file_hander = logging.FileHandler(filename='main_log/track_log/track_log.log', mode='a',encoding='utf-8')

   logger.setLevel(logging.DEBUG)
   console_handler.setLevel(logging.DEBUG)
   file_hander.setLevel(logging.INFO)
   #这里的判断就是让日志详细记录或者不详细记录
   file_formatter = logging.Formatter(
      #格式转换(文件)
      fmt='[%(asctime)s.%(msecs)03d] |%(levelname)-8s | %(filename)s | %(funcName)s | line:%(lineno)-5d |%(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
      )
   console_formatter = colorlog.ColoredFormatter(
      #格式转换(输出再控制台!)
      fmt='[%(asctime)s.%(msecs)03d] |%(log_color)s%(levelname)-8s%(reset)s | %(filename)s | %(funcName)s | line:%(log_color)s%(lineno)d%(reset)s |%(log_color)s%(message)s%(reset)s',
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

if __name__ == '__main__':
   '''下面是用法
   config_log() 为我配置好的日志处理器对象
   用法:
   logger = config_log(log_name=your_log_name)
   然后你就可以用logger来记录东西啦!
   注意: 在其他模块中使用这个模块的话,要
   import logs
   logger = logs.config_log(log_name=your_log_name)
   下面是示例
   '''
   logger = config_log(log_name='example')
   logger.warning("请注意,找到1个php文件,在.static/API_images/test.php")
   #可以看到他们都被渲染上了不同的颜色,根据不同的等级!