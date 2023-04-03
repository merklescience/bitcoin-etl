import logging

logger = logging.getLogger(__name__)

blocks_fieldnames = [
    "hash",
    "number",
    "timestamp",
    "median_timestamp",
    "merkle_root",
    "coinbase_param",
    "coinbase_param_decoded",
    "coinbase_txid",
    "nonce",
    "difficulty",
    "chain_work",
    "version",
    "version_hex",
    "size",
    "stripped_size",
    "weight",
    "bits",
    "block_reward",
]

transactions_fieldnames = [
    "transaction_id",
    "hash",
    "block_number",
    "block_hash",
    "block_timestamp",
    "is_coinbase",
    "lock_time",
    "size",
    "virtual_size",
    "weight",
    "version",
    "input_count",
    "output_count",
    "input_value",
    "output_value",
]

inputs_fieldnames = [
    "index",
    "create_transaction_id",
    "spending_transaction_id",
    "create_output_index",
    "script_asm",
    "script_hex",
    "required_signatures",
    "addresses",
    "value",
    "type"
]

outputs_fieldnames = [
    "index",
    "create_transaction_id",
    "script_asm",
    "script_hex",
    "required_signatures",
    "addresses",
    "value",
    "type"
]


class ClickhouseConvertor:

    @classmethod
    def append_to_field(cls, transaction, field_name, field_value):
        if field_name not in transaction:
            transaction[field_name] = []
        transaction[field_name].append(field_value)

    @classmethod
    def convert_blocks(cls, transaction):
        converted_block_data = {}
        for field in blocks_fieldnames:
            field_value = str(transaction[field])
            if field_value is None or field_value == "None":
                field_value = ""
            converted_block_data[field] = field_value
        converted_block_data['coin_price_usd'] = 0.0
        return converted_block_data

    @classmethod
    def convert_transactions(cls, transaction):
        converted_transaction_data = {}

        for field in transactions_fieldnames:
            field_value = str(transaction[field])
            if field == "is_coinbase":
                if field_value == "True":

                    field_value = "1"
                else:
                    field_value = "0"
            if field_value is None or field_value == "None":
                field_value = ""
            converted_transaction_data[field] = field_value

        converted_transaction_data['coin_price_usd'] = 0.0
        for each_input in transaction['inputs']:
            for field in inputs_fieldnames:
                field_value = each_input[field]
                if field_value is None or field_value == "None":
                    field_value = ""
                if field == "addresses":
                    cls.append_to_field(converted_transaction_data, 'inputs.' + field, str(",".join(field_value)))
                else:
                    cls.append_to_field(converted_transaction_data, 'inputs.' + field, str(field_value))

        for each_output in transaction['outputs']:
            for field in outputs_fieldnames:
                field_value = each_output[field]
                if field_value is None or field_value == "None":
                    field_value = ""
                if field == "addresses":
                    cls.append_to_field(converted_transaction_data, 'outputs.' + field, str(",".join(field_value)))
                else:
                    cls.append_to_field(converted_transaction_data, 'outputs.' + field, str(field_value))

        return converted_transaction_data
