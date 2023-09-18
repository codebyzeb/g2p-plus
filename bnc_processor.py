"""
Script that downloads and processes the Audio BNC corpus (http://www.phon.ox.ac.uk/AudioBNC).

Uses the words from the phonemic transcriptions to group the phonemes into words, and uses alignment with the orthographic transcriptions to group the words into utterances.

A conversion table is used to convert from the BNC phonemes to IPA, according to this table: http://www.phon.ox.ac.uk/files/docs/BNC_transcription_alphabet.html

"""

import os
import re
import requests

from tqdm import tqdm

CONVERSION_TABLE = {
    'P' : 'p',
    'B' : 'b',
    'T' : 't',
    'D' : 'd',
    'CH' : 't̠ʃ',
    'JH' : 'd̠ʒ',
    'K' : 'k',
    'G' : 'g',
    'M' : 'm',
    'N' : 'n',
    'NG' : 'ŋ',
    'F' : 'f',
    'V' : 'v',
    'TH' : 'θ',
    'DH' : 'ð',
    'S' : 's',
    'SH' : 'ʃ',
    'ZH' : 'ʒ',
    'HH' : 'h',
    'R' : 'r',
    'L' : 'l',
    'W' : 'w',
    'Y' : 'j',
    'Z' : 'z',
    'IH' : 'ɪ',
    'EH' : 'ɛ',
    'AE' : 'a',
    'AH0' : 'ə',
    'AH1' : 'ʌ',
    'AH2' : 'ʌ',
    'UH1' : 'ʊ',
    'UH2' : 'ʊ',
    'OH': 'ɒ',
    'UH' : 'ʊ',
    'IY' : 'i:',
    'EY' : 'eɪ',
    'AY' : 'aɪ',
    'OY' : 'oɪ',
    'AW' : 'aʊ',
    'OW' : 'əʊ',
    'UW' : 'u:',
    'ER0': 'ɚ',
    'ER1': 'ə:',
    'ER2': 'ə',
    'AA' : 'ɑ:',
    'AO' : 'ɔ:'
}

def convert_to_ipa(phones):
    """Converts a list of phones to IPA."""
    ipa = []
    i = 0
    while i < len(phones):
        # Deal with dipthongs
        phone = phones[i].upper()
        if i != len(phones) - 1 and (phone == 'IH1' or phone == 'IH2') and phones[i+1] == 'AH0':
            ipa.append('ɪə')
            i += 1
        elif phone in CONVERSION_TABLE:
            ipa.append(CONVERSION_TABLE[phone])
        elif phone[-1] in ['0','1','2'] and phone[:-1] in CONVERSION_TABLE: # Stressed vowel
            ipa.append(CONVERSION_TABLE[phone[:-1]])
        else:
            raise ValueError('Unknown phone: {}'.format(phone))
        i += 1
    return ipa

def edit_distance(line1, line2):
    # Initialize the matrix
    matrix = [[0 for _ in range(len(line2) + 1)] for _ in range(len(line1) + 1)]
    for i in range(len(line1) + 1):
        matrix[i][0] = i
    for j in range(len(line2) + 1):
        matrix[0][j] = j
    # Compute the matrix
    for i in range(1, len(line1) + 1):
        for j in range(1, len(line2) + 1):
            if line1[i-1] == line2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + 1)
    # Return the edit distance
    return matrix[-1][-1]

# Works through all HTML transcripts from AudioBNC and extracts the orthographic words
def get_orthographic_utterances(transcript_paths):
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

# Tries to match the TextGrid words to the orthographic words
def clean_words(words):
    word_line = ' '.join([word for word in words if not word in ['sp', '{OOV}', '{LG}', '{GAP_ANONYMIZATION}', '{CG}', '{XX}']])
    word_line = (
        word_line.replace(" 'S", "'S")
        .replace(" 'VE", "'VE")
        .replace("GON NA", "GONNA")
        .replace("DUN N","DUN XXXXN")
        .replace("DUN N NO","DUNNO")
        .replace(" N IT","NIT")
        .replace("GOT TA","GOTTA")
        .replace("WAN NA","WANNA").strip()
    )
    return word_line

