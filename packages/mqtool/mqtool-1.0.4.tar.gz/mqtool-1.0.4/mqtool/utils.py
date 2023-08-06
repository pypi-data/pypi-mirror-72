import json
import logging
from uuid import uuid1
import requests
# import base64
# import numpy as np
# import cv2
# from fdfs_client.client import *


def http_post(url, json_data):
    json_data = json.dumps(json_data)
    with requests.session() as s:
        s.keep_alive = False
        headers = {'Content-Type': 'application/json'}
        response = s.post(url=url, data=json_data, headers=headers)
        json_res = response.json()
        logger.info("http_post result:"+str(json_res))
    return json_res

# def readfile(imgId):
#     tracker_path = get_tracker_conf('/etc/fdfs/client.conf')
#     client = Fdfs_client(tracker_path)
#     ret_read = client.download_to_buffer(imgId.encode())
#     nparr = np.fromstring(ret_read['Content'], np.uint8)
#     img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     # img = cv2.cvtColor(img_decode, cv2.COLOR_BGR2RGB)
#     return img_decode
#
#
# def readfrombase64(imgstr):
#     if 'base64,' in imgstr:
#         i = imgstr.index('base64,') + 7
#         imgstr = imgstr[i:]
#     imgData = base64.decodebytes(imgstr.encode())
#     nparr = np.fromstring(imgData, np.uint8)
#     img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     return img_decode
#
#
# def uploadfile(thumbnail):
#     tracker_path = get_tracker_conf('/etc/fdfs/client.conf')
#     client = Fdfs_client(tracker_path)
#     img_encode = cv2.imencode('.jpg', thumbnail)[1]
#     data_encode = np.array(img_encode)
#     str_encode = data_encode.tostring()
#     subimg_key = client.upload_by_buffer(str_encode)
#     thumbnail_id = subimg_key['Remote file_id']
#     return thumbnail_id

def init_log():
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    if len(logger.handlers) == 0:
        # handler = logging.FileHandler("log.txt")
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        # pathname
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d[%(funcName)s] - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = init_log()


# 生成8位短uuid
uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid1()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


def get_short_uuids(length):
    uuid_list = [short_uuid() for i in range(length)]
    return uuid_list


def isEmpty(obj):
    """
    对象是否为空
    :param obj:
    :return:
    """
    return True if (obj is None or len(obj) == 0) else False


# # 暂定
# def get_db(user, password, ip, instance='orcl', port=1521):
#     engine_str = 'oracle://%s:%s@%s:%s/%s' % (user, password, ip, port, instance)
#     engine = create_engine(engine_str, encoding='utf-8')
#     return engine
#
#
# # 暂定
# def get_mysql(user, password, ip, db, port=3306):
#     engine_str = f'mysql+pymysql://{user}:{password}@{ip}:{port}/{db}'
#     engine = create_engine(engine_str, encoding='utf-8')
#     return engine
#
#
# # 暂定
# def get_pg(user="postgres", password="", ip="10.2.111.1", db="mydb", port=5432):
#     engine_str = f'postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db}'
#     engine = create_engine(engine_str, encoding='utf-8')
#     return engine
