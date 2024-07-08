"""
Entry point to all the scripts.
"""

import argparse
import pandas as pd
import os
from pathlib import Path

from src.utils import split_df
from src.process import process_childes
from src.phonemize import phonemize_utterances, character_split_utterance, langcodes

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
        out_path = path / f'{args.collection if args.corpus is None else args.corpus}.csv'
        utts.to_csv(out_path)
        print(f'Saving {len(utts)} utterances to {out_path}')

def process(args):
    """ 
    Processes a CHILDES CSV file or folder of CSV files, cleaning utterances, finding child and adult utterances, and phonemizing utterances.
    """
    
    path = args.path
    out_path = args.out_path
    keep_child_utterances = args.keep_child_utterances
    max_age = args.max_age
    split = args.split
    
    # Process CHILDES CSV file or folder of CSV files
    df = process_childes(path)

    # Remove rows above max age if desired
    if max_age is not None:
        num_above_max = len(df[df['target_child_age'] > max_age])
        df = df[df['target_child_age'] <= max_age]
        print(f'Removed {num_above_max} utterances above {max_age} months. Now have {len(df)} utterances below this age.')

    # Remove child utterances if desired
    if not keep_child_utterances:
        num_child = len(df[df['is_child']])
        df = df[~df['is_child']]
        print(f'Removed {num_child} child utterances. Now have {len(df)} adult utterances.')

    # Phonemize utterances
    lines = df['stem'] if args.language.lower() in ['cantonese', 'mandarin'] else df['processed_gloss']
    df['phonemized_utterance'] = phonemize_utterances(lines, language=args.language)
    num_empty = len(df[df['phonemized_utterance'] == ''])
    print(f'WARNING: {num_empty} lines were not phonemized successfully. Dropping these.')
    df = df[df['phonemized_utterance'] != '']
    df['language_code'] = langcodes[args.language.lower()]
    df['character_split_utterance'] = character_split_utterance(df['processed_gloss'])

    # Print statistics
    print(f'Total corpora: {len(df["corpus_id"].unique())}')
    print(f'Total speakers: {len(df["speaker_id"].unique())}')
    print(f'Total target children: {len(df["target_child_id"].unique())}')
    print('Total lines:', len(df))
    num_words = sum([line.count('WORD_BOUNDARY') for line in df['phonemized_utterance']])
    num_phonemes = sum([len(line.split()) for line in df['phonemized_utterance']]) - num_words
    print('Total words:', num_words)
    print('Total phonemes:', num_phonemes)

    # Save dataframe
    out_path.mkdir(exist_ok=True, parents=True)
    if split:
        train, valid = split_df(df)
        train.to_csv(out_path / 'train.csv')
        print(f'Saved train set to {out_path / "train.csv"} with a total of {len(train)} utterances.')
        valid.to_csv(out_path / 'valid.csv')
        print(f'Saved valid set to {out_path / "valid.csv"} with a total of {len(valid)} utterances.')
        print(f'Saved train and valid sets to {out_path}')
    else:
        df.to_csv(out_path / 'processed.csv')
        print(f'Saved processed dataset to {out_path / "processed.csv"} with a total of {len(df)} utterances.')

def extract(args):
    """ Extracts utterances from a processed dataset. """

    path = args.path
    out_path = args.out_path
    max_age = args.max_age
    target_column = args.column

    if not path.exists():
        raise FileNotFoundError(f'Path {path} does not exist.')
    
    df = pd.read_csv(path)
    if max_age is not None:
        df = df[df['target_child_age'] <= max_age]

    if target_column not in df.columns:
        raise ValueError(f'Target column "{target_column}" not found in DataFrame. Columns found: {df.columns}')

    utterances = df[target_column]
    out_path.mkdir(exist_ok=True, parents=True)
    out_file = out_path / 'utterances.txt'
    open(out_file, 'w').writelines('\n'.join(utterances))
    print(f'Wrote {len(utterances)} utterances to: {out_file}')

# Hacky way to set the espeak library path
import os
os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = '/opt/local/lib/libespeak-ng.dylib'

parser = argparse.ArgumentParser(description="Childes Processor")
subparsers = parser.add_subparsers(help='sub-command help')
parser_download = subparsers.add_parser('download', help='Download utterances from CHILDES into a CSV')
parser_download.add_argument('collection', help='Name of the collection that the corpus is contained within (e.g. Eng-NA)')
parser_download.add_argument('-c', '--corpus', default=None, help='Name of the corpus to download (e.g. Warren). If not provided, will download from entire collection instead.')
parser_download.add_argument('-o', '--out_path', default='childes', type=Path, help='Directory to save utterances to')
parser_download.add_argument('-s', '--separate_by_child', action='store_true', help='Create a separate output file for each child in the corpus')
parser_download.set_defaults(func=download)

parser_process = subparsers.add_parser('process', help='Processes downloaded CHILDES CSV(s), cleaning utterances, phonemizing utterances and ordering by target child age.')
parser_process.add_argument('path', type=Path, help='CHILDES CSV file or folder of CSVs to extract from')
parser_process.add_argument('language', type=str, help='Language used to phonemize. Choices: {}'.format(', '.join(langcodes)))
parser_process.add_argument('-o', '--out_path', default='processed', type=Path, help='Directory where processed datasets will be saved')
parser_process.add_argument('-k', '--keep_child_utterances', action='store_true', help='Keep the child utterances in the dataset. Otherwise will only store adult utterances.')
parser_process.add_argument('-m', '--max_age', default=None, type=int, help='Maximum age in months to include. If not provided, will include all ages.')
parser_process.add_argument('-s', '--split', action='store_true', help='Produce three datasets according to a train-valid-test split of 90-5-5. Splitting is interleaved, not sequential.')
parser_process.set_defaults(func=process)

parser_extract = subparsers.add_parser('extract', help='Takes a processed CSV and extracts a column, splitting child and adult utterances if desired.')
parser_extract.add_argument('path', type=Path, help='Text file containing the utterances to phonemize')
parser_extract.add_argument('column', type=str, help='Column of the dataset to extract. Likely "phonemized_utterance", "character_split_utterance" or "processed_gloss".')
parser_extract.add_argument('-o', '--out_path', default='utterances.txt', type=Path, help='File where extracted utterances will be saved.')
parser_extract.add_argument('-m', '--max_age', default=None, type=int, help='Maximum age in months to include. If not provided, will include all ages.')
parser_extract.set_defaults(func=extract)

args = parser.parse_args()
if args.func == download:
    # Only import childespy if downloading from CHILDES, since it re-downloads childesr each time
    print ('Importing childespy')
    from childespy import get_utterances
args.func(args)
