from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter


def get_item_exporter(output, topic_prefix):
    item_type_to_topic_mapping = {
        "block": topic_prefix + ".blocks",
        "transaction": topic_prefix + ".transactions"
    }

    if output == "gcp":
        from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
        item_exporter = GooglePubSubItemExporter(
            item_type_to_topic_mapping=item_type_to_topic_mapping,
            message_attributes=('item_id',))
    elif output == "kafka":
        from blockchainetl.jobs.exporters.kafka_item_exporter import KafkaItemExporter
        item_exporter = KafkaItemExporter(item_type_to_topic_mapping)
    else:
        item_exporter = ConsoleItemExporter()

    return item_exporter
