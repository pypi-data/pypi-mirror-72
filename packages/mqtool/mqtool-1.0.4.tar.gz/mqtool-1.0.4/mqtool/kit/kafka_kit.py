from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


class Kafka_producer():
    """
    生产模块：根据不同的key，区分消息
    """

    def __init__(self, bootstrap_servers, kafkatopic, key=None, is_json=False):
        self.bootstrap_servers = bootstrap_servers
        self.kafkatopic = kafkatopic
        self.key = key
        self.is_json = is_json
        if is_json:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                          value_serializer=lambda v: json.dumps(v,ensure_ascii=False).encode())
        else:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def send_df(self, message, topic=None):
        try:
            if topic is None:
                topic = self.kafkatopic
            producer = self.producer
            if self.is_json:
                producer.send(topic, message, key=self.key)
            else:
                producer.send(topic, key=self.key, value=message.encode())  # 注意转换
            producer.flush()
        except KafkaError as e:
            print(e)


class Kafka_consumer():

    def __init__(self, bootstrap_servers, kafkatopic, groupid=None, key=None, auto_offset_reset='latest'):
        self.bootstrap_servers = bootstrap_servers
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.key = key
        self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid,
                                      auto_offset_reset=auto_offset_reset, bootstrap_servers=self.bootstrap_servers,
                                      enable_auto_commit=False)

    def assign(self):
        assignment = []
        count = 0
        while len(assignment) == 0 and count < 100:
            self.consumer.poll(100)
            assignment = self.consumer.assignment()
            count += 1
        return assignment

    def read_df(self, seek_end=True):
        if seek_end:
            assignment = self.assign()
            if len(assignment) > 0:
                self.consumer.seek_to_end(*assignment)
        try:
            for message in self.consumer:
                self.consumer.commit()
                yield message.value  # 返回迭代器
        except Exception as e:
            print(e)
