from __init__ import *
'''
在这里写自己的API
'''

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_PICTURE_EXTENSIONS

def allowed_music(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_MUSIC_EXTENSIONS

"""API文档
[GET]https://music.cinojiang.cc/api.my-picture?mode=get&token=&picture=
[POST]https://music.cinojiang.cc/api.my-picture?mode=post&token=
{
   "image":"二进制图片文件",
   "token":"如果api里面填了的话这个请忽略"
   "image_name":"图片名字"
}

"""

@api.get("/api.sese-picture")
async def get_picture(mode: str,token: str,picture: str):
    logger.info(f"有人尝试获取图片,图片名字为 {picture}")
    try:
        if mode == 'get' and token == 'FurinaPrimaryConntroRods':
            cursor, conn = get_cursor()
            cursor.execute("SELECT * FROM API_images WHERE userpicname = %s", (picture,))
            data = cursor.fetchall()
            logger.debug(f"{data}")
            database_pool.release_conn(conn)
            if data:
                logger.info(f"获取图片 {picture} 成功")
                return FileResponse(settings.IMAGES_FOLDER + '/' + data[0][1],filename=data[0][1], headers={'Content-Disposition': 'attachment'})
            else:
                return JSONResponse(status_code=404, content={'status': 404, 'message': '没找到指定图片'})
        else:
            return JSONResponse(status_code=403, content={'status': 403, 'message': 'token错误'})
    except Exception as e:
        logger.error(f"获取图片 {picture} 失败,原因: {e}")
        return JSONResponse(status_code=500, content={'status': 500, 'message': str(e)})

@api.post("/api.sese-picture")
async def post_picture(mode: str,token: str,image_name: str, image: bytes = File(...)):
    logger.info(f"有人尝试上传图片,图片名字为 {image_name}")
    if mode == 'post' and token == 'FurinaPrimaryConntroRods':
        try:
            if not allowed_file(image.filename):
                return JSONResponse(status_code=400, content={'status': 400, 'message': '上传的不是图片'})
            
            if image.filename == '' or image_name == '' or image_name is None:
                return JSONResponse(status_code=400, content={'status': 400, 'message': '上传的图片名为空'})
            
            unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[-1]
            file_path = os.path.join(settings.IMAGES_FOLDER, unique_filename)
            with open(file_path, "wb") as file_object:
                file_object.write(image.file.read())
            
            cursor, conn = get_cursor()
            cursor.execute("INSERT INTO API_images (filename,userpicname) VALUES (%s,%s)", (unique_filename,image_name))
            conn.commit()
            database_pool.release_conn(conn)
            logger.info(f"上传图片 {image_name} 成功")
            return {'status': 200, 'message': '上传成功', 'filename': unique_filename}
        except Exception as e:
            logger.error(f"上传失败,原因为: {e}")
            return JSONResponse(status_code=500, content={'status': 500, 'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'status': 403, 'message': 'token错误'})
    
"""API文档
[GET]https://music.cinojiang.cc/api.my-music?mode=get&token=&music=你的音乐
[POST]https://music.cinojiang.cc/api.my-music?mode=post&token=
{
   "music":"二进制音频文件",
   "token":"api填了token的话请忽略"
   "music_name":"音乐名字"
}

"""

@api.get('/api.my-music')
async def get_music(music: str, mode: str, token: str):
 logger.info(f"有人尝试获取音乐,音乐名字为 {music}")
 try:
    if mode != 'get':
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method Not Allowed")
    if token != 'FurinaMusicPrimaryConntroRods':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token Error")
    
    cursor , conn = get_cursor()
    cursor.execute("SELECT * FROM API_music WHERE usermusicname = %s", (music,))
    data = cursor.fetchall()
    database_pool.release_conn(conn)
    if data:
        filepath = os.path.join(settings.MUSIC_FOLDER + '/' + data[0][1])
        return FileResponse(filepath,filename=data[0][1], headers={'Content-Disposition': 'attachment'})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music Not Found")
 except Exception as e:
     logger.error(f"获取失败,api:my-music,原因为: {e}")

@api.post('/api.my-music')
async def upload_music(mode: str,token: str,music_name: str, music: bytes = File(...)):
 logger.info(f"有人尝试上传音乐,音乐名字为 {music_name}")
 try:
    if mode != 'post':
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method Not Allowed")
    if token != 'FurinaMusicPrimaryConntroRods':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token Error")
    if not allowed_music(music.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Music")
    if music_name == '' or music_name == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Music Name Empty")
    
    unique_filename = str(uuid.uuid4()) + os.path.splitext(music.filename)[-1]
    with open(os.path.join(settings.MUSIC_FOLDER, unique_filename), 'wb') as f:
        f.write(music)
    
    cursor, conn = get_cursor()
    cursor.execute("INSERT INTO API_music (filename,usermusicname) VALUES (%s,%s)", (unique_filename,music_name))
    conn.commit()
    database_pool.release_conn(conn)
    return {'status': 200, 'message': '上传成功', 'filename': unique_filename}
 except Exception as e:
     logger.error(f"发生了一个错误在试图上传到my-music的api中,信息为: {e}")


@api.get("/api.download")
async def download(bv: str,returns: str):
 '''API文档
 [GET]https://music.cinojiang.cc/api.download
 参数需要[requires]:
 1. bv: b站的视频bv号,一般在网址中
 2. returns: 返回video[视频文件],audio[音频文件]
 Example[例子]:
 https://music.cinojiang.cc/api.download?bv=BV1eN4y1D7oU&returns=audio -> 对应视频的音频文件
 https://music.cinojiang.cc/api.download?bv=BV1eN4y1D7oU&returns=video -> 对应视频的视频文件
 Exceptions[可能的异常]:
 1. bv不正确或不存在 raise -> 404
 2. 视频或音频不存在 raise -> 404
 3. 数据库的查询bug  raise -> null
 4. returns模式错误  raise -> 400: require video or audio mode!
 '''
 cursor = None
 conn = None
 bv_code = bv
 try:
    cursor,conn = get_cursor()
    cursor.execute(f"SELECT * FROM api_spider WHERE bv_code = %s",(bv_code,))
    data = cursor.fetchone()
    database_pool.release_conn(conn=conn)
    cursor.close()
    if data:
     print(data)
     if returns == 'video':
        video_name = data[1]
        return FileResponse(settings.VIDEO_STATIC + '/' + video_name,headers={'Content-Disposition': 'attachment'})
     elif returns == 'audio':
        audio_name = data[2]
        print(data)
        return FileResponse(settings.VIDEO_STATIC + '/' + audio_name,headers={'Content-Disposition': 'attachment'})
     else:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='参数错误')
    else:
       url = f'https://www.bilibili.com/video/{bv}/'
       logger.info("someone has spidered a video")

       header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
        'Referer': 'https://www.bilibili.com/'
       }

       resp = requests.get(url=url, headers=header)
       soup = BeautifulSoup(resp.text, 'html.parser')
       script_content = soup.find('script', text=re.compile(r'window\.__playinfo__'))
       json_str = re.search(r'({.*})', script_content.string).group(1)
       json_data = json.loads(json_str)

       videos = json_data['data']['dash']['video']
       audios = json_data['data']['dash']['audio']
       video_url = videos[0]['baseUrl']
       audio_url = audios[0]['baseUrl']

       response = requests.get(url=video_url, headers=header)
       video_filename = f'{uuid.uuid4()}.mp4'  # 使用唯一标识符作为视频文件名
       video_path = os.path.join(settings.VIDEO_STATIC, video_filename)
       with open(video_path, 'wb') as f:
          f.write(response.content)

       response2 = requests.get(url=audio_url, headers=header)
       audio_filename = f'{uuid.uuid4()}.wav'  # 使用唯一标识符作为音频文件名
       audio_path = os.path.join(settings.VIDEO_STATIC, audio_filename)
       with open(audio_path, 'wb') as f:
          f.write(response2.content)

       videoname = video_filename
       audioname = audio_filename
       bv_code = bv
       cursor,conn = get_cursor()
       cursor.execute(f"INSERT INTO api_spider (videoname,audioname,bv_code) VALUES (%s,%s,%s)",(videoname,audioname,bv_code))
       conn.commit()
       cursor.close()
       database_pool.release_conn(conn=conn)

       if returns == 'video':
          cursor,conn = get_cursor()
          cursor.execute(f"SELECT * FROM api_spider WHERE bv_code = %s",(bv_code,))
          data = cursor.fetchone()
          database_pool.release_conn(conn=conn)
          cursor.close()
          if data:
             video_name = data[0][1]
             return FileResponse(settings.VIDEO_STATIC + '/' + video_name,headers={'Content-Disposition': 'attachment'})
          raise HTTPException(status_code=404, detail='视频不存在')
       elif returns == 'audio':
          cursor,conn = get_cursor()
          cursor.execute(f"SELECT * FROM api_spider WHERE bv_code = %s",(bv_code,))
          data = cursor.fetchone()
          database_pool.release_conn(conn=conn)
          cursor.close()
          if data:
             audio_name = data[0][2]
             return FileResponse(settings.VIDEO_STATIC + '/' + audio_name,headers={'Content-Disposition': 'attachment'})
          raise HTTPException(status_code=404, detail='音频不存在')
       else:
           raise HTTPException(status_code=400, detail='参数错误')
 except Exception as e:
     logger.error(f"在爬取视频的时候发生了一个异常: {e}")
 finally:
     if cursor:
         cursor.close()
     if conn:
         database_pool.release_conn(conn=conn)
