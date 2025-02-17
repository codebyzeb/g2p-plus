""" Process CHILDES CSV files."""

import json
from pathlib import Path
import pandas as pd
import re 
import logging
import sys

from .dicts import w2string, string2w, punctuation_dict, col2dtype

top_level_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(top_level_dir))

from corpus_phonemizer import character_split_utterances, phonemize_utterances

PHONEMIZER_CONFIG_PATH = Path(__file__).parent / 'phonemizer_config.json'

def _clean_english(sentence, type):
    """ Copied from AOChildes pipeline.py. Fixes spelling, punctuation, and word pairs for English CHILDES sentences. """

    sentence = str(sentence)

    # Fix word pairs 
    for string in string2w:
        if string in sentence:
            sentence = sentence.replace(string, string2w[string])

    # consistent question marking
    if (sentence.startswith('what') and not sentence.startswith('what a ')) or \
            sentence.startswith('where') or \
            sentence.startswith('how') or \
            sentence.startswith('who') or \
            sentence.startswith('when') or \
            sentence.startswith('you wanna') or \
            sentence.startswith('do you') or \
            sentence.startswith('can you'):
        sentence += '?'
    else:
        sentence += f'{punctuation_dict[type]}' if type in punctuation_dict else '.'

    words = []
    for w in str(sentence).split():
        w = w.lower()
        # fix spelling
        if w in w2string:
            w = w2string[w.lower()]
        # split compounds
        w = w.replace('+', ' ').replace('_', ' ')
        words.append(w)
    
    return ' '.join(words)

def _clean(sentence, type):
    """ Process a CHILDES sentence. Lowercase, add punctuation and split compounds."""

    sentence = str(sentence)
    if not type in punctuation_dict:
        sentence += '. '
    else:
        sentence += f' {punctuation_dict[type]}'
    words = []
    for w in str(sentence).split():
        w = w.lower()
        # split compounds
        w = w.replace('+', ' ').replace('_', ' ')
        words.append(w)
    return ' '.join(words)

