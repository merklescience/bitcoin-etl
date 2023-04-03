NEWLY_GENERATED_COINS = "Newly Generated Coins"

# BASE TOPIC NAMES
TOPIC_BLOCK = "block"
TOPIC_TRANSACTION = "transaction"

# TG TOPIC NAMES
TG_LINK_INPUTS = "tg_link_inputs"
TG_LINK_OUTPUTS = "tg_link_outputs"
TG_LINK_FLAT = "tg_link_flat"
TG_TRANSACTION = "tg_transaction"

# CH TOPIC NAMES
CH_BLOCK = "ch_block"
CH_TRANSACTION = "ch_transaction"


# map of topic name and postfix value to be added to topic prefix
TOPIC_NAMES_POSTFIX_MAP = {
    TOPIC_BLOCK: ".blocks",
    TOPIC_TRANSACTION: ".transactions",
    TG_LINK_INPUTS: ".tg.link_inputs",
    TG_LINK_OUTPUTS: ".tg.link_outputs",
    TG_LINK_FLAT: ".tg.link_flat",
    TG_TRANSACTION: ".tg.transactions",
    CH_BLOCK: ".ch.blocks",
    CH_TRANSACTION: ".ch.transactions",
}
