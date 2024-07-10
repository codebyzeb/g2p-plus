"""
Script that downloads and processes the Audio BNC corpus (http://www.phon.ox.ac.uk/AudioBNC).

Uses the words from the phonemic transcriptions to group the phonemes into words, and uses alignment with the orthographic transcriptions to group the words into utterances.

A conversion table is used to convert from the BNC phonemes to IPA, according to this table: http://www.phon.ox.ac.uk/files/docs/BNC_transcription_alphabet.html

"""

import argparse
from pathlib import Path
import re
import requests
import sys

sys.path.append('../..')

from src.utils import phonemize_utterances, convert_bnc_to_ipa, clean_textgrid_words, split_and_save

from tqdm import tqdm

ORTHOGRAPHIC_TRANSCRIPTS_REPO = "http://bnc.phon.ox.ac.uk/filelist-html.txt"
PHONEMIC_TRANSCRIPTS_REPO = "http://bnc.phon.ox.ac.uk/filelist-textgrid.txt"

# Works through all HTML transcripts from AudioBNC and extracts the orthographic words
def download_bnc_orthographic_utterances(transcript_paths):
    orthographic_utterances = {}

    for path in tqdm(transcript_paths, 'Getting orthographic utterances'):
        if path == '':
            continue
        section = path.split('/')[-1].split('.')[0]
        lines = requests.get(path).text.split('\n')
        tape_ref = None

        for line in lines:

            # If the line is in the form "<h4>1 (Tape XXXXXX)</h4>", save the number XXXXXX
            if '(Tape' in line:
                recording_number = line.split('<h4>')[1].split(' ')[0].strip()
                tape_ref = section + '_' + recording_number
            elif 'Undivided text' in line:
                tape_ref = section + '_1'
            elif tape_ref is not None and line.strip().startswith('['):
                utterance = ']'.join(line.strip().split('<')[0].split(']')[1:]).strip()
                utterance = re.sub(r'\[.*?\]', '', utterance) # Remove annotations in square brackets
                utterance = re.sub(r'[^\w\s\']', '', utterance) # Remove punctuation
                utterance = re.sub(r'\s{2,}', ' ', utterance) # Remove extra spaces
                utterance = utterance.strip().upper() # Remove leading and trailing spaces and make uppercase
                if utterance != '':
                    if tape_ref not in orthographic_utterances:
                        orthographic_utterances[tape_ref] = []
                    orthographic_utterances[tape_ref].append(utterance)

    return orthographic_utterances

# Works through all TextGrid files of AudioBNC, extracting the phones and words,
# aligning them according to the linebreaks in the orthographic transcripts
# and converting phonemes to IPA
def download_bnc_phonemic_transcriptions(grid_paths, orthographic_utterances):

    phone_lines = []
    word_lines = []
    orthographic_word_lines = []

    for path in tqdm(grid_paths, 'Getting utterances'):
        if path == '':
            continue
        tape_ref = '_'.join(path.split('.')[-2].split('_')[-2:]) # Extracts e.g. 'KDP_1' from 'http://bnc.phon.ox.ac.uk/data/021A-C0897X0004XX-AAZZP0_000406_KDP_1.TextGrid'
        if not tape_ref in orthographic_utterances:
            raise ValueError('No orthographic words for tape {}'.format(tape_ref))
        orthographic_words = orthographic_utterances[tape_ref]

        # Download and read file
        text = requests.get(path).text.split('\n')

        # Get the phones and words
        phones = []
        words = []
        i = 0

        # Get to the phones
        while not text[i].startswith('"phone"'):
            i += 1
        i += 1

        # Get all phones
        while i < len(text):
            while not text[i].startswith('"'):
                i += 1
            if text[i].startswith('"IntervalTier"'):
                break
            phone = text[i].strip()[1:-1]
            start_time = float(text[i-2].strip())
            phones.append((phone, start_time))
            i += 1

        # Get to the words
        while not text[i].startswith('"word"'):
            i += 1
        i += 1

        # Get all words
        while i < len(text):
            while not text[i].startswith('"'):
                i += 1
            if text[i].startswith('"IntervalTier"'):
                break
            word = text[i].strip()[1:-1]
            start_time = float(text[i-2].strip())
            words.append((word, start_time))
            i += 1
                
        # Get the phones for each word, and add an utterance boundary if the word aligns with a whole line of orthographic words
        phones_in_word = []
        phone_line = ''

        current_word_index = 1
        start_word_index = 0
        orthographic_words_index = 0

        # Iterate through phones, using words to determine word boundaries and aligning with orthographic words to determine utterance boundaries
        for phone, start_time in phones:
            if current_word_index >= len(words):
                break
            # Check for start of new word
            if start_time >= words[current_word_index][1]:
                if phones_in_word != []:
                    phone_line = phone_line + ' '.join(convert_bnc_to_ipa(phones_in_word)) + ' WORD_BOUNDARY '
                    phones_in_word = []
                # Check if start of new utterances
                word_line = clean_textgrid_words([word[0] for word in words[start_word_index : current_word_index]])
                orthographic_word_line = orthographic_words[orthographic_words_index]
                if word_line.strip() != '' and word_line.strip() != ' ' and orthographic_words_index < len(orthographic_words) and abs(len(orthographic_word_line) - len(word_line)) < 3 and (orthographic_word_line[0] == word_line[0] and orthographic_word_line[-2:] == word_line[-2:]): # Allow for a bit of leeway
                    phone_lines.append(phone_line)
                    word_lines.append(word_line)
                    orthographic_word_lines.append(orthographic_word_line)
                    phone_line = ''
                    orthographic_words_index += 1
                    start_word_index = current_word_index
                    if orthographic_words_index >= len(orthographic_words):
                        remaining_words = clean_textgrid_words([word[0] for word in words[current_word_index:]])
                        if remaining_words != '':
                            print('Error: Stopping alignment but words remaining: {} in sentence {}, {}'.format(remaining_words, clean_textgrid_words([word[0] for word in words[-20:]]), orthographic_word_lines[-2:]))
                        break
                current_word_index += 1
            # Ignore pause markers and other non-phones
            if phone in ['sil', 'ns', 'sp', 'lg', 'cg', 'ls', 'br', 'ns1q']:
                continue
            phones_in_word.append(phone)

        # Add the last utterance
        if phones_in_word != []:
            phone_line = phone_line + ' '.join(convert_bnc_to_ipa(phones_in_word)) + ' WORD_BOUNDARY '
            phone_lines.append(phone_line)
            word_lines.append(word_line)
            orthographic_word_lines.append(orthographic_word_line)
        
    return phone_lines, word_lines, orthographic_word_lines


