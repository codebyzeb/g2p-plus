""" Phonemize text using the phonemizer library."""

import re
import subprocess
import pandas as pd
from phonemizer import phonemize
from phonemizer.separator import Separator
from pinyin_to_ipa import pinyin_to_ipa

from src.dicts import cantonese_phoneme_symbol_pairs_map

# Espeak has some issues with joining IPA symbols together, so we need to add spaces between them
# TODO: Make sure this is working per language
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

langcodes = { 'basque':'eu', 'cantonese':'yue', 'croatian':'hr', 'danish':'da', 'dutch':'nl',
              'englishna':'en-us', 'englishuk':'en-gb', 'estonian':'et', 'farsi':'fa-latn', 'french':'fr-fr', 'german':'de', 'greek':'el',
              'hungarian':'hu', 'icelandic':'is', 'indonesian':'id', 'irish':'ga', 'Italian':'it', 'japanese':'ja', 'korean':'ko',
              'mandarin':'cmn-latn-pinyin', 'norwegian':'nb', 'polish':'pl', 'portuguesebr':'pt-br', 'portuguesept':'pt',
              'romanian':'ro', 'serbian':'sv', 'spanish':'es', 'swedish':'sv', 'turkish':'tr', 'welsh':'cy', 'hebrew' : 'he' }

def phonemize_utterances(lines, language='EnglishNA'):
    """ Phonemizes lines using a technique depending on the language. Returning a list of lines with space-separated IPA phonemes.
    Lines that could not be phonemized are returned as empty strings."""


    print(f'Phonemizing using language "{language}"...')
    language = language.lower()
    if language not in langcodes:
        raise ValueError(f'Language "{language}" not supported. Supported languages: {list(langcodes.keys())}')

    if language == 'mandarin':
        return phonemize_mandarin(lines)
    elif language == 'cantonese':
        return phonemize_cantonese(lines)
    elif language == 'japanese':
        return phonemize_japanese(lines)
    else:
        return phonemize_utterances_espeak(lines, language)
    
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
        for key, value in REPLACE_DICT.items():
            phn[i] = phn[i].replace(key, value)
        phn[i] = phn[i] + ' WORD_BOUNDARY'

    return phn
    
def phonemize_utterances_espeak(lines, language='EnglishNA'):
    """ Uses phonemizer to phonemize text. Returns a list of phonemized lines. Lines that could not be phonemized are returned as empty strings."""
    
    language = langcodes[language]
    print(f'Using espeak backend with language code "{language}"...')
    phn = phonemize(
        lines,
        language=language,
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
        for key, value in REPLACE_DICT.items():
            phn[i] = phn[i].replace(key, value)
        phn[i] = phn[i] + ' WORD_BOUNDARY'

    # Language-specific fixes
    if language == 'en-us':
        phn[i] = phn[i].replace('ææ', 'æ')
        phn[i] = phn[i].replace('ᵻ', 'ɪ')
    if language == 'de':
        phn[i] = phn[i].replace('ɔø', 'ɔ ʏ')
        phn[i] = phn[i].replace('??', 'ʊr')
        phn[i] = phn[i].replace(' 1 ', ' ')

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

    # Separate phonemes with spaces
    for i in range(len(phn)):
        # Add a space between every character
        line = phn[i]
        line = ' '.join(list(line))
        line = line.replace('_', 'WORD_BOUNDARY')
        for pair in cantonese_phoneme_symbol_pairs_map:
            line = line.replace(pair, cantonese_phoneme_symbol_pairs_map[pair])
        phn[i] = line

    return phn

def character_split_utterance(lines):
    """ Splits the lines into characters, in a similar format to the phonemizer. 
    Intended for comparison between phonemization and written text.
    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip()[:-2])]) + ' WORD_BOUNDARY' for line in lines]
