"""
If the path points to a CHILDES corpora CSV file, extracts the child and child-directed utterances
and places them in a new folder with the same name as the CSV file. 
If the path points to a folder, extracts the child and child-directed utterances in every CSV
file found in that directory and concatenates them.

Example usage:
    python -m scripts.process_corpus data/corpora/Manchester/Warren.csv

TODO: There is currently an issue where if the utterance is just the word "nan", aochildes
will fail (pandas will try to load "nan" as a float, rather than a string and a regex match
fails). Current fix involves adding a line in aochildes/pipeline.py to cast "gloss" to a string.

"""

import sys, shutil, os
import pandas as pd
from pathlib import Path

from aochildes.helpers import Transcript, col2dtype, punctuation_dict
from aochildes.dataset import ChildesDataSet
from aochildes.params import ChildesParams
from aochildes.pipeline import Pipeline
from aochildes.configs import Dirs

#TODO: Extract collection names automatically
collection_names = ['Eng-NA', 'Eng-UK']
OUT_PATH = Path('.')

path = Path(sys.argv[1])
if path.is_dir():
    transcripts = path
else:
    # Temporarily copy csv file to a new folder since AOChildes takes a folder for processing
    transcripts = path.parent / path.stem
    transcripts.mkdir(exist_ok=True)
    shutil.copy(path, transcripts)

# Have AOChildes use our saved transcripts
Dirs.transcripts = transcripts

# Using the pre-processing from aochildes to extract child and adult utterances
adult_data = ChildesDataSet(ChildesParams(collection_names=collection_names))
adult_utterances = adult_data.load_sentences()
print("Number of adult utterances: {:>8,}".format(len(adult_utterances)))

all_speakers = adult_data.pipeline.df.groupby("speaker_role").size()
# Exclude all adult utterances from child data, as well as non-target-child utterances
all_but_target_child = list(all_speakers.keys()) + ['Child']

child_data = ChildesDataSet(ChildesParams(bad_speaker_roles=all_but_target_child, collection_names=collection_names))
child_utterances = child_data.load_sentences()
print("Number of child utterances: {:>8,}".format(len(child_utterances)))

def write_sentences(path, sentences):
    if path.exists():
        path.unlink()

    with path.open('w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')

write_sentences(OUT_PATH / '{}_child.txt'.format(path.stem), child_utterances)
write_sentences(OUT_PATH / '{}_adult.txt'.format(path.stem), adult_utterances)
if not path.is_dir():
    copied_file = transcripts / path.name
    copied_file.unlink()
    os.rmdir(transcripts)
