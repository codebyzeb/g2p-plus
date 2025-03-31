""" 
Wrapper for converting text to IPA phonemes using the phonemizer library.

This wrapper provides access to multiple transcription backends:
- espeak-ng: Supports 100+ languages and accents
- segments: Used specifically for Japanese transcription

The wrapper handles stress markers, word boundaries, and various configuration
options for fine-tuning the transcription process.
"""

import logging
import os
import re
import subprocess
from phonemizer import phonemize
from phonemizer.separator import Separator

from g2p_plus.wrappers.wrapper import Wrapper

SECONDARY_STRESS = 'ˈ'  # Secondary stress marker used by espeak-ng
PRIMARY_STRESS = "'"    # Primary stress marker used by espeak-ng

class PhonemizerWrapper(Wrapper):
    """
    Wrapper for the phonemizer library's text-to-phoneme conversion.

    This wrapper supports multiple transcription backends and provides various
    configuration options. It uses espeak-ng for most languages and the segments
    backend specifically for Japanese.

    Class Attributes:
        WRAPPER_KWARGS_TYPES (dict): Type checking for configuration options
        WRAPPER_KWARGS_DEFAULTS (dict): Default values for configuration options
        KWARGS_HELP (dict): Help text explaining each configuration option
    """

    WRAPPER_KWARGS_TYPES = {
        'allow_possibly_faulty_word_boundaries': bool,
        'preserve_punctuation': bool,
        'with_stress': bool,
    }

    WRAPPER_KWARGS_DEFAULTS = {
        'allow_possibly_faulty_word_boundaries': False,
        'preserve_punctuation': False,
        'with_stress': False,
    }

    KWARGS_HELP = {
        'allow_possibly_faulty_word_boundaries': 'Allow possibly faulty word boundaries (otherwise removes lines with mismatched word boundaries).',
        'preserve_punctuation': 'Preserve punctuation in the transcribed output.',
        'with_stress': 'Include stress markers in the transcribed output.',
    }

    @staticmethod
    def supported_languages_message():
        """
        Returns information about supported languages and backends.

        Returns:
            str: Detailed message about language support and backend selection
        """
        message = 'The PhonemizerWrapper uses the phonemizer library, which supports multiple backends.\n'
        message += 'For Japanese (language="ja"), the segments backend is used.\n'
        message += 'For all other languages, the espeak-ng backend, which supports over 127 languages and accents.\n'
        message += 'For a list of supported languages, run `espeak-ng --voices` or see https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md\n'
        return message

    def __init__(self, language, keep_word_boundaries=True, verbose=False, use_folding=True, **wrapper_kwargs):
        """
        Initializes the wrapper with phonemizer-specific configurations.

        In addition to the base Wrapper parameters, this sets up:
        - Separator configuration for phones, words, and syllables
        - Word boundary mismatch handling
        - Multi-processing settings
        """
        super().__init__(language, keep_word_boundaries, verbose, use_folding, **wrapper_kwargs)
        self.separator = Separator(phone='PHONE_BOUNDARY', word=' ', syllable='')
        self.strip = True
        self.language_switch = 'remove-utterance'

        # Configure word boundary mismatch handling
        self.words_mismatch = 'ignore' if self.allow_possibly_faulty_word_boundaries or not self.keep_word_boundaries else 'remove'
        self.njobs = 4

    def check_language_support(self, language):
        """ 
        Checks if a language is supported by the appropriate backend.
        
        Args:
            language (str): Language code to check

        Returns:
            bool: True if the language is supported

        Raises:
            ValueError: If PHONEMIZER_ESPEAK_LIBRARY environment variable is not set
        """
        if language == 'ja':
            return True
        if os.getenv('PHONEMIZER_ESPEAK_LIBRARY') is None:
            raise ValueError('PHONEMIZER_ESPEAK_LIBRARY is not set. Please set it to the path of the espeak-ng library. See README.md for more information: https://github.com/codebyzeb/g2p-plus/blob/main/README.md')
        if language in self.get_supported_languages():
            return True
        return False
        
    def get_supported_languages(self):
        """ 
        Gets list of languages supported by espeak-ng backend.

        Returns:
            list[str]: List of supported language codes, empty if espeak-ng
                      is not installed
        """
        try:
            output = subprocess.run(['espeak-ng', '--voices'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
            languages = [re.sub(r'\s+', ' ', l.strip()).split(' ')[1] for l in output.strip().split('\n')][1:]
            return languages
        except subprocess.CalledProcessError:
            self.logger.error('Phonemizer requires espeak-ng to be installed. Please install espeak-ng.')
            return []
        
    def _transcribe(self, lines):
        """ 
        Converts text to phonemes using the appropriate backend.

        Uses the segments backend for Japanese and espeak-ng for all other
        languages. Failed conversions return empty strings.

        Args:
            lines (list[str]): Text strings to convert to phonemes

        Returns:
            list[str]: Transcribed versions of input lines
        """
        if self.language == 'ja':
            transcribed_lines = self._transcribe_japanese(lines)
        else:
            transcribed_lines = self._transcribe_utterances(lines)
        return transcribed_lines

    def _transcribe_japanese(self, lines):
        """ 
        Transcribes Japanese text using the segments backend.

        Args:
            lines (list[str]): Japanese text strings to transcribe

        Returns:
            list[str]: Transcribed Japanese text
        """
        self.logger.debug('Using the segments backend to transcribe Japanese text.')
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
            self.logger.debug(f'{missed_lines} lines were not transcribed due to errors with the segments file.')

        return phn
    
    def _transcribe_utterances(self, lines):
        """ 
        Transcribes text using the espeak-ng backend.

        Args:
            lines (list[str]): Text strings to transcribe

        Returns:
            list[str]: Transcribed text strings
        """
        self.logger.debug(f'Using espeak backend with language code "{self.language}"...')
        logging.disable(logging.WARNING)
        phn = phonemize(
            lines,
            language=self.language,
            backend='espeak',
            separator=self.separator,
            strip=self.strip,
            preserve_punctuation=self.preserve_punctuation,
            language_switch=self.language_switch,
            words_mismatch=self.words_mismatch,
            with_stress=self.with_stress,
            njobs=self.njobs)
        logging.disable(logging.NOTSET)
        
        return phn

    def _post_process_line(self, line):
        """
        Post-processes transcribed output to handle word boundaries and spacing.

        Args:
            line (str): Transcribed line to process

        Returns:
            str: Processed line with proper word boundaries and spacing
        """
        if self.keep_word_boundaries:
            line = line.replace(' ', ' WORD_BOUNDARY ')
        line = line.replace('PHONE_BOUNDARY', ' ')
        line = super()._post_process_line(line)
        if self.keep_word_boundaries:
            line = line + ' WORD_BOUNDARY'
        return line

