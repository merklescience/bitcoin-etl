# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from confluent_kafka import Producer

# from kafka import KafkaProducer
import logging

import socket
import json


class KafkaItemExporter:
    def __init__(self, topic= "ltc-bd-txns-hot" ) -> None:
        logging.basicConfig(
            level=logging.INFO,
            # filename="/data/mempool/mempool.log",
            filename="msessage-publish.log",
            format='{"time" : "%(asctime)s", "level" : "%(levelname)s" , "message" : "%(message)s"}',
        )

        conf = {
            "bootstrap.servers": "104.197.163.1:9092",
            "client.id": socket.gethostname(),
            "message.max.bytes" : 5242880,
        }
        producer = Producer(conf)
        self.producer = producer
        self.logging = logging.getLogger(__name__)
        self.topic = topic

    def open(self):
        pass

    def export_items(self, items):
        for item in items:
            self.export_item(item)
            self.write_hot_txns(json.dumps(item, separators=(",", ":")))

    def export_item(self, item):
        print(json.dumps(item, separators=(",", ":")))
        self.write_hot_txns(json.dumps(item, separators=(",", ":")))

    def close(self):
        pass

    def write_hot_txns(self, enriched_data: str):
        def acked(err, msg):
            if err is not None:
                self.logging.error(
                    "Failed to deliver message: %s: %s" % (str(msg), str(err))
                )
            else:
                self.logging.info("Message produced: %s" % msg)

        self.producer.produce(
            self.topic, key="", value=enriched_data, callback=acked
        )
        self.producer.poll(1)
