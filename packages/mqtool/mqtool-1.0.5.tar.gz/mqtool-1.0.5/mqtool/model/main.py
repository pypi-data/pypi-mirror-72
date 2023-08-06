from mqtool.kit import Kafka_consumer, Kafka_producer
from mqtool.kit.tornado_server import Tornado_http
from mqtool.utils import *


def start():
    return {"status": "algorithm service success"}


def api(data):
    """
    处理data参数，算法运行
    :param data: dict字段类型
    :return:
    """
    if data_type == "kafka":
        if 'picture' in data:
            fdfsKey = data['picture']
            img = readfile(str(fdfsKey))
            data['img'] = img
    elif data_type == "http":
        if 'data' in data:
            img = readfrombase64(data['data'])
            del data['data']
            data['img'] = img
        if 'structure' in data:
            data['structure'] = data['structure'].replace('\"', '')
    return algo(data)


def aistart(run):
    try:
        global algo
        global data_type
        algo = run
        data_type = os.getenv("DATA_TYPE", default="http")
        if data_type == "kafka":
            bootstrap_server = os.getenv("BOOTSTRAP_SERVER")
            kafkatopic = os.getenv("TOPIC")
            storage_url = os.getenv("STORAGE_URL", default="http://localhost:8888/")
            consumer = Kafka_consumer(bootstrap_servers=bootstrap_server, kafkatopic=kafkatopic,
                                      groupid=algo.__name__)
            data = consumer.read_df()
            sinktopic = os.getenv("SINKTOPIC")
            if sinktopic is not None:
                producer = Kafka_producer(bootstrap_servers=bootstrap_server, kafkatopic=sinktopic,
                                          is_json=True)
            for message in data:
                try:
                    logger.info('receive data')
                    mes = json.loads(message.decode())
                    res = api(mes)
                    if res is not None:
                        if isinstance(res, list):
                            for item in res:
                                if sinktopic is not None:
                                    producer.send_df(item)
                                http_post(storage_url, item)
                        else:
                            if sinktopic is not None:
                                producer.send_df(res)
                            http_post(storage_url, res)
                except:
                    logger.exception("deal data error")

        elif data_type == "http":
            tornado_server = Tornado_http()
            # 添加路由
            tornado_server.add_handler("/", start)
            # 数据为json格式
            tornado_server.add_handler("/predict", api, json_type=True, get=False)
            # 开启服务
            tornado_server.start_http_server()
    except:
        logger.exception("system error")
