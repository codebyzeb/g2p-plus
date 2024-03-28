""" Phonemize text using the phonemizer library."""

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

langcodes = { 'basque':'eu', 'cantonese':'yue', 'croatian':'hr', 'danish':'da', 'dutch':'nl',
              'englishna':'en-us', 'englishuk':'en-gb', 'estonian':'et', 'farsi':'fa-latn', 'french':'fr-fr', 'german':'de', 'greek':'el',
              'hungarian':'hu', 'icelandic':'is', 'indonesian':'id', 'irish':'ga', 'Italian':'it', 'japanese':'ja', 'korean':'ko',
              'mandarin':'cmn', 'norwegian':'nb', 'polish':'pl', 'portuguesebr':'pt-br', 'portuguesept':'pt',
              'romanian':'ro', 'serbian':'sv', 'spanish':'es', 'swedish':'sv', 'turkish':'tr', 'welsh':'cy', 'hebrew' : 'he' }

def phonemize_utterances(lines, language='EnglishNA', words_mismatch='remove', language_switch='remove-utterance'):
    """ Uses phonemizer to phonemize text. Returns a list of phonemized lines. Lines that could not be phonemized are returned as empty strings."""

    print(f'Phonemizing using language "{language}"...')
    language = language.lower()
    if language not in langcodes:
        raise ValueError(f'Language "{language}" not supported. Supported languages: {list(langcodes.keys())}')
    if language == 'japanese':
        print('INFO: Japanese phonemization is not supported by espeak. Using the segments backend instead.')
        phn = []
        missed_lines = 0
        for line in lines:
            try:
                phn.append(phonemize(
                    line,
                    language=language.lower(),
                    backend='segments',
                    separator=Separator(phone='PHONE_BOUNDARY', word=' ', syllable=''),
                    strip=True,
                    preserve_punctuation=False)) 
            except ValueError:
                missed_lines += 1
                phn.append('')
        print(f'WARNING: {missed_lines} lines were not phonemized due to errors with the segments file.')
    else:
        language = langcodes[language]
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
        
    for i in range(len(phn)):
        if phn[i] == '':
            continue
        phn[i] = phn[i].replace(' ', ' WORD_BOUNDARY ').replace('PHONE_BOUNDARY', ' ')
        for key, value in REPLACE_DICT.items():
            phn[i] = phn[i].replace(key, value)
        phn[i] = phn[i] + ' WORD_BOUNDARY'

    return phn

def character_split_utterance(lines):
    """ Splits the lines into characters, in a similar format to the phonemizer. 
    Intended for comparison between phonemization and written text.
    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip()[:-2])]) + ' WORD_BOUNDARY' for line in lines]
