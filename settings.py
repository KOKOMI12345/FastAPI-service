#这里写配置文件

class settings:
   '''
   settings模块为自己的API项目配置,在这里写自己的配置文件
   '''
   ALLOWED_PICTURE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
   ALLOWED_MUSIC_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
   IMAGES_FOLDER = 'static/images'
   MUSIC_FOLDER = 'static/music'
   DATABASE = 'static/database.json'
   MAX_DATABASE_CONN = 30
   DB_MODEL = 'static/db_model.sql'
   VIDEO_STATIC = 'static/api_video'