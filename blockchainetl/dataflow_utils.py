from blockchainetl.constants import NEWLY_GENERATED_COINS


def get_addresses(input_or_output_item):
    return ",".join(input_or_output_item["addresses"])


def get_grouped_inputs_or_outputs(inputs_or_outputs):
    data = {}

    for each_item in inputs_or_outputs:
        addresses = get_addresses(each_item)
        if not each_item["type"]:
            data[""] = 0
        elif addresses in data:
            data[addresses] += each_item["value"]
        else:
            data[addresses] = each_item["value"]

    return data


def transform_transaction_link_inputs_output_data(transaction, evaluate_input=True):
    """
    This function take transaction data and convert it into daily_link_inputs job format
    transaction_Id,input_address_value,input_address/10^8,(input_address/10^8)*latest_price

    transaction: transaction data
    input: If True it calculates value for input_addresses else calculate for output addresses
    """

    link_data = []
    transaction_id = transaction["transaction_id"]
    input_or_output_addresses = transaction["inputs"] if evaluate_input else transaction["outputs"]
    grouped_inputs_or_outputs = get_grouped_inputs_or_outputs(input_or_output_addresses)

    if evaluate_input and transaction.get("is_coinbase"):
        link_data.append({
            "transaction_id": transaction_id,
            "addresses": NEWLY_GENERATED_COINS,
            "input_value": 0
        })

    for each_input_or_output in input_or_output_addresses:
        addresses = get_addresses(each_input_or_output)
        input_value = grouped_inputs_or_outputs.get(addresses) / 10**8
        link_data.append({
            "transaction_id": transaction_id,
            "addresses": addresses,
            "input_value": input_value
        })
    return link_data


def flatten_input_output_addresses_data(transaction, add_flattened_data=False):
    """
    this function loops through input and outputs addresses and does cartesian product of it
    transaction : transaction data
    add_flattened_data: Boolean, If True will add flattened data to transaction data else just return the flattened data
    """
    link_flat = []
    block_timestamp = transaction.get("block_timestamp")

    if not (transaction.get("outputs") and transaction.get("inputs")):
        return

    for each_output in transaction.get("outputs"):
        for each_input in transaction.get("inputs"):
            link_flat.append({
                "input_address": get_addresses(each_input),
                "output_address": get_addresses(each_output),
                "block_timestamp": block_timestamp
            })

    add_flattened_data and transaction.update({"flattened_data": link_flat})
    return link_flat



def get_transaction_data(transaction):
    transaction_data = []
    transaction_id = transaction["transaction_id"]

    transaction_data.append({
        "transaction_id": transaction_id,
        "output_value": transaction["output_value"] / 10 ** 8,
        "block_timestamp": transaction["block_timestamp"],
        "fee": transaction["fee"]
    })

    return transaction_data


def transform_transaction_data(transaction, add_flattened_data):
    link_inputs = transform_transaction_link_inputs_output_data(transaction)
    link_outputs = transform_transaction_link_inputs_output_data(transaction, evaluate_input=False)
    link_flat = flatten_input_output_addresses_data(transaction, add_flattened_data)
    transaction_data = get_transaction_data(transaction)
    return link_inputs, link_outputs, link_flat, transaction_data
