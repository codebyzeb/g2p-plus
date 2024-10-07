""" Wrapper for pingyam library for converting Cantonese  to IPA. """

import os
import pandas as pd
import re

from ..dicts import FOLDING_PINGYAM
from .wrapper import Wrapper
from ..utils import move_tone_marker_to_after_vowel

PINGYAM_PATH = os.path.join(os.path.dirname(__file__), '../../data/pingyam/pingyambiu')

class PingyamWrapper(Wrapper):

    SUPPORTED_LANGUAGES = ['cantonese']

    @staticmethod
    def supported_languages_message():
        message = 'The PingyamWrapper uses the pingyam library, which only supports `cantonese`.\n'
        return message
    
    def phonemize(self, lines):
        """ Uses pingyam library to convert Cantonese from jyutping to IPA. """

        broken = 0
        phonemized_utterances = []

        # Load pingyam database
        cantonese_dict = pd.read_csv(PINGYAM_PATH, sep='\t', header=None)[[5, 6]]
        cantonese_dict.columns = ['ipa', 'jyutping']
        cantonese_dict = cantonese_dict.set_index('jyutping').to_dict()['ipa']

        # Convert jyutping to IPA
        for line in lines:
            if line.strip() == '':
                phonemized_utterances.append('')
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
                        syll = cantonese_dict[syllable]
                        syll = move_tone_marker_to_after_vowel(syll)
                        phonemized += syll + ''
                phonemized += '_'
            if line_broken:
                phonemized = ''
            phonemized_utterances.append(phonemized)

        if broken > 0:
            self.logger.debug(f'WARNING: {broken} lines were not phonemized successfully by jyutping to ipa conversion.')
        
        # Separate phonemes with spaces and add word boundaries
        # The spaces between multi-character phonemes are fixed by the folding dictionary, which
        # also attaches tone markers to the vowels
        for i in range(len(phonemized_utterances)):
            phonemized_utterances[i] = ' '.join(list(phonemized_utterances[i]))
            phonemized_utterances[i] = phonemized_utterances[i].replace('_', 'WORD_BOUNDARY' if self.keep_word_boundaries else ' ')

        if self.use_folding:
            phonemized_utterances = self._post_process_pingyam_output(phonemized_utterances)
        else:
            self.logger.debug("Skipping folding dictionary post-processing, using uncorrected output from pingyam.")

        return phonemized_utterances

    def _post_process_pingyam_output(self, lines):
        """Corrects output from pinyin_to_ipa library. """

        for i in range(len(lines)):
            if lines[i] == '' or lines[i] == ' ':
                continue
            for key, value in FOLDING_PINGYAM.items():
                lines[i] = lines[i].replace(key, value)

        return lines