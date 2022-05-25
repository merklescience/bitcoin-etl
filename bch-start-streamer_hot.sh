#!/usr/bin/bash
rm last_synced_block_hot.txt
python3 bitcoinetl.py stream -o kafka -l last_synced_block_hot.txt --provider-uri "https://c9jo4lo5qqklbcv160ig.bdnodes.net/?auth=LFTVaHxAfS3lZ4lCFbRgMaV0UtlNs8v97rg0tgPe6O8" --chain bitcoin_cash -s $1 --kafka-topic-name $2