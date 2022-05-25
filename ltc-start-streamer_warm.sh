#!/usr/bin/bash
rm last_synced_block_warm.txt
python3 bitcoinetl.py stream -o kafka -l last_synced_block_warm.txt --lag 12  --provider-uri "https://c9kn23u3s29nn567vq7g.bdnodes.net?auth=Wm-EfF7sEGhFMxJTcsJtF0cY-KQ-MmcCmVLnR9eKyQ8" -s $1 --kafka-topic-name $2
