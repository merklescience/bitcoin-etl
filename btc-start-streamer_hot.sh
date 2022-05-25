#!/usr/bin/bash
rm last_synced_block_hot.txt
python3 bitcoinetl.py stream -o kafka -l last_synced_block_hot.txt --provider-uri "https://c9jo6f85qqklbcv160j0.bdnodes.net?auth=Mf8Z4xLB55U13nVt8fzlbVM7hSTJ8mXnQcUw4VMcpqY" --chain bitcoin -s $1 
#--kafka-topic-name $2