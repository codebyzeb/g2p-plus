""" Wrapper for the phonemizer library. """

import os
import re
import subprocess
from phonemizer import phonemize
from phonemizer.separator import Separator

from ..dicts import FOLDING_PHONEMIZER
from .wrapper import Wrapper

class PhonemizerWrapper(Wrapper):

    WRAPPER_KWARGS_TYPES = {
        'allow_possibly_faulty_word_boundaries': bool,
        'preserve_punctuation': bool,
    }

    WRAPPER_KWARGS_DEFAULTS = {
        'allow_possibly_faulty_word_boundaries': False,
        'preserve_punctuation': False,
    }

    KWARGS_HELP = {
        'allow_possibly_faulty_word_boundaries': 'Allow possibly faulty word boundaries (otherwise removes lines with mismatched word boundaries).',
        'preserve_punctuation': 'Preserve punctuation.',
    }

    @staticmethod
    def supported_languages_message():
        message = 'The PhonemizerWrapper uses the phonemizer library, which supports multiple backends.\n'
        message += 'For Japanese (language="ja"), the segments backend is used.\n'
        message += 'For all other languages, the espeak-ng backend, which supports over 127 languages and accents.\n'
        message += 'For a list of supported languages, run `espeak-ng --voices` or see https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md\n'
        return message

    def __init__(self, language, keep_word_boundaries=True, verbose=False, **wrapper_kwargs):
        super().__init__(language, keep_word_boundaries, verbose, **wrapper_kwargs)
        self.separator = Separator(phone='PHONE_BOUNDARY', word=' ', syllable='')
        self.strip = True
        self.language_switch = 'remove-utterance'

        # This setting removes utterances that the backend produces with a different number of words.
        # If we are not keeping word boundaries, this does not matter.
        self.words_mismatch = 'ignore' if self.allow_possibly_faulty_word_boundaries or not self.keep_word_boundaries else 'remove'
        self.njobs = 4

    def check_language_support(self, language):
        """ Checks if the language is supported by the wrapper. """
        
        if language == 'ja':
            return True
        # Check if PHONEMIZER_ESPEAK_LIBRARY is set
        if os.getenv('PHONEMIZER_ESPEAK_LIBRARY') is None:
            raise ValueError('PHONEMIZER_ESPEAK_LIBRARY is not set. Please set it to the path of the espeak-ng library. See README.md for more information.')
        if language in self.get_supported_languages():
            return True
        return False
        
    def get_supported_languages(self):
        """ Returns a list of supported languages for the wrapper. """
        try:
            output = subprocess.run(['espeak-ng', '--voices'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
            languages = [re.sub(r'\s+', ' ', l.strip()).split(' ')[1] for l in output.strip().split('\n')][1:]
            return languages
        except subprocess.CalledProcessError:
            self.logger.error('Phonemizer requires espeak-ng to be installed. Please install espeak-ng.')
            return []
        
    def phonemize(self, lines):
        """ Uses phonemizer to phonemize text. Returns a list of phonemized lines. Lines that could not be phonemized are returned as empty strings."""
        if self.language == 'ja':
            # Japanese is not supported by espeak, so we use the segments backend.
            phonemized_lines = self._phonemize_japanese(lines)
        else:
            phonemized_lines = self._phonemize_utterances(lines)

        phonemized_lines = self._post_process_phonemizer_output(phonemized_lines)

        return phonemized_lines

    def _phonemize_japanese(self, lines):
        """ Uses phonemizer with segments backend to phonemize Japanese text."""

        self.logger.debug('Using the segments backend to phonemize Japanese text.')
        phn = []
        missed_lines = 0
        for line in lines:
            try:
                phn.append(phonemize(
                    line,
                    language='japanese',
                    backend='segments',
                    separator=self.separator,
                    strip=self.strip,
                    preserve_punctuation=self.preserve_punctuation)) 
            except ValueError:
                missed_lines += 1
                phn.append('')
        if missed_lines > 0:
            self.logger.debug(f'{missed_lines} lines were not phonemized due to errors with the segments file.')

        return phn
    
    def _phonemize_utterances(self, lines):
        """ Uses phonemizer with the espeak backend to phonemize text. """
        
        self.logger.debug(f'Using espeak backend with language code "{self.language}"...')
        phn = phonemize(
            lines,
            language=self.language,
            backend='espeak',
            separator=self.separator,
            strip=self.strip,
            preserve_punctuation=self.preserve_punctuation,
            language_switch=self.language_switch,
            words_mismatch=self.words_mismatch,
            njobs=self.njobs)
        
        return phn

    def _post_process_phonemizer_output(self, lines):
        """ Removes phone boundary markers, adds word boundary markers, removes extra spaces and corrects general espeak output. """

        if self.language not in FOLDING_PHONEMIZER:
            self.logger.debug(f'No folding dictionary found for language code: "{self.language}".')

        for i in range(len(lines)):
            if lines[i] == '' or lines[i] == ' ':
                continue
            if self.keep_word_boundaries:
                lines[i] = lines[i].replace(' ', ' WORD_BOUNDARY ')
            lines[i] = lines[i].replace('PHONE_BOUNDARY', ' ')
            for key, value in FOLDING_PHONEMIZER['all'].items():
                lines[i] = lines[i].replace(key, value)
            if self.language in FOLDING_PHONEMIZER:
                for key, value in FOLDING_PHONEMIZER[self.language].items():
                    lines[i] = lines[i].replace(key, value)
            if self.keep_word_boundaries:
                lines[i] = lines[i] + ' WORD_BOUNDARY'

        return lines
