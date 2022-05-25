from typing import Optional
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.kafka_item_exporter import KafkaItemExporter


def get_item_exporter(output,kafka_topic: Optional[str] = None):
    if output == "pubsub":
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping={
                "block": output + ".blocks",
                "transaction": output + ".transactions",
            },
            message_attributes=('item_id',))
    elif output == "kafka":
        item_exporter = KafkaItemExporter(topic=kafka_topic)
        # if lag == 0 :
        # else:
        #     item_exporter = KafkaItemExporter(topic="ltc-bd-txns-warm")
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