class ChildesProcessor:
    """
    Processes CHILDES CSV files.
    """
    
    def __init__(self, path: Path, keep_child_utterances: bool = True, max_age: int = None):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.df = self.load_data(path)
    
        if max_age is not None:
            num_above_max = len(self.df[self.df['target_child_age'] > max_age])
            self.df = self.df[self.df['target_child_age'] <= max_age]
            self.logger.info(f'Removed {num_above_max} utterances above {max_age} months. Now have {len(self.df)} utterances below this age.')

        if not keep_child_utterances:
            num_child = len(self.df[self.df['is_child']])
            self.df = self.df[~self.df['is_child']]
            self.logger.info(f'Removed {num_child} child utterances. Now have {len(self.df)} adult utterances.')
    
    def load_data(self, path: Path):
        """ Given a path to a CHILDES CSV file, or a folder of CHILDES CSV files, prepare the data for training, returning a DataFrame.
        
        Carries out the following:
        1. Keep only the columns specified in col2dtype.
        2. Remove rows with negative number of tokens or no tokens.
        3. Add a column 'is_child' to indicate whether the speaker is a child.
        4. Sort the DataFrame by target_child_age and transcript_id.
        5. Remove rows that have nonsense words.
        6. Clean each sentence with some simple preprocessing (fixing spelling if in English).

        Args:
            path (Path): Path to a CHILDES CSV file or folder of CHILDES CSV files.
        
        """

        if not path.exists():
            raise FileNotFoundError(f'Path {path} does not exist.')
        if path.is_dir():
            self.logger.info('Path is a directory, will extract utterances from all CSVs found in this directory.')
            transcripts = path
        else:
            self.logger.info('Path is a file, will extract utterances from this CSV.')
            transcripts = [path]

        # Load each utterance as a row in original CSV and remove empty rows
        dfs = [pd.read_csv(csv_path, index_col='id', usecols=col2dtype.keys(), dtype=col2dtype) for csv_path in sorted(transcripts.glob('*.csv'))]
        df = pd.concat(dfs)
        df.drop(df[df['num_tokens'] <= 0].index, inplace=True)
        self.logger.info(f'Loaded {len(df)} utterances from {len(dfs)} CSVs.')
        
        # Add a column to indicate whether the speaker is a child
        roles = df['speaker_role'].unique()
        child_roles = ['Target_Child', 'Child']
        self.logger.info(f'Found speaker roles: {roles}')
        df['is_child'] = df['speaker_role'].isin(child_roles)

        # Sort df by target_child_age and transcript_id
        df.sort_values(by=['target_child_age', 'transcript_id'], inplace=True)

        # Remove rows with ignore_regex in gloss
        ignore_regex = re.compile(r'(�|www|xxx|yyy)')
        df.drop(df[df['gloss'].apply(lambda x: ignore_regex.findall(str(x)) != [])].index, inplace=True)
        
        # Drop null gloss
        df.dropna(subset=['gloss'], inplace=True)

        # Clean each sentence, special cleaning for English
        if df['language'].iloc[0] == 'eng':
            df['processed_gloss'] = df.apply(lambda x: _clean_english(x['gloss'], x['type']), axis=1)
        else:
            df['processed_gloss'] = df.apply(lambda x: _clean(x['gloss'], x['type']), axis=1)

        # Fix some data types
        df['part_of_speech'] = df['part_of_speech'].astype(str)
        df['part_of_speech'] = df['part_of_speech'].apply(lambda x: ' ' if x == 'nan' else x)
        df['stem'] = df['stem'].astype(str)
        df['stem'] = df['stem'].apply(lambda x: ' ' if x == 'nan' else x)
        df['target_child_sex'] = df['target_child_sex'].astype(str)
        df['target_child_sex'] = df['target_child_sex'].apply(lambda x: 'unknown' if x == 'nan' else x)

        # Fix transcription errors in Serbian
        if df['language'].iloc[0] == 'srp':
            df.drop(df[df['processed_gloss'].str.contains('q')].index, inplace=True)

        return df
    
    def phonemize_utterances(self, language: str, keep_word_boundaries: bool = True, verbose: bool = False):
        """ Phonemize utterances. """

        with open(PHONEMIZER_CONFIG_PATH, 'r') as f:
            phonemizer_config = json.load(f)
        language = language.lower()
        if language not in phonemizer_config:
            raise ValueError(f'Language "{language}" not found in phonemizer config. Choices: {list(phonemizer_config.keys())}')
        config = phonemizer_config[language]
        self.logger.info(f'Using phonemizer config: {config}')

        backend = config['backend']
        lang = config['language']
        lines = self.df['stem'] if lang in ['mandarin', 'cantonese', 'yue-Latn', 'cmn-Latn'] else self.df['processed_gloss']
        if 'wrapper_kwargs' in config:
            self.df['phonemized_utterance'] = phonemize_utterances(lines, backend, lang, keep_word_boundaries=keep_word_boundaries, verbose=verbose, **config['wrapper_kwargs'])
        else:
            self.df['phonemized_utterance'] = phonemize_utterances(lines, backend, lang, keep_word_boundaries=keep_word_boundaries, verbose=verbose)

        num_empty = len(self.df[self.df['phonemized_utterance'] == ''])
        num_empty += len(self.df[self.df['phonemized_utterance'] == 'WORD_BOUNDARY '])
        if num_empty > 0:
            self.logger.warning(f'{num_empty} lines were not phonemized successfully. Dropping these.')
            self.df = self.df[self.df['phonemized_utterance'] != '']
            self.df = self.df[self.df['phonemized_utterance'] != 'WORD_BOUNDARY ']
        self.df['language_code'] = config['language']

    def character_split_utterances(self):
        """ Character split utterances. """

        self.df['character_split_utterance'] = character_split_utterances(self.df['processed_gloss'])

    def split_df(self, dev_size: int = 10_000, sequential: bool = False):
        """ Split the DataFrame into a training set and a validation set.
        
        Note that the DataFrame is likely to be sorted by age, so the split will be age-ordered
        and if the split is sequential, the validation set will consist of utterances
        targetted at older children.
        """

        if sequential:
            train = self.df[:-dev_size]
            valid = self.df[-dev_size:]
        else:
            interval = len(self.df) // dev_size
            self.logger.info("Taking every {}th line to get 10,000 lines for validation...".format(interval))
            valid = self.df.iloc[::interval]
            valid = valid[:dev_size]
            train = self.df.drop(valid.index)
        return train, valid

    def print_statistics(self):
        """ Print statistics about the DataFrame. """

        total_corpora = len(self.df['corpus_id'].unique())
        total_speakers = len(self.df['speaker_id'].unique())
        total_target_children = len(self.df['target_child_id'].unique())
        total_lines = len(self.df)
        num_words = sum([line.count('WORD_BOUNDARY') for line in self.df['phonemized_utterance']])
        num_phonemes = sum([len(line.split()) for line in self.df['phonemized_utterance']]) - num_words

        self.logger.info(f'Total corpora: {total_corpora}')
        self.logger.info(f'Total speakers: {total_speakers}')
        self.logger.info(f'Total target children: {total_target_children}')
        self.logger.info(f'Total lines: {total_lines}')
        self.logger.info(f'Total words: {num_words}')
        self.logger.info(f'Total phonemes: {num_phonemes}')

    def save_df(self, out_path: Path):
        """ Save the DataFrame to a CSV file. """

        out_path.mkdir(exist_ok=True, parents=True)
        self.df.to_csv(out_path / 'processed.csv')
        self.logger.info(f'Saved processed dataset to {out_path / "processed.csv"} with a total of {len(self.df)} utterances.')

    def save_splits(self, out_path: Path):
        """ Save the training and validation DataFrames to CSV files. """

        out_path.mkdir(exist_ok=True, parents=True)
        train, valid = self.split_df()
        train.to_csv(out_path / 'train.csv')
        valid.to_csv(out_path / 'valid.csv')
        self.logger.info(f'Saved train and valid sets to {out_path}')