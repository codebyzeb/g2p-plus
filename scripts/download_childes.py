"""
Download a corpus from CHILDES and save a csv for each target child
#TODO: Use commandline arguments instead of hardcoded variables

"""

import sys
from pathlib import Path
from childespy import get_utterances

CORPUS = sys.argv[1]
COLLECTION = "Eng-NA"
SEPARATE_BY_SPEAKER = False
SAVE_DIR = Path('childes')

utts = get_utterances(collection=COLLECTION, corpus=CORPUS)
speakers = list(utts["target_child_name"].unique())

if SEPARATE_BY_SPEAKER:
    path = SAVE_DIR / f'{CORPUS}'
    if not path.exists():
        path.mkdir()
    for speaker in speakers:
        a = utts[utts["target_child_name"] == speaker]
        out_path = path /f'{speaker}.csv'
        if out_path.exists():
            out_path.unlink()
        a.to_csv(out_path)
else:
    path = SAVE_DIR / f'{COLLECTION}'
    if not path.exists():
        path.mkdir()
    out_path = path / f'{CORPUS}.csv'
    utts.to_csv(out_path)
