# Dictionaries used in the project
# TODO: The folding dictionaries could be moved into individual files for better organization.

language_to_code = { 'basque':'eu', 'catalan':'ca', 'croatian':'hr', 'danish':'da', 'dutch':'nl',
			'englishna':'en-us', 'englishuk':'en-gb', 'estonian':'et', 'farsi':'fa-latn', 'french':'fr-fr', 'german':'de', 'greek':'el',
			'hungarian':'hu', 'icelandic':'is', 'indonesian':'id', 'irish':'ga', 'italian':'it', 'japanese':'ja', 'korean':'ko',
			'norwegian':'nb', 'polish':'pl', 'portuguesebr':'pt-br', 'portuguesept':'pt', 'quechua':'qu',
			'romanian':'ro', 'serbian':'sr', 'spanish':'es', 'swedish':'sv', 'turkish':'tr', 'welsh':'cy', 'hebrew' : 'he'}

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
        '  ' : ' ',
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

        # Additional fixes
        'ɬ' : 'l',
        'nʲ' : 'n',
        'ɑ̃' : 'ɑ',
        'r' : 'ɹ',
	},

	'en-gb' : {
		# Fix strange espeak output
        'ææ' : 'æ',

		# Changes to match Phoible inventory 2252
        't ' : 'tʰ ',
        'k' : 'kʰ',
        'p' : 'pʰ',
        'iə' : 'ɪə',
        'ɛ ' : 'e ',
        'a ' : 'æ ',
        'ɔ ' : 'ɔː',
        'ɑ̃' : 'ɑː',
        'r' : 'ɹ',
        'aː' : 'ɑː',
	},

	'de' : {
		# Fix strange espeak output
        'ɔø' : 'ɔ ʏ',
        '??' : 'ʊ ʀ',
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

    'fr-fr' : {
        # Fix strange espeak output
        'ɑː' : 'ɑ',

        # Changes to match Phoible inventory 2269
        'øː' : 'ø',
        'iː' : 'i',
        'yː' : 'y',
        'aː' : 'a',
        'oː' : 'o',
        'œ̃' : 'œ',
    },

    'ja' : {
        # Match Japanese Phoible inventory
        't͡s' : 'ts',
        'g' : 'ɡ',
        'r' : 'ɾ',
    },

    'nl' : {
        # Match Dutch Phoible inventory
        'ɾ r' : 'ɾ',
        'r' : 'ɾ',
        'h' : 'ɦ',
        'ɛɪ' : 'ɛi',
        'yʊ' : 'ʏ ʋ',
        'ʌʊ' : 'ʌu',
        'eʊ' : 'eː u',
        'ɵ' : 'ʏ',
        'ɪː' : 'eː',

        'e' : 'ɛ',
        'ð' : 'd',
        'a' : 'ã',
     },

     'et' : {
        # Fix output of palatalised consonants
        's^' : 'sʲ',
        't^' : 'tʲ',
        'd^' : 'dʲ',
        # Fix output of long consonants
        'sʲ sʲ' : 'sʲː',
        'tʲ tʲ' : 'tʲː',
        'dʲ dʲ' : 'dʲː',
        's s' : 'sː',
        't t' : 'tː',
        'd d' : 'dː',
        'l l' : 'lː',
        'm m' : 'mː',
        'h h' : 'h',
        'ʃ ʃ' : 'ʃː',
        'n n' : 'nː',
        'f f' : 'fː',
        'r r' : 'rː',
        'k k' : 'kː',
        # Fix output of long vowels
        'ɵ ɵː' : 'ɤː',
        'ɵ' : 'ɤ',
        'y yː' : 'yː',
        'i iː' : 'iː',
        'e eː' : 'eː',
        'u uː' : 'uː',
        'a aː' : 'aː',
        'ø øː' : 'øː',
        'o oː' : 'oː',
        # Fix output of diphthongs
        'øi j' : 'øɪ̯',
        'øi' : 'øɪ̯',
        'æiː' : 'æi',
        'æ i' : 'æi',
        'yi j' : 'yː',
        # Other fixes
        'ʎ ' : 'l ',
     },

     'pl' : {
        # Match Polish Phoible inventory
        'ɛ' : 'e',
        'ɔ' : 'o',
        't ' : 't̪ ',
        'n' : 'n̪',
        ' s' : ' s̪',
        ' z' : ' z̪',
        'l' : 'l̪',
        'd ' : 'd̪ ',
        'ts' : 't̪s̪',
        ' ʒ' : ' z̻',
        ' ʃ' : ' s̻',
        't̠ʃ' : 't̻s̻',
        'tʃ' : 't̻s̻',
        'd̠ʒ' : 'd̻z̻',
        # Consonants that shouldn't be palatalised
        'ɲʲ' : 'ɲ',
        'vʲ' : 'v',
        'bʲ' : 'b',
        'pʲ' : 'p',
        'mʲ' : 'm',
        'fʲ' : 'f',
        'tʲ' : 't',
        'dʲ' : 'd̪',
        'rʲ' : 'r',
        's̻ʲ' : 's̻',
        'xʲ' : 'x',
        'z̻ʲ' : 'z̻',
        'tɕʲ' : 'tɕ',
        # Other fixes
        'ç' : 'x',
        'õ' : 'o',
        'oː' : 'o',
        'ɹ' : 'r',
        't ' : 't̪ ',
     },

    'sv' : {
        # Match Swedish Phoible inventory
        'n sx' : 'n s k',
        'sx' : 'ɧ',
        'n' : 'n̪',
        'r' : 'ɹ',
        'd' : 'd̪',
        't' : 't̪',
        's' : 's̪',
        'ʉ' : 'ʉ̟',
        'j' : 'ʝ',
        'y ' : 'ʏ ',
        'kː' : 'k',
        't̪ː' : 't̪',
        'ə' : 'e',
        'ɵː' : 'uː',
    },

    'pt' : {
        # Match Portuguese Phoible inventory
        't̠ʃ' : 't̪',
        't ' : 't̪ ',
        'd' : 'd̪',
        'ɹ' : 'ʁ',
        'r' : 'ʁ',
        'l' : 'l̪ˠ',
        'n' : 'n̪',
        'ɐ̃ʊ̃' : 'ɐ̃u̜',
        'ʊ' : 'u',
        'ɪ' : 'i',
        'ɑ' : 'a',
        'ɨ' : 'ɯ',
        'aː' : 'a',
        'ɾ ə' : 'ɾ',

        # Fix palatalised consonants
        'mʲ' : 'm',
        'sʲ' : 's',
        'ʁʲ' : 'ʁ',
        # Correct nasals
        'o ŋ' : 'õ',
        'ei ŋ' : 'ẽ',
        'ei m' : 'ẽ',
        'i ŋ' : 'ĩ',
        'ɐ̃ ŋ' : 'ɐ̃',
        'u ŋ' : 'ũ',
        'ũ ŋ' : 'ũ',
        # Fix dipthongs
        'ɛĩ' : 'ɛi',
        'eu' : 'eu̜',
        'au' : 'au̜',
        'iu' : 'iu̜',
        'ɛu' : 'ɛu̜',
        'eĩ' : 'ẽ',
        'ei' : 'ɐi',
        # Fix 'j'
        'ɐ̃ j' : 'ɐ̃i',
        'õ j' : 'õi',
        'j' : 'i',
        # Fix 'w'
        'k u w p' : 'k u l̪ˠ p', # Fix 'culp' sounds
        'w ĩ' : 'ũi',
        'o w' : 'o',
        'u w' : 'u',
        'w' : 'o', # Not sure if this is correct, we lose 'kw' sounds but w was also being produced instead of 'o' in cases like "como" which is definitely incorrect
        
        'fʲ' : 'f',
    
    },

    'ko' : {
        # Match Korean Phoible inventory
        'ɐ' : 'a',
        'q' : 'ɡ',
        'n' : 'n̪',
        's' : 's̪',
        'tɕ' : 't̠ʃ',
        't ' : 't̪ ',
        'ɫ' : 'l',
        'kh' : 'kʰ',
        'ph' : 'pʰ',
        't̠ʃ hʲ' : 't̠ʃʰ',
        'ɯ i' : 'ɯi',
        'ʌ' : 'ɤ̞',
        'ɛ' : 'æ' 
    },

    'it' : {
        # Match Italian Phoible inventory
        'a' : 'ɐ',
        'ɪ' : 'i',
        'ʊ ɔ' : 'w ɔ',
        'ʊ o' : 'w o',
        'ʊ' : 'o',
        'ss' : 'sː',
        'ei' : 'ɛ i',
        'ɐi' : 'a i',
        'd̪' : 'd',
    },

    'ca' : {
        # Match Catalan Phoible inventory
        'ɐ' : 'a',
        's' : 's̺',
        'n' : 'n̺',
        't ' : 't̪ ',
        'l' : 'ɫ̺',
        'ɾ' : 'ɾ̺',
        'r' : 'r̺',
        'ʎ' : 'ʎ̟',
        'z' : 'z̺',
        'd ' : 'd̪ ',
        'ɲ' : 'ɲ̟',
        'ʑ' : 'ʒ',
        'dʒ' : 'd̠ʒ',
        'ɕ' : 'ʃ',
        'tʃ' : 't̠ʃ',
        'ʊ' : 'u̯', # Not sure about this one
        'ʋ' : 'β', # Also not sure about this one
        'v' : 'β',
        'pː' : 'p',
        'ɟ' : 'ɡ',
    },

    'cy' : {
        # Match Welsh Phoible inventory
        ' ɨ ' : ' ɪ ',
        ' ɨː ' : ' iː ',
        'ɑɨ' : 'ai',
        'aɨ' : 'ai',
        'aɪ' : 'ai',
        'ɨu' : 'ɪu',
        'ɔɨ' : 'ɔi',
        'x' : 'χ',
        'əɨ' : 'əi',
        'uɨ' : 'ʊi',
        'aʊ' : 'au',
        'eʊ' : 'ɛu',
        'əɪ' : 'əi',
        'ɔɪ' : 'ɔi',
        'ç' : 'χ',
        'ɪuː' : 'ɪu',
        'ɨ' : 'ɪ',
    },

    'is' : {
        # Match Icelandic Phoible inventory
        'a ' : 'ä ',
        'n' : 'n̪',
        's' : 's̺',
        'ð' : 'ð̺̞',
        'θ' : 'θ̻',
        'ɾ' : 'r̥',
        't' : 't̪',
        'h r#' : 'r̥',
        'r r#' : 'r̥',
        'r r̥' : 'r̥',
        'r̥ r' : 'r̥',
        'n̪#' : 'n̪̥',
        'ɲ#' : 'ɲ̥',
        'ŋ#' : 'ŋ̥',
        't̪l#' : 't̪ ɬ',
        'l#' : 'l',
        'm#' : 'm̥',
        'y' : 'ʏ',
        'eɪː' : 'ei̯',
        'eɪ' : 'ei̯',
        'ʏɪ' : 'ʏi̯',
        'aʊː' : 'äu̯',
        'aʊ' : 'äu̯',
        'aɪː' : 'äi̯',
        'aɪ' : 'äi̯',
        'øʏː' : 'øɪ̯',
        'øʏ' : 'øɪ̯',
        'oʊː' : 'ou̯',
        'oʊ' : 'ou̯',
        'ɔɪ' : 'ɔi̯',
        'h d' : 't̪ t̪ʰ',
        'd n̪' : 'n̪',
        'n̪ d' : 'n̪ t̪ʰ',
        'd' : 't̪ʰ',
        'b' : 'pʰ',
        'ɟ' : 'cʰ',
        'ɣ' : 'ɰ',
        # Not sure about the following
        # 'iː' : 'i',
        # 'ɪː' : 'ɪ',
        # 'ʏː' : 'ʏ',
        # 'œː' : 'œ',
        # 'uː' : 'u',
        # 'ɔː' : 'ɔ',
        # 'ɛː' : 'ɛ',
        # 'aː' : 'a',
    },

    'da' : {
        # Fixing vowels
        'ʌ' : 'ɔ',
        # Fixing glottal stops on vowels
        'ʔɔ' : 'ɔˤ',
        'ʔeː' : 'eˤ',
        'ʔe' : 'eˤ',
        '?ɑ' : 'ɑˤː',
        'ʔi' : 'iˤ',
        'ʔu' : 'uˤ',
        'ʔœː' : 'œ', # Glottal marker doesn't seem to be present in phoible for this vowel
        'ʔœ' : 'œ',
        'ʔo' : 'oˤ',
        'ʔy' : 'y', # Glottal marker doesn't seem to be present in phoible for this vowel
        '?a' : 'aˤ',
        'aˤ ʔ' : 'aˤ',
        # Seems to be many errors with d being added before vowels
        'dɔ' : 'ɔ',
        'de' : 'e',
        'di' : 'i',
        # Fix vowels
        'ε' : 'ɛ',
        'ɐ̯' : 'r', # This one is correct but not in phoible, so we use /r/ instead
        'ɒɒ' : 'ɒː',
        'ɑɑ' : 'ɑˤː',
        'aa' : 'aˤ',
        'aɪ' : 'a i',
        # Fix consonants
        ' ʃ' : ' ɕ',
    },

    'nb' : {
        # Fix consonants
        'r' : 'ɾ',
        'k ' : 'kʰ ',
        't ' : 't̪ʰ ',
        'p ' : 'pʰ ',
        'v' : 'ʋ',
        'n' : 'n̪',
        'd ' : 'd̪ ',
        'x' : 'ç',
        #'tː' : 'ʈʰ',
        #'dː' : 'ɖ',
        'ɾ ɹ' : 'ɾ',
        # Fix vowels
        'aɪ' : 'ai',
        'oː' : 'o̞ː',
        'aʊ' : 'æʉ',
        'ɑɪ' : 'ɔy',
        'ɔɪ' : 'ɔy',
        'øː' : 'ø̞ː',
        'ɛː' : 'æ',
        'ɛ' : 'e̞',
        'aː' : 'æː',
        'ɔ ' : 'ɒ̝ ',
        ' y ' : ' ʏ ',
        'ʊː' : 'ʉː',
        'ʉɪ' : 'uː', # "juice"
    },

    'eu' : {
        # Match Basque Phoible inventory
        # Fix consonants
        't ' : 't̪ ',
        ' s̻' : ' s̪̻',
        'ts̺' : 't̺s̺',
        'ts̻' : 't̪̻s̪̻',
        'd' : 'd̪',
        # Fix diphthongs
        'aɪ' : 'ai̯',
        'aʊ' : 'au̯',
        'eɪ' : 'ei̯',
        'oɪ' : 'oi̯',
        'eʊ' : 'eu̯', 
    },

    'ro' : {
        # Match Romanian Phoible inventory
        # Fix vowels
        'ɔa' : 'o̯ä',
        'ea' : 'e̯ä',
        'a a ' : 'ä ',
        ' a ' : ' ä ',
        'e e ' : 'e̞ ',
        ' e ' : ' e̞ ',
        'o o' : 'o̞',
        ' o ' : ' o̞ ',
        'ɔ' : 'o̞',
        'yɪ' : 'aɪ',
        # Fix consonants
        'ɾ ' : 'ɾ̪ ',
        'r ' : 'ɾ̪ ', # Shouldn't have r and ɾ
        'rʲ ' : 'ɾʲ ',
        'n ' : 'n̪ ',
        't ' : 't̪ ',
        ' s ' : ' s̪ ',
        'ts ' : 't̪s̪ ',
        'd ' : 'd̪ ',
        'dʒ' : 'd̠ʒ',
        'z ' : 'z̪ ',
        'ŋ ' : 'n̪ ',
        # Fix double palatalised consonants
        'ʲʲ' : 'ʲ',
    },

    'pt-br' : {
        # Match Brazilian Portuguese Phoible inventory
        # Fix consonants
        't̠ʃ' : 't̪',
        't ' : 't̪ ',
        'd ' : 'd̪ ',
        'n' : 'n̪',
        's' : 's̪',
        'x' : 'ɣ',
        'ɹ' : 'r',
        'ɾ ə' : 'ɾ',
        # Fix vowels and diphthongs
        'aː' : 'a',
        ' æ ' : ' ɐ ',
        ' ʊ ' : ' u ',
        'ʊ ' : 'ʊ̯ ', # Fix end of dipthongs
        'ɪ ' : 'ɪ̯ ', # Fix end of dipthongs
        'ɐ̃ʊ̃' : 'ɐ̃ʊ̯̃',
        'y' : 'i',
        # Correct nasals - possibly more could be done for vowels that precede 'm' or 'n'
        'o ŋ' : 'õ',
        'ei ŋ' : 'ẽɪ̯̃',
        'i ŋ' : 'ĩ',
        'ɐ̃ ŋ' : 'ɐ̃',
        'ɐ̃ m' : 'ɐ̃',
        'u ŋ' : 'ũ',
        'ũ ŋ' : 'ũ',
        'eɪ̯ ŋ' : 'ẽɪ̯̃',
        # # Fix 'j'
        'j w' : 'iʊ̯',
        'j' : 'i',
        # Fix 'w'
        ' o w' : ' oʊ̯',
        'w i ' : 'ũɪ̯̃ ',
        's̪ w' : 's̪ u',
        'd̪ w' : 'd̪ u',
        'ɡ w' : 'ɡ u',
    },

    'ga' : {
        # Match Irish Phoible inventory
        # Fix consonants
        't̪ ' : 't̪ˠʰ ',
        's ' : 'sˠ ',
        'd̪ ' : 'd̪ˠ ',
        'd ' : 'd̪ˠ ',
        'dʲ ' : 'd̪ʲ ',
        'm ' : 'mˠ ',
        'c ' : 'cʰ ',
        'çʲ' : 'ç',
        'k ' : 'kʰ ',
        'kʲ ' : 'kʰ ',
        'ɡʲ ' : 'ɡ ',
        'lʲ l ' : 'l̪ˠ ',
        'lʲʲ' : 'l̪ʲ',
        'lʲ' : 'l̪ʲ',
        'l ' : 'l̪ˠ ',
        'b ' : 'bˠ ',
        'n ' : 'n̪ˠ ',
        'nʲ ' : 'n̪ʲ ',
        'f ' : 'fˠ ',
        'ʁ' : 'ɾ̪ˠ',
        'ɹ ' : 'ɾ̪ˠ ',
        'r ' : 'ɾ̪ʲ ',
        't̠ʃ' : 't̪ʲʰ ',
        't ' : 't̪ʲʰ ',
        'v ' : 'vˠ ',
        'p ' : 'pˠʰ ',
        'pʲ ' : 'pʲʰ ',
        'hʲ' : 'h',
        'ŋʲ' : 'ŋ',
        # Fix vowels
        ' ɔ ' : ' ɔ̝ ',
        ' A ' : ' a ',
        ' ɐ ' : ' ə ',
        ' i̯ ' : ' i̞ ',
        ' ɛ ' : ' ɛ̝ ',
        'eɪ' : 'ɐɪ',
        'uə' : 'uːe',
        'iə' : 'iːə',
        ' u ' : ' ʊ ',
        ' ŭ ' : ' ʊ ',
        ' aɪ ' : ' iː ',
        ' aʊ ' : ' a ',
        # Other fixes
        'ə χ' : 'ə',
        'χ ə' : 'ɡ',
        'n j' : 'n̪ʲ',
        ' ʲ ' : ' ',
    },

    'tr' : {
        # Match Turkish Phoible inventory
        # Fix consonants
        'n' : 'n̪',
        'r' : 'ɾ',
        'z' : 'z̪',
        ' s' : ' s̪',
        't ' : 't̪ ',
        'tː' : 't̪',
        'dː' : 'd̪',
        'd ' : 'd̪ ',
        'l' : 'lʲ', # These might be the wrong way
        'ɫ' : 'l̪ˠ',
        'kː' : 'k',

        # Fix vowels
        'e' : 'eː',
        'ɛ' : 'e',
        'i' : 'iː',
        'ɪ' : 'i',
        'ɔ' : 'o',
        'oː' : 'o',
        'ʊː' : 'u',        
        'ʊ' : 'u',        
        'ø' : 'y',
        'yː' : 'y',
        'æ' : 'e',
        'ɯɯ' : 'ɯ',
        'œː' : 'œ',
    },

    'qu' : {
        # Match Quechua Phoible inventory
        # Fix consonants
        'p`' : 'pʼ',
        'k`' : 'kʼ',
        't`' : 'tʼ',
        't̠ʃ`' : 't̠ʃʼ',
        'q`' : 'qʼ',
        'v' : 'β',
        'b' : 'β',
        'g' : 'ɣ',
        'n g' : 'ɲ',
        'z' : 's',

        # Fix vowels
        'i' : 'ɪ',
        'u' : 'ʊ',
        'e' : 'ɛ',
        'o' : 'ɔ',
    },

    'fa-latn' : {
        # Match Persian Phoible inventory
        'q 1' : 'ɢ',
        'd ' : 'd̪ ',
        'n' : 'n̪',
        'k' : 'kʰ',
        't ' : 't̪ʰ ',
        'a' : 'a̟',
        'p' : 'pʰ',
    }
}
    
