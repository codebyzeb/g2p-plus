""" Wrapper for pinyin_to_ipa library for converting Mandarin pinyin to IPA. """

import re

from pinyin_to_ipa import pinyin_to_ipa
from ..dicts import FOLDING_PINYIN_TO_IPA
from .wrapper import Wrapper

class PinyinToIpaWrapper(Wrapper):

    SUPPORTED_LANGUAGES = ['mandarin']

    @staticmethod
    def supported_languages_message():
        message = 'The PinyinToIpaWrapper uses the pinyin_to_ipa library, which only supports `mandarin`.\n'
        return message
    
    def phonemize(self, lines):
        """ Uses pinyin_to_ipa library to convert Mandarin pinyin to IPA. """

        phonemized_utterances = []
        broken = 0
        for line in lines:
            if line.strip() == '':
                phonemized_utterances.append('')
                continue
            phonemized = ""
            words = line.split(' ')
            try:
                for word in words:
                    syllables = re.findall(r'[a-zA-Z]+[0-9]*', word)
                    syllables = [re.sub(r'[0]', '', syllable) for syllable in syllables]
                    for syllable in syllables:
                        syll_set = pinyin_to_ipa(syllable)
                        syll = ' '.join(syll_set[0])
                        phonemized += syll + ' '
                    if self.keep_word_boundaries:
                        phonemized += 'WORD_BOUNDARY '
            except Exception as e:
                phonemized = ""
                broken += 1

        if broken > 0:
            self.logger.debug(f'WARNING: {broken} lines were not phonemized successfully by pinyin to ipa conversion.')

        return phonemized_utterances

    def _post_process_pinyin_to_ipa_output(self, lines):
        """Corrects output from pinyin_to_ipa library. """

        for i in range(len(lines)):
            if lines[i] == '' or lines[i] == ' ':
                continue
            for key, value in FOLDING_PINYIN_TO_IPA.items():
                lines[i] = lines[i].replace(key, value)

