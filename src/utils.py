""" Utility functions for the project. """

import pandas as pd
from .dicts import CONVERSION_TABLE

def move_tone_marker_to_after_vowel(syll):
    """ Move the tone marker from the end of a cantonese syllable to directly after the vowel """

    cantonese_vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    cantonese_tone_symbols = "˥˧˨˩"
    if not syll[-1] in cantonese_tone_symbols:
        print(syll, syll[-1])
        return syll
    tone_marker = len(syll) - 1
    # Iterate backwards
    for i in range(len(syll)-2, -1, -1):
        if syll[i] in cantonese_tone_symbols:
            tone_marker = i
            continue
        if syll[i] in cantonese_vowel_symbols:
            return syll[:i+1] + syll[tone_marker:] + syll[i+1:tone_marker]
    return syll

def move_tone_marker_to_after_vowel_line(line):
    """ Move the tone marker from the end of a mandarin or cantonese syllable to directly after the vowel """

    vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    tone_symbols = ['˥', '˧˥', '˨˩', '˥˩', '˧', '˧˩̰', '˩˧', '˨', '˧˩̰', '˩˧'] 
    last_marker = -1
    line = line.split(' ')
    for i in range(len(line)):
        if line[i] in tone_symbols:
            for j in range(i-1, last_marker, -1):
                if line[j] in vowel_symbols or line[j] in tone_symbols:
                    line[j+1], line[i] = line[i], line[j+1]
                    break
            last_marker = i
    line = ' '.join(line)
    # Combine tone markers with previous vowel
    for tone in tone_symbols:
        line = line.replace(' ' + tone, tone)
    return line

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