FOLDING_PINYIN_TO_IPA = {
    # Fix diphthongs
    'ou̯' : 'ou',
    'ei̯' : 'ei',
    'ai̯' : 'ai',
    'ʈʂʰ' : 't̠ʃ̺ʰ',
    'ʈʂ' : 't̠ʃ̺',
    'au̯' : 'au',
    'ʂ' : 'ʃ̺',
    'ɹ̩' : 'ɹ̪̩',
    'h ' : '',
    '  ' : ' ',
}


FOLDING_PINGYAM = {
    '  ' : ' ',

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

	# Long vowels - remove marker to match inventory
	'i ː' : 'i',
	'a ː' : 'a̞',
	'ɛ ː' : 'ɛ',
	'ɔ ː' : 'ɔ̽',
	'u ː' : 'u',
	'y ː' : 'y',
	'œ ː' : 'œ̞',

	# Aspirated consonants
	't s ʰ' : 'tsʰ',
	't s' : 'ts',
	't ʰ' : 'tʰ',
	'k ʰ' : 'kʰ',
	'p ʰ' : 'pʰ',
	'm ̩ ː' : 'm̩', # Doesn't actually appear in phoible, so we remove vowel length marker

    # Match phoible inventory
    'ɪ' : 'ɪ̞',
    'ʊ' : 'ʊ̟',
    ' ̩' : '̩',

}

