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
    def __init__(self, topic="dead-letter-topic") -> None:
        logging.basicConfig(
            level=logging.INFO,
            # filename="/data/mempool/mempool.log",
            filename="msessage-publish.log",
            format='{"time" : "%(asctime)s", "level" : "%(levelname)s" , "message" : "%(message)s"}',
        )

        conf = {
            "bootstrap.servers": "pkc-3w22w.us-central1.gcp.confluent.cloud:9092",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "linger.ms":100,
            "message.max.bytes": 5242880,
            "batch.size" : 32 * 1024,
            "sasl.username": "J7VXXU374KGW672N",
            "sasl.password": "46RfgGhqkZcgnj9e0XplI3FsL98GZmSWvTOkmVmJPecrceOD72mkSiuFzxl4q4xA",
        }
        self.producer = Producer(conf)
        self.logging = logging.getLogger(__name__)
        self.topic = topic

    def open(self):
        pass

    def export_items(self, items):
        for item in items:
            self.export_item(item)

    def export_item(self, item):
        self.write_txns(json.dumps(item, separators=(",", ":")), topic=self.topic)

    def close(self):
        pass

    def write_txns(self, enriched_data: str, topic: str):
        def acked(err, msg):
            if err is not None:
                self.logging.error("%% Message failed delivery: %s\n" % err)
            else:
                self.logging.info(
                    "%% Message delivered to %s [%d] @ %d\n"
                    % (msg.topic(), msg.partition(), msg.offset())
                )

        try:
            self.producer.produce(topic, key="", value=enriched_data, callback=acked)
        except BufferError:
            self.logging.error(
                "%% Local producer queue is full (%d messages awaiting delivery): try again\n"
                % len(self.producer)
            )
        except Exception(e):
            self.logging.error("error while pushing " + e)

        self.producer.poll(1)
        # self.logging.info("published "+msgsPublished)
