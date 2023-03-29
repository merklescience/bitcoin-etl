from blockchainetl.constants import TOPIC_NAMES_POSTFIX_MAP
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


def get_item_exporter(output, topic_prefix, flatten_data):
    item_type_to_topic_mapping = dict()

    if topic_prefix:
        item_type_to_topic_mapping.update({
            topic_name: topic_prefix + topic_value for topic_name, topic_value in TOPIC_NAMES_POSTFIX_MAP.items()
        })

    if output == "gcp":
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping=item_type_to_topic_mapping,
            message_attributes=('item_id',), flatten_data=flatten_data)
    elif output == "kafka":
        from blockchainetl.jobs.exporters.kafka_item_exporter import KafkaItemExporter
        item_exporter = KafkaItemExporter(item_type_to_topic_mapping, flatten_data=flatten_data)
    else:
        item_exporter = ConsoleItemExporter(flatten_data=flatten_data)

    return item_exporter