FOLDING_EPITRAN = {
    # All Epitran output
	'all' : {
        # Attach ipa markers to their phonemes
        ' ̚' : '̚',
        ' ̈' : '̈',
        ' ˆ' : 'ˆ',
        ' ̂' : '̂',

        # Removing the double breve and other diacritics unknown to phoible
        'ʈ͡ʂʰ' : 't̠ʃ̺ʰ',
        'ʈ͡ʂ' : 't̠ʃ̺',
        'ʂ' : 'ʃ̺',
        't͡ɕʰ' : 'tɕʰ',
        't͡ɕ' : 'tɕ',
        't͡s' : 'ts',
        't͡sʰ' : 'tsʰ',
        'p͡f' : 'pf',
        'd͡ʒ' : 'd̠ʒ',
        't͡ʃ' : 't̠ʃ',
        'd͡ʑ' : 'd̠ʒ',
        'tɕ' : 't̠ʃ',
        't͡ɬ' : 'tl',
        'ɐ̯' : 'ɐ',
        'ɪ̯̈' : 'ɪ̯',
        'ŋ̈' : 'ŋ',
        'ʊ̯̈' : 'ʊ̯',
        'v̈' : 'v',
        'ɡ̈' : 'ɡ',
        'g' : 'ɡ',
        'ç' : 'ç', 

        '  ' : ' ',
	},
    
	'yue-Latn' : {
        # Join tone markers
        '˧ ˥' : '˧˥',
        '˨ ˥' : '˨˥',
		'˨ ˩' : '˧˩̰',
		'˩ ˧' : '˩˧', 
        '˨ ˧' : '˨˧',
		'˨': '˨',
		'˥' : '˥',
		'˧' : '˧',

        # Diphthongs
        'e i' : 'ei',
        'a i' : 'ai',
        'ɔ i' : 'ɔi',
        'ɛ u' : 'ɛu',
        'a u' : 'au',
        'o u' : 'ou',
        'ɐ u' : 'ɐu',
        'ɵ y' : 'ɵy',
        'ɐ i' : 'ɐi',
        'u i' : 'ui',
        'i u' : 'iu',

        # Fix ts
        't s' : 'ts',
        't s ʰ' : 'tsʰ',

        # Fix other
        '6 ' : '',
        '8 ' : '',
	},
    
	'cmn-Latn' : {
        '1' : '˥',
        '2' : '˧˥',
        '3' : '˨˩',
        '4' : '˥˩',
        '5' : '˧',
	},
	
	'cmn-Hans' : {
        # Join tone markers
        '˧ ˥' : '˧˥',
        '˨ ˩' : '˨˩',
        '˥ ˩' : '˥˩',

        # Diphthongs - this might join too many phonemes
        'u a i' : 'uai',
        'u e i' : 'uei',
        'i a u' : 'iau',
        'i o u' : 'iou',
        'i e' : 'ie',
        'a i' : 'ai',
        'i a' : 'ia',
        'u ə' : 'uə',
        'y e' : 'ye',
        'y e' : 'ye',
        'a u' : 'au',
        'o u' : 'ou',
        'e i' : 'ei',
        'u o' : 'uo',
        'u a' : 'ua',
        'i u' : 'iu',
	},

    'deu-Latn' : {
        # Removing strange output
        'E' : 'ə',
        ' A ' : ' a ',
        'Z' : 'z',
        'I' : 'iː',
        'Ø' : 'øː',
        ': ' : '',
        'q' : 'kʰ', # Caused by transcription error, q is in the orthographic text incorrectly
        'ˆ' : '', # Caused by transcription error, ˆ is in the orthographic text incorrectly
        'ä h' : 'ɛː', # Caused by transcription error
        'D ' : '', 
        'iː̂' : 'iː',
        'aː̈' : 'aː',
        'e̯' : 'ɛ',
        'uː̈' : 'uː',
        'uː̂' : 'uː',
        '̊' : '',
        '́' : '',
        'r̥ ' : 'ʀ ',
        'rˆ ' : 'ʀ ',
        'oː̈' : 'oː',

        # Matching phoible inventory for German
        'r ' : 'ʀ ',
        'd ' : 'd̺ ',
        'k ' : 'kʰ ',
        't ' : 't̺ʰ ',
        'p ' : 'pʰ ',
        'ɪ̯ ' : 'ɪ ',
        'ʊ̯ ' : 'ʊ ',
        'i ' : 'iː ',
        'e ' : 'eː ',
        'u ' : 'uː ',
        'y ' : 'ʏ ',
        'o ' : 'oː ',
        'ø ' : 'øː ',
        'ä ' : 'ɛː ',
    },

    'ind-Latn' : {
        'ɕ' : 'ʃ',
        '̀' : '',
        '́' : '',
    },

    'spa-Latn' : {
        'e' : 'e̞',
        'b' : 'β',
        '̀' : '',
        '̧' : '',
        'o ' : 'o̞ ',
        'î' : 'i',
        'k̈' : 'k',
        'ê̞' : 'e̞',

        # Match Phoible inventory for Spanish
        'ɛ' : 'e̞',
        'ö' : 'o̞',
        'ü' : 'u',
        'ä' : 'a',
        'ï' : 'i',
        'ë̞' : 'e̞',
        'ɘ' : 'e̞',
    },

    'srp-Latn' : {
        # Match Phoible inventory for Serbian
        'ʃ' : 'ʃ̺',
        't ɕ' : 't̻ʃ̻',
        't̪̻ ɕ' : 't̻ʃ̻',
        'd ʒ' : 'd̻ʒ̻',
        'd̪̻ ʒ' : 'd̻ʒ̻',
        'd̪̻ ʒ̺' : 'd̻ʒ̻',
        'd ʒ̺' : 'd̻ʒ̻',
        'd ʑ' : 'd̻ʒ̻',
        't s' : 't̪̻s̪̻',
        ' s' : ' s̪̻',
        ' ʒ' : ' ʒ̺',
        't ' : 't̪̻ ',
        'd ' : 'd̪̻ ',
        'a' : 'ä',
        'eː' : 'e̞ː',
        'ɑː' : 'äː',
        'v' : 'ʋ',
        'z' : 'z̪̻',
        'o' : 'o̞',
        'h' : 'x',
        'ʉ' : 'u',
        'ɪ' : 'i',
        'e' : 'e̞',
        'n̩' : 'n',
        'l̩' : 'l',
        ' ́' : '',
        'ä̈' : 'ä',
     },

     'hrv-Latn' : {
        # Match Phoible inventory for Croatian
        't ' : 't̪ ',
        'd ' : 'd̪ ',
        'v' : 'ʋ',
        'ts' : 't̪s',
     },

     'hun-Latn' : {
        # Match Phoible inventory for Hungarian
        'ɒ' : 'ɑ',
        't ' : 't̪ ',
        'tː ' : 't̪ː ',
        ' s' : ' s̻',
        'ts' : 't̻s̻',
        'd ' : 'd̪ ',
        'dː' : 'd̪ː',
        ' z' : ' z̻',
        'd͡z' : 'd̻z̻',
        'n' : 'n̪',
        'l' : 'l̪',
        'r' : 'r̪',
        'ɟ' : 'ɟʝ',
        'c' : 'cç',
        'ô' : 'øː', # Caused by transcription error, ô is in the orthographic text but should be ő
        'û' : 'øː', # Caused by transcription error, û is in the orthographic text but should be ű
        'õ' : 'øː', # Caused by transcription error, 
        'q' : 'r̪ k', # Caused by transcription error, q is in the orthographic text but should be k
     }
    
}