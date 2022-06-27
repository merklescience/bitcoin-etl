from typing import Optional
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.kafka_item_exporter import KafkaItemExporter


def get_item_exporter(output, topic: Optional[str] = None):
    item_type_to_topic_mapping = {
                                     "block": topic + ".blocks",
                                     "transaction": topic + ".transactions",
                                 }

    if output == "pubsub":
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping=item_type_to_topic_mapping,
            message_attributes=('item_id',))
    elif output == "kafka":
        item_exporter = KafkaItemExporter(
            item_type_to_topic_mapping=item_type_to_topic_mapping,
            message_attributes=('item_id',))
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
