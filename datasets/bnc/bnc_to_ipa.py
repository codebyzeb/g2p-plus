# Conversion table from BNC ASCII phonemes to IPA symbols
# Taken from http://www.phon.ox.ac.uk/files/docs/BNC_transcription_alphabet.html
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