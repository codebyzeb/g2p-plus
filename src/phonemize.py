""" Phonemize text using the phonemizer library."""

import re
import subprocess
import pandas as pd
from phonemizer import phonemize
from phonemizer.separator import Separator
from pinyin_to_ipa import pinyin_to_ipa

from src.dicts import folding, folding_espeak, langcodes

def phonemize_utterances(lines, language='EnglishNA'):
    """ Phonemizes lines using a technique depending on the language. Returning a list of lines with space-separated IPA phonemes.
    Lines that could not be phonemized are returned as empty strings."""


    print(f'Phonemizing using language "{language}"...')
    language = language.lower()
    if language not in langcodes:
        raise ValueError(f'Language "{language}" not supported. Supported languages: {list(langcodes.keys())}')
    langcode = langcodes[language]

    if language == 'mandarin':
        utterances = phonemize_mandarin(lines)
    elif language == 'cantonese':
        utterances = phonemize_cantonese(lines)
    elif language == 'japanese':
        utterances = phonemize_japanese(lines)
    else:
        utterances = phonemize_utterances_espeak(lines, langcode)

    utterances = correct_errors(utterances, langcode)
    return utterances

def correct_errors(lines, langcode):
    """ Uses folding dictionaries to correct output produced by the backend phonemizers. """

    if langcode not in folding:
        print(f'WARNING: No folding dictionary found for language code "{langcode}".')
        return lines

    for i in range(len(lines)):
        if lines[i] == '':
            continue
        for key, value in folding[langcode].items():
            lines[i] = lines[i].replace(key, value)
    return lines
    
def phonemize_japanese(lines):
    """ Uses phonemizer with segments backend to phonemize Japanese text."""

    print('INFO: Japanese phonemization is not supported by espeak. Using the segments backend instead.')
    phn = []
    missed_lines = 0
    for line in lines:
        try:
            phn.append(phonemize(
                line,
                language='japanese',
                backend='segments',
                separator=Separator(phone=' ', word=' WORD_BOUNDARY ', syllable=''),
                strip=True,
                preserve_punctuation=False)) 
        except ValueError:
            missed_lines += 1
            phn.append('')
    if missed_lines > 0:
        print(f'WARNING: {missed_lines} lines were not phonemized due to errors with the segments file.')
        
    for i in range(len(phn)):
        if phn[i] == '':
            continue
        phn[i] = phn[i].replace(' ', ' WORD_BOUNDARY ').replace('PHONE_BOUNDARY', ' ')
        for key, value in folding_espeak.items():
            phn[i] = phn[i].replace(key, value)
        phn[i] = phn[i] + ' WORD_BOUNDARY'

    return phn
    
def phonemize_utterances_espeak(lines, langcode='en-us'):
    """ Uses phonemizer to phonemize text. Returns a list of phonemized lines. Lines that could not be phonemized are returned as empty strings."""
    
    print(f'Using espeak backend with language code "{langcode}"...')
    phn = phonemize(
        lines,
        language=langcode,
        backend='espeak',
        separator=Separator(phone='PHONE_BOUNDARY', word=' ', syllable=''),
        strip=True,
        preserve_punctuation=False,
        language_switch='remove-utterance',
        words_mismatch='remove',
        njobs=4)
        
    for i in range(len(phn)):
        if phn[i] == '':
            continue
        phn[i] = phn[i].replace(' ', ' WORD_BOUNDARY ').replace('PHONE_BOUNDARY', ' ')
        for key, value in folding_espeak.items():
            phn[i] = phn[i].replace(key, value)
        phn[i] = phn[i] + ' WORD_BOUNDARY'

    return phn

# TODO: Compare output phonemes to phoible and make sure they match
def phonemize_mandarin(lines):
    """ Uses pinyin to IPA converter to produce phonemic transcripts for pinyin input. """

    phn = []
    broken = 0
    for line in lines:
        if line.strip() == '':
            phn.append('')
            continue
        phonemized = ""
        words = line.split(' ')
        try:
            for word in words:
                # Split word into syllables and get the pinyin for each syllable
                syllables = re.findall(r'[a-zA-Z]+[0-9]*', word)
                syllables = [re.sub(r'[0]', '', syllable) for syllable in syllables]
                for syllable in syllables:
                    set = pinyin_to_ipa(syllable)
                    # Convert ordered set into string
                    syll = ' '.join(set[0])
                    # Add space before tone markers ˥˩, ˧˥, ˥ and ˧˩˧ but only if not preceded by a space
                    syll = re.sub(r'(?<!\s)(˥˩|˧˥|˥|˧˩˧)', r' \1', syll)
                    # Replace ˧˩˧ with	˧˨˧ to match phoible
                    syll = syll.replace('˧˩˧', '˧˨˧')
                    phonemized += syll + ' '
                phonemized += 'WORD_BOUNDARY '
        except Exception as e:
            phonemized = ""
            broken += 1
        phn.append(phonemized)

    if broken > 0:
        print(f'WARNING: {broken} lines were not phonemized successfully by pinyin to ipa conversion.')

    return phn

def phonemize_cantonese(lines):
    """ Use pingyam database to convert Cantonese from jyutping to IPA. """

    broken = []
    broken = 0
    phn = []

    # Load pingyam database
    cantonese_dict = pd.read_csv('data/pingyam/pingyambiu', sep='\t', header=None)[[5, 6]]
    cantonese_dict.columns = ['ipa', 'jyutping']
    cantonese_dict = cantonese_dict.set_index('jyutping').to_dict()['ipa']

    # Convert jyutping to IPA
    for line in lines:
        if line.strip() == '':
            phn.append('')
            continue
        phonemized = ''
        words = line.split(' ')
        line_broken = False
        for word in words:
            syllables = re.findall(r'[a-zA-Z]+[0-9]*', word)
            for syllable in syllables:
                if syllable not in cantonese_dict:
                    if not line_broken:
                        broken += 1
                        line_broken = True
                else:
                    ipa = cantonese_dict[syllable]
                    phonemized += ipa + ''
            phonemized += '_'
        if line_broken:
            phonemized = ''
        phn.append(phonemized)

    if broken > 0:
        print(f'WARNING: {broken} lines were not phonemized successfully by jyutping to ipa conversion.')

    # Separate phonemes with spaces and add word boundaries
    for i in range(len(phn)):
        phn[i] = ' '.join(list(phn[i]))
        phn[i] = phn[i].replace('_', 'WORD_BOUNDARY')

    return phn

def character_split_utterance(lines):
    """ Splits the lines into characters, in a similar format to the phonemizer. 
    Intended for comparison between phonemization and written text.
    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip()[:-2])]) + ' WORD_BOUNDARY' for line in lines]
