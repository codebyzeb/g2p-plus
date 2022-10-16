"""
Entry point to all the scripts.
"""

import argparse
from re import T
import pandas as pd
import sys, shutil, os
from pathlib import Path
from phonemizer import phonemize
from phonemizer.separator import Separator
from aochildes.dataset import AOChildesDataSet
from aochildes.params import AOChildesParams
from aochildes.configs import Dirs

def download(args):
    """ Downloads utterances from CHILDES using `childespy`"""

    # TODO: Add ability to download from entire collection (e.g. Eng-NA)

    print(f'\n\nAttempting to get utterances from the "{args.corpus}" corpus in the "{args.collection}" collection:\n')
    utts = get_utterances(collection=args.collection, corpus=args.corpus)
    speakers = list(utts["target_child_name"].unique())
    path = args.out_path / f'{args.collection}'

    if args.separate_by_child:
        path = path / f'{args.corpus}'
        if not path.exists():
            path.mkdir(parents=True)
        for speaker in speakers:
            a = utts[utts["target_child_name"] == speaker]
            out_path = path /f'{speaker}.csv'
            if out_path.exists():
                out_path.unlink()
            print(f'Saving {len(a)} utterances to {out_path}')
            a.to_csv(out_path)
    else:
        if not path.exists():
            path.mkdir(parents=True)
        out_path = path / f'{args.corpus}.csv'
        utts.to_csv(out_path)
        print(f'Saving {len(utts)} utterances to {out_path}')

def extract(args):
    """ 
    If the path points to a CHILDES corpora CSV file, extracts the child and child-directed utterances
    and places them in a new folder with the same name as the CSV file. 
    If the path points to a folder, extracts the child and child-directed utterances in every CSV
    file found in that directory and concatenates them.
    """

    path = args.path
    out_path = args.out_path
    transcripts = path
    if path.is_dir():
        print('Path is a directory, will extract utterances from all CSVs found in this directory.')
    else:
        print('Path is a CSV file, will only extract utterances from this file.')
        # Temporarily copy csv file to a new folder since AOChildes takes a folder for processing
        transcripts = path.parent / ('tmp_' + path.stem)
        print(f'Creating temporary directory {transcripts}')
        transcripts.mkdir(exist_ok=True)
        shutil.copy(path, transcripts)

    csvs = [p for p in list(transcripts.iterdir()) if p.suffix == '.csv']
    print(f'Found {len(csvs)} CSVs in {transcripts}')
    collection_names = []
    for csv in csvs:
        a = pd.read_csv(csv)
        collection_names.extend(list(a.collection_name.unique()))
    collection_names = list(set(collection_names))
    print(f'Found collection names: {collection_names}')

    # Have AOChildes use our saved transcripts
    Dirs.transcripts = transcripts

    # Using the pre-processing from aochildes to extract child and adult utterances
    print('\n--Using AOChildes to extract adult utterances:--')
    adult_data = AOChildesDataSet(AOChildesParams(collection_names=collection_names))
    adult_utterances = adult_data.load_sentences()
    print(f'--Number of adult utterances: {len(adult_utterances)}--')

    # Exclude all adult utterances from child data, as well as non-target-child utterances
    all_speakers = adult_data.pipeline.df.groupby("speaker_role").size()
    all_but_target_child = list(all_speakers.keys()) + ['Child']

    print('\n--Using AOChildes to extract child utterances:--')
    child_data = AOChildesDataSet(AOChildesParams(bad_speaker_roles=all_but_target_child, collection_names=collection_names))
    child_utterances = child_data.load_sentences()
    print(f'--Number of child utterances: {len(child_utterances)}--\n')

    out_path.mkdir(exist_ok=True)
    child_out = out_path / 'child.txt'
    adult_out = out_path / 'adult.txt'
    open(child_out, 'w').writelines('\n'.join(child_utterances))
    print(f'Wrote child utterances to: {child_out}')
    open(adult_out, 'w').writelines('\n'.join(adult_utterances))
    print(f'Wrote adult utterances to: {adult_out}')

    if not path.is_dir():
        copied_file = transcripts / path.name
        copied_file.unlink()
        print(f'Deleting temporary directory {transcripts}')
        os.rmdir(transcripts)

def phonemize_file(args):
    """ Uses phonemizer to phonemize a text """

    lines = open(args.path, 'r').readlines()

    phn = phonemize(
        lines,
        language=args.language,
        backend='espeak',
        separator=Separator(phone=' ', word=' ;eword ', syllable=''),
        strip=True,
        preserve_punctuation=False,
        njobs=4)

    # TODO: make directory if doesnt exist
    with open(args.out_path, 'w') as f:
        f.writelines(' ;eword \n'.join(phn))

parser = argparse.ArgumentParser(description="Childes Processor")
subparsers = parser.add_subparsers(help='sub-command help')
parser_download = subparsers.add_parser('download', help='Download utterances from CHILDES into a CSV')
parser_download.add_argument('corpus', help='Name of the corpus to download')
parser_download.add_argument('collection', help='Name of the collection that the corpus is contained within')
parser_download.add_argument('-o', '--out_path', default='childes', type=Path, help='Directory to save utterances to')
parser_download.add_argument('-s', '--separate_by_child', action='store_true', help='Create a separate output file for each child in the corpus')
parser_download.set_defaults(func=download)

parser_extract = subparsers.add_parser('extract', help='Extract utterances from a CSV, separating child and child-directed speech')
parser_extract.add_argument('path', type=Path, help='CSV file of utterances or folder of utterances to extract from')
parser_extract.add_argument('-o', '--out_path', default='processed', type=Path, help='Directory to save utterances to')
parser_extract.set_defaults(func=extract)

parser_phonemize = subparsers.add_parser('phonemize', help='Takes a txt file of utterances and returns a phonemized file')
parser_phonemize.add_argument('path', type=Path, help='Text file containing the utterances to phonemize')
# TODO: limit language to certain options or test if ok
parser_phonemize.add_argument('language', type=str, help='Language used to phonemize')
parser_phonemize.add_argument('-o', '--out_path', default='phonemized.txt', type=Path, help='File to save utterances to')
parser_phonemize.set_defaults(func=phonemize_file)

args = parser.parse_args()
if args.func == download:
    # Only import childespy if downloading from CHILDES, since it re-downloads childesr each time
    print ('Importing childespy')
    from childespy import get_utterances
args.func(args)