# Works through all TextGrid files of AudioBNC, extracting the phones and words,
# aligning them according to the linebreaks in the orthographic transcripts
# and converting phonemes to IPA
def get_utterance_from_paths(grid_paths, orthographic_utterances):

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
                    phone_line = phone_line + ' '.join(convert_to_ipa(phones_in_word)) + ' WORD_BOUNDARY '
                    phones_in_word = []
                # Check if start of new utterances
                word_line = clean_words([word[0] for word in words[start_word_index : current_word_index]])
                orthographic_word_line = orthographic_words[orthographic_words_index]
                if word_line.strip() != '' and word_line.strip() != ' ' and orthographic_words_index < len(orthographic_words) and abs(len(orthographic_word_line) - len(word_line)) < 3 and (orthographic_word_line[0] == word_line[0] and orthographic_word_line[-2:] == word_line[-2:]): # Allow for a bit of leeway
                    phone_lines.append(phone_line)
                    word_lines.append(word_line)
                    orthographic_word_lines.append(orthographic_word_line)
                    phone_line = ''
                    orthographic_words_index += 1
                    start_word_index = current_word_index
                    if word_line != orthographic_word_line:
                        not_quite_equal += 1
                    if orthographic_words_index >= len(orthographic_words):
                        remaining_words = clean_words([word[0] for word in words[current_word_index:]])
                        if remaining_words != '':
                            print('Error: Stopping alignment but words remaining: {} in sentence {}, {}'.format(remaining_words, clean_words([word[0] for word in words[-20:]]), orthographic_word_lines[-2:]))
                        break
                current_word_index += 1
            # Ignore pause markers and other non-phones
            if phone in ['sil', 'ns', 'sp', 'lg', 'cg', 'ls', 'br', 'ns1q']:
                continue
            phones_in_word.append(phone)

        # Add the last utterance
        if phones_in_word != []:
            phone_line = phone_line + ' '.join(convert_to_ipa(phones_in_word)) + ' WORD_BOUNDARY '
            phone_lines.append(phone_line)
            word_lines.append(word_line)
            orthographic_word_lines.append(orthographic_word_line)
        
    return phone_lines, word_lines, orthographic_word_lines

if __name__ == '__main__':

    transcripts_repo = "http://bnc.phon.ox.ac.uk/filelist-html.txt"
    transcript_paths = requests.get(transcripts_repo).text.split('\n')

    #transcript_paths = ['http://bnc.phon.ox.ac.uk/transcripts-html/KDP.html']
        
    # Get orthographic words from each path and show progress bar
    orthographic_utterances = get_orthographic_utterances(transcript_paths)
    # Show first 10 utterances

    grid_repo = "http://bnc.phon.ox.ac.uk/filelist-textgrid.txt"
    grid_paths = requests.get(grid_repo).text.split('\n')

    # Get utterances from each path
    phone_lines, word_lines, orthographic_word_lines = get_utterance_from_paths(grid_paths, orthographic_utterances)


    # Split into train, dev and test
    train_size = int(len(phone_lines) * 0.8)
    dev_size = int(len(phone_lines) * 0.1)
    test_size = len(phone_lines) - train_size - dev_size

    # Write train, dev and test to dataset
    with open('BNC/train.txt', 'w') as f:
        for line in phone_lines[:train_size]:
            f.write(line + '\n')
    with open('BNC/valid.txt', 'w') as f:
        for line in phone_lines[train_size:train_size+dev_size]:
            f.write(line + '\n')
    with open('BNC/test.txt', 'w') as f:
        for line in phone_lines[train_size+dev_size:]:
            f.write(line + '\n')

    # # Write full phonemic dataset
    # with open('bnc_full.txt', 'w') as f:
    #     for line in phone_lines:
    #         f.write(line + '\n')

    # # Write words
    # with open('bnc_word.txt', 'w') as f:
    #     for line in word_lines:
    #         f.write(line + '\n')

    # # Write orthographic words
    # out_path = 'bnc_orthographic_word.txt'
    # with open(out_path, 'w') as f:
    #     for line in orthographic_word_lines:
    #         f.write(line + '\n')
            