def download(args):

    # Get orthographic transcripts to align with phonemic transcripts for finding utterance boundaries,
    # since the phonemic transcripts don't mark them
    transcript_paths = requests.get(ORTHOGRAPHIC_TRANSCRIPTS_REPO).text.split('\n')        
    orthographic_utterances = download_bnc_orthographic_utterances(transcript_paths)

    # Get phonemic transcripts and extract utterances in IPA
    grid_paths = requests.get(PHONEMIC_TRANSCRIPTS_REPO).text.split('\n')
    phone_lines, word_lines, _ = download_bnc_phonemic_transcriptions(grid_paths, orthographic_utterances)

    if not args.out_dir.is_dir():
        print('WARNING: A directory must be provided. Using file name as directory name')
        args.out_dir = args.out_dir.parent / args.out_dir.stem
    args.out_dir.mkdir(exist_ok=True)

    if args.split:
        split_and_save(phone_lines, out_path=args.out_dir, sequential=True)

    # Write full phonemic dataset
    with open(args.out_dir / 'bnc_phonemes.txt', 'w') as f:
        for line in phone_lines:
            f.write(line + '\n')
    print(f'Wrote {len(phone_lines)} lines to {args.out_dir / "bnc.txt"}')

    # Write words
    with open(args.out_dir / 'bnc_words.txt', 'w') as f:
        for line in word_lines:
            f.write(line + '\n')
    print(f'Wrote {len(word_lines)} lines to bnc_words.txt')

def phonemize_bnc(args):
    """ Uses phonemizer to phonemize a text. Doesn't remove mistmatched words or language switches. """

    if not args.out_dir.is_dir():
        print('WARNING: When splitting, a directory must be provided. Using file name as directory name')
        args.out_dir = args.out_dir.parent / args.out_dir.stem
    args.out_dir.mkdir(exist_ok=True)

    lines = open(args.path, 'r').readlines()
    lines = phonemize_utterances(lines, words_mismatch='warn', language_switch='remove-flags')

    if args.split:
        split_and_save(lines, out_path=args.out_dir, sequential=True)
    out_path = args.out_dir / 'bnc_ortho_phonemes.txt'
    open(out_path, 'w').writelines(lines)
    print(f'Wrote {len(lines)} lines to {out_path}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="BNC Processor")
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_download = subparsers.add_parser('download', help='Download utterances from BNC, save phonemes as IPA in "bnc.txt" and saves the words from the phonetic transcriptions in "bnc_words.txt"')
    parser_download.add_argument('-s', '--split', action='store_true', help='Produce three files according to a train-valid-test split of 90-5-5. Splitting is sequential, not interleaved.')
    parser_download.add_argument('-o', '--out_dir', default='BNC', type=Path, help='Directory to save utterances to')
    parser_download.set_defaults(func=download)

    parser_phonemize = subparsers.add_parser('phonemize', help='Phonemizes an orthographic transcription, such as the one produced by the download command.')
    parser_phonemize.add_argument('path', type=Path, help='Text file of orthographic transcriptions, one per line – presumably the "bnc_words.txt" file produced by "download"')
    parser_phonemize.add_argument('-s', '--split', action='store_true', help='Produce three files according to a train-valid-test split of 90-5-5. Splitting is sequential, not interleaved.')
    parser_phonemize.add_argument('-o', '--out_dir', default='BNC', type=Path, help='Directory to save utterances to')
    parser_phonemize.set_defaults(func=phonemize_bnc)

    args = parser.parse_args()
    args.func(args)