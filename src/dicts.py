# Dictionaries used in the project


language_to_code = { 'basque':'eu', 'catalan':'ca', 'croatian':'hr', 'danish':'da', 'dutch':'nl',
			'englishna':'en-us', 'englishuk':'en-gb', 'estonian':'et', 'farsi':'fa-latn', 'french':'fr-fr', 'german':'de', 'greek':'el',
			'hungarian':'hu', 'icelandic':'is', 'indonesian':'id', 'irish':'ga', 'italian':'it', 'japanese':'ja', 'korean':'ko',
			'norwegian':'nb', 'polish':'pl', 'portuguesebr':'pt-br', 'portuguesept':'pt', 'quechua':'qu',
			'romanian':'ro', 'serbian':'sv', 'spanish':'es', 'swedish':'sv', 'turkish':'tr', 'welsh':'cy', 'hebrew' : 'he'}

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

# Contains language-specific dictionaries to fix errors in the output of the phonemizer library.
FOLDING_PHONEMIZER = {

	# This dictionary splits phonemes produced by Espeak in order to match standard phoneme sets found in Phoible.
	'all' : {
        'ɛɹ': 'ɛ ɹ',
		'ʊɹ' : 'ʊ ɹ',
		'əl' : 'ə l',
		'oːɹ' : 'oː ɹ',
		'ɪɹ' : 'ɪ ɹ',
		'ɑːɹ' : 'ɑː ɹ',
		'ɔːɹ' : 'ɔː ɹ',
		'aɪɚ' : 'aɪ ɚ',
		'aɪə' : 'aɪ ə',
		'aɪʊɹ' : 'aɪ ʊ ɹ',
		'aɪʊ' : 'aɪ ʊ',
		'dʒ' : 'd̠ʒ',
		'tʃ' : 't̠ʃ',
		'iːː' : 'iː',
		'ɐɐ' : 'ɐ',
	},
	
	'en-us' : {
		# Fix strange espeak output
        'ææ' : 'æ',
        'ᵻ' : 'ɪ',

		# Changes to match BabySLM phoneme set
        'n̩' : 'ə n',
        'ɚ' : 'ə ɹ',
        'oː' : 'ɔ',
        'ɔː' : 'ɔ',
        'ɾ' : 't',
        'ɐ' : 'ʌ',
        'ɑː' : 'ɑ',
        'ʔ' : 't',
	},

	'de' : {
		# Fix strange espeak output
        'ɔø' : 'ɔ ʏ',
        '??' : 'ʊ r',
        ' 1 ' : ' ',

        # Analysed the output of espeak for German and found that the following replacements are necessary
        'ɑ' : 'a', # a vowels
        'ɜ' : 'ɐ', # er syllables
        'ɾ' : 'ɐ', # r endings
        'r' : 'ʀ', # r endings
	},

    'id' : {
        # Analysed the output of espeak for Indonesian and found that the following replacements are necessary
        'ç' : 'ʃ', # Replace voiceless palatal fricative with voiceless postalveolar fricative
        'aɪ' : 'ai̯', # Replace diphthong with more standard representation for indonesian
        'aʊ' : 'au̯', # Replace diphthong with more standard representation for indonesian
	},
    
}
    
FOLDING_PINYIN_TO_IPA = {
    # Fix tones to match "Standard Chinese; Mandarin" set
    '˥ ' : '˦ ',
	'˥˩ ' : '˦˨ ',
	'˧˥ ' : '˧˦ ',
	'˧˩˧ ' : '˧˨˧ ',
}


FOLDING_PINGYAM = {
	# Tones – note that we also remove the space before the tone marker, attaching it to the vowel
	' ˧ ˥' : '˧˥',
	' ˨ ˩' : '˧˩̰',
	' ˩ ˧' : '˩˧', 
	' ˨': '˨',
	' ˥' : '˥',
	' ˧' : '˧',
	'˧ ˥' : '˧˥',
	'˨ ˩' : '˧˩̰',
	'˩ ˧' : '˩˧', 

	# Long Diphthongs - we add extra-short vowel markers
	'a ː i' : 'aːĭ',
	'u ː i' : 'uːĭ',
	'ɔ ː i' : 'ɔːĭ',
	'a ː u' : 'aːŭ',
	'i ː u' : 'iːŭ',

	# Dipthongs
	'o u' : 'ou',
	'ɐ i'  : 'ɐi',
	'ɐ u' : 'ɐu',
	'ɵ y' : 'ɵy',
	'e i' : 'ei',

	# Long vowels
	'i ː' : 'iː',
	'a ː' : 'aː',
	'ɛ ː' : 'ɛː',
	'ɔ ː' : 'ɔː',
	'u ː' : 'uː',
	'y ː' : 'yː',
	'œ ː' : 'œː',

	# Aspirated consonants
	't s ʰ' : 'tsʰ',
	't s' : 'ts',
	't ʰ' : 'tʰ',
	'k ʰ' : 'kʰ',
	'p ʰ' : 'pʰ',
	'm ̩ ː' : 'm̩', # Doesn't actually appear in phoible, so we remove vowel length marker
}

FOLDING_EPITRAN = {
    # All Epitran output
	'all' : {
        # Attach ipa markers to their phonemes
        ' ̚' : '̚'
	},
    
	'yue-Latn' : {
        '˧ ˥' : '˧˥',
		'˨ ˩' : '˧˩̰',
		'˩ ˧' : '˩˧', 
		'˨': '˨',
		'˥' : '˥',
		'˧' : '˧',
	},
    
	'cmn-Latn' : {
        '1' : '˥',
        '2' : '˧˥',
        '3' : '˨˩',
        '4' : '˥˩',
        '5' : '˧',
	},
	
	'cmn-Hans' : {
        '˧ ˥' : '˧˥',
        '˨ ˩' : '˨˩',
        '˥ ˩' : '˥˩',
	}
    
}