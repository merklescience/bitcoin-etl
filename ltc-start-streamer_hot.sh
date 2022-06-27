#!/usr/bin/bash
rm last_synced_block_hot.txt
python3 bitcoinetl.py stream -o kafka -t ltc.hote2dedf -l last_synced_block_hot.txt --provider-uri "https://c9kn23u3s29nn567vq7g.bdnodes.net?auth=Wm-EfF7sEGhFMxJTcsJtF0cY-KQ-MmcCmVLnR9eKyQ8" -s $1