""" Utility functions for the project. """

import pandas as pd

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

def split_df(df, sequential=False):
    """ Splits a DataFrame into a training set and a 10,000-line validation set.
    
    Note that the DataFrame is likely to be sorted by age, so the split will be age-ordered
    and if the split is sequential, the validation set will consist of utterances
    targetted at older children.
    """

    dev_size = 10_000
    if sequential:
        train = df[:-dev_size]
        valid = df[-dev_size:]
    else:
        interval = len(df) // dev_size
        print("Taking every {}th line to get 10,000 lines for validation...".format(interval))
        valid = df.iloc[::interval]
        valid = valid[:dev_size]
        train = df.drop(valid.index)
    return train, valid
