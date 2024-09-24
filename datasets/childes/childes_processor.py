"""
Entry point for downloading, processing and extracting data from CHILDES.
"""
import argparse
import pandas as pd
import json
import logging
from pathlib import Path

from childes_processor.processor import PHONEMIZER_CONFIG_PATH, ChildesProcessor
from childes_processor.downloader import ChildesDownloader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def download(args):
    """ Downloads utterances from CHILDES using `childespy`"""

    downloader = ChildesDownloader()
    downloader.download(args.collection, args.corpus, args.out_path, args.separate_by_child)

def process(args):
    """ 
    Processes a CHILDES CSV file or folder of CSV files, cleaning utterances, finding child and adult utterances, and phonemizing utterances.
    """
    
    processor = ChildesProcessor(args.path, args.keep_child_utterances, args.max_age)
    processor.phonemize_utterances(args.language)
    processor.character_split_utterances()
    processor.print_statistics()

    if args.split:
        processor.save_splits(args.out_path)
    else:
        processor.save_df(args.out_path)

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
    logger.info(f'Wrote {len(utterances)} utterances to: {out_file}')

def main():
    
    languages = json.load(open(PHONEMIZER_CONFIG_PATH)).keys()

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
    parser_process.add_argument('language', type=str, help='Language used to phonemize. Choices: {}'.format(', '.join(languages)))
    parser_process.add_argument('-o', '--out_path', default='processed', type=Path, help='Directory where processed datasets will be saved')
    parser_process.add_argument('-k', '--keep_child_utterances', action='store_true', help='Keep the child utterances in the dataset. Otherwise will only store adult utterances.')
    parser_process.add_argument('-m', '--max_age', default=None, type=int, help='Maximum age in months to include. If not provided, will include all ages.')
    parser_process.add_argument('-s', '--split', action='store_true', help='Produce three datasets according to a train-valid-test split of 90-5-5. Splitting is interleaved, not sequential.')
    parser_process.set_defaults(func=process)

    parser_extract = subparsers.add_parser('extract', help='Takes a processed CSV and extracts a column, splitting child and adult utterances if desired.')
    parser_extract.add_argument('path', type=Path, help='Processed CSV file to extract from')
    parser_extract.add_argument('column', type=str, help='Column of the dataset to extract. Likely "phonemized_utterance", "character_split_utterance" or "processed_gloss".')
    parser_extract.add_argument('-o', '--out_path', default='utterances.txt', type=Path, help='File where extracted utterances will be saved.')
    parser_extract.add_argument('-m', '--max_age', default=None, type=int, help='Maximum age in months to include. If not provided, will include all ages.')
    parser_extract.set_defaults(func=extract)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
