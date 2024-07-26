""" Process CHILDES CSV files."""

from pathlib import Path
import pandas as pd
import re 
from src.dicts import w2string, string2w

col2dtype = {'id': int,
             'speaker_role': str,
             'gloss': str,
             'stem': str,
             'type': str,
             'num_tokens': int,
             'target_child_age': float,
             'target_child_sex': str,
             'transcript_id': int,
             'target_child_id': int,
             'speaker_id': int,
             'collection_id': int,
             'corpus_id': int,
             'part_of_speech': str,
             'num_morphemes': int,
             'num_tokens': int,
             'language': str,}

punctuation_dict = {'imperative': '! ',
                    'imperative_emphatic': '! ',
                    'question exclamation': '! ',
                    'declarative': '. ',
                    'interruption': '. ',
                    'self interruption': '. ',
                    'quotation next line': '. ',
                    'quotation precedes': '. ',
                    'broken for coding': '. ',
                    'question': '? ',
                    'self interruption question': '? ',
                    'interruption question': '? ',
                    'trail off question': '? ',
                    'trail off': '. '}

def clean_english(sentence, type):
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

def clean(sentence, type):
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

def process_childes(path: Path):
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
        print('Path is a directory, will extract utterances from all CSVs found in this directory.')
        transcripts = path
    else:
        print('Path is a file, will extract utterances from this CSV.')
        transcripts = [path]

    # Load each utterance as a row in original CSV and remove empty rows
    dfs = [pd.read_csv(csv_path, index_col='id', usecols=col2dtype.keys(), dtype=col2dtype) for csv_path in sorted(transcripts.glob('*.csv'))]
    df = pd.concat(dfs)
    df.drop(df[df['num_tokens'] <= 0].index, inplace=True)
    print(f'Loaded {len(df)} utterances from {len(dfs)} CSVs.')
    
    # Add a column to indicate whether the speaker is a child
    roles = df['speaker_role'].unique()
    child_roles = ['Target_Child', 'Child']
    print(f'Found speaker roles: {roles}')
    df['is_child'] = df['speaker_role'].isin(child_roles)

    # Sort df by target_child_age and transcript_id
    df.sort_values(by=['target_child_age', 'transcript_id'], inplace=True)

    # Remove rows with ignore_regex in gloss
    ignore_regex = re.compile(r'(�|www|xxx|yyy)')
    df.drop(df[df['gloss'].apply(lambda x: ignore_regex.findall(str(x)) != [])].index, inplace=True)
    
    # Drop null gloss
    df.dropna(subset=['gloss'], inplace=True)

    # Clean each sentence, special cleaning for English
    if 'eng' in df['language'].iloc[0]:
        df['processed_gloss'] = df.apply(lambda x: clean_english(x['gloss'], x['type']), axis=1)
    else:
        df['processed_gloss'] = df.apply(lambda x: clean(x['gloss'], x['type']), axis=1)

    # Fix some data types
    df['part_of_speech'] = df['part_of_speech'].astype(str)
    df['part_of_speech'] = df['part_of_speech'].apply(lambda x: ' ' if x == 'nan' else x)
    df['stem'] = df['stem'].astype(str)
    df['stem'] = df['stem'].apply(lambda x: ' ' if x == 'nan' else x)
    df['target_child_sex'] = df['target_child_sex'].astype(str)
    df['target_child_sex'] = df['target_child_sex'].apply(lambda x: 'unknown' if x == 'nan' else x)

    return df