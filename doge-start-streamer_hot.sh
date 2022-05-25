#!/usr/bin/bash
rm last_synced_block_hot.txt
python3 bitcoinetl.py stream -o kafka -l last_synced_block_hot.txt --provider-uri "https://c9jo6uo5qqklbcv160jg.bdnodes.net?auth=sYJ5Yk1PNhZAF0hXUhVow-GQDxrW_H2UZCXOtcTD0Bo" --chain dogecoin -s $1 
# --kafka-topic-name $2