# kafka handler

from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': "192.168.1.100:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)


def kf_produce_msg():
    producer.produce("my-toooopiiic", value="bonjour_kafka_from_python_producer")
    producer.flush()

