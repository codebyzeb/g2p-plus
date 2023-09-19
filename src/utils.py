""" Utility functions for the project """

from phonemizer import phonemize
from phonemizer.separator import Separator

# Espeak has some issues with joining IPA symbols together, so we need to add spaces between them
REPLACE_DICT = {'ɛɹ': 'ɛ ɹ', 
                'ʊɹ' : 'ʊ ɹ',
                'əl' : 'ə l',
                'oːɹ' : 'oː ɹ',
                'ɪɹ' : 'ɪ ɹ',
                'ɑːɹ' : 'ɑː ɹ',
                'ɔːɹ' : 'ɔː ɹ',
                'aɪɚ' : 'aɪ ɚ',
                'iə' : 'i ə',
                'aɪə' : 'aɪ ə',
                'aɪʊɹ' : 'aɪ ʊ ɹ',
                'aɪʊ' : 'aɪ ʊ',
                'dʒ' : 'd̠ʒ',
                'tʃ' : 't̠ʃ'}

# Conversion table from BNC ASCII phonemes to IPA symbols
CONVERSION_TABLE = {'P' : 'p',
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
                'AO' : 'ɔ:',}

def phonemize_utterances(lines, language='en', words_mismatch='remove', language_switch='remove-utterance'):
    """ Uses phonemizer to phonemize text. Returns a list of phonemized lines. """

    print(f'Phonemizing using language "{language}"...')
    phn = phonemize(
        lines,
        language=language,
        backend='espeak',
        separator=Separator(phone='PHONE_BOUNDARY', word=' ', syllable=''),
        strip=True,
        preserve_punctuation=False,
        language_switch=language_switch,
        words_mismatch=words_mismatch,
        njobs=4)
    
    mismatched = len([line for line in phn if line == ''])
    phn = [line.replace(' ', ' WORD_BOUNDARY ').replace('PHONE_BOUNDARY', ' ') for line in phn if line != ''] # Set the word boundary
    # Use replace map to fix some issues with espeak
    for key, value in REPLACE_DICT.items():
        phn = [line.replace(key, value) for line in phn]
    phn = [line + ' WORD_BOUNDARY \n' for line in phn] # Add newline

    print(f'Removed {mismatched} mismatched or language switched lines')

    return phn

def convert_bnc_to_ipa(phones):
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

# Tries to match the formatting of TextGrid words in BNC to the orthographic words in BNC
def clean_textgrid_words(words):
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

def split_and_save(lines, out_path, sequential):
    """ Splits 95-5-5 and saves to out_path. Either sequential or interleaved. """
    lines = [line.strip() + '\n' for line in lines if line.strip() != '']
    train_lines = []
    valid_lines = []
    test_lines = []
    # Split the lines 90-5-5 while preserving age-ordering
    if sequential:
        train_size = int(len(lines) * 0.9)
        dev_size = int(len(lines) * 0.05)
        train_lines = lines[:train_size]
        valid_lines = lines[train_size:train_size+dev_size]
        test_lines = lines[train_size+dev_size:]
    else:
        for i, line in enumerate(lines):
            if i % 20 == 18:
                valid_lines.append(line)
            elif i % 20 == 19:
                test_lines.append(line)
            else:
                train_lines.append(line)

    print(f'Total lines: {len(lines)}')
    open(out_path / 'train.txt', 'w').writelines(train_lines)
    print(f'Wrote {len(train_lines)} ({round(len(train_lines)/len(lines), 3)*100}%) lines to {out_path / "train.txt"}')
    open(out_path / 'valid.txt', 'w').writelines(valid_lines)
    print(f'Wrote {len(valid_lines)} ({round(len(valid_lines)/len(lines), 3)*100}%) lines to {out_path / "valid.txt"}')
    open(out_path / 'test.txt', 'w').writelines(test_lines)
    print(f'Wrote {len(test_lines)} ({round(len(test_lines)/len(lines), 3)*100}%) lines to {out_path / "test.txt"}')