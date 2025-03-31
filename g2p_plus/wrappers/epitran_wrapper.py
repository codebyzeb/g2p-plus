""" 
Wrapper for the Epitran library for phonetic transcription.

This wrapper utilizes the Epitran library to convert text from various languages
into their corresponding phonetic representations in the International Phonetic Alphabet (IPA).
It supports a wide range of languages and scripts, making it a versatile tool for phonetic transcription.

The wrapper is designed to handle language-specific nuances and provides options for
normalizing punctuation and handling ligatures.
"""

import os
import re
import subprocess

from epitran import Epitran
from g2p_plus.wrappers.wrapper import Wrapper

class EpitranWrapper(Wrapper):
    """
    A wrapper class for phonetic transcription using the Epitran library.

    This class provides methods to transcribe text into IPA phonemes for various languages.
    It includes support for language-specific features such as tone markers and ligatures.

    Class Attributes:
        SUPPORTED_LANGUAGES (list): A list of language codes supported by the Epitran library.
        CEDICT (str): Path to the CEDICT file used for Chinese language support.

    Methods:
        supported_languages_message(): Returns a message indicating supported languages.
        check_language_support(language): Checks if a given language is supported.
        _transcribe(lines): Transcribes input lines into IPA phonemes.
        _post_process_line(line): Applies post-processing to the transcribed line.
    """

    # TODO: Check support from epitran library instead of hardcoding.
    # See https://github.com/dmort27/epitran#language-support
    SUPPORTED_LANGUAGES = ['aar-Latn', 'aii-Syrc', 'amh-Ethi', 'amh-Ethi-pp', 'amh-Ethi-red', 'ara-Arab', 'ava-Cyrl', 'aze-Cyrl', 'aze-Latn', 'ben-Beng', 'ben-Beng-red', 'bxk-Latn', 'cat-Latn', 'ceb-Latn', 'ces-Latn', 'cjy-Latn', 'cmn-Hans', 'cmn-Hant', 'cmn-Latn', 'ckb-Arab', 'csb-Latn', 'deu-Latn', 'deu-Latn-np', 'deu-Latn-nar', 'eng-Latn', 'epo-Latn', 'fas-Arab', 'fra-Latn', 'fra-Latn-np', 'fra-Latn-p', 'ful-Latn', 'gan-Latn', 'got-Latn', 'hak-Latn', 'hau-Latn', 'hin-Deva', 'hmn-Latn', 'hrv-Latn', 'hsn-Latn', 'hun-Latn', 'ilo-Latn', 'ind-Latn', 'ita-Latn', 'jam-Latn', 'jav-Latn', 'kaz-Cyrl', 'kaz-Cyrl-bab', 'kaz-Latn', 'kbd-Cyrl', 'khm-Khmr', 'kin-Latn', 'kir-Arab', 'kir-Cyrl', 'kir-Latn', 'kmr-Latn', 'kmr-Latn-red', 'kor-Hang', 'lao-Laoo', 'lij-Latn', 'lsm-Latn', 'ltc-Latn-bax', 'mal-Mlym', 'mar-Deva', 'mlt-Latn', 'mon-Cyrl-bab', 'mri-Latn', 'msa-Latn', 'mya-Mymr', 'nan-Latn', 'nan-Latn-tl', 'nld-Latn', 'nya-Latn', 'ood-Lat-alv', 'ood-Latn-sax', 'ori-Orya', 'orm-Latn', 'pan-Guru', 'pol-Latn', 'por-Latn', 'quy-Latn', 'ron-Latn', 'run-Latn', 'rus-Cyrl', 'sag-Latn', 'sin-Sinh', 'sna-Latn', 'som-Latn', 'spa-Latn', 'spa-Latn-red', 'sqi-Latn', 'srp-Latn', 'swa-Latn', 'swe-Latn', 'tam-Taml-red', 'tam-Taml', 'tel-Telu', 'tgk-Cyrl', 'tgl-Latn-red', 'tgl-Latn', 'tha-Thai', 'tir-Ethi', 'tir-Ethi-pp', 'tir-Ethi-red', 'tpi-Latn', 'tuk-Cyrl', 'tuk-Latn', 'tur-Latn', 'tur-Latn-bab', 'tur-Latn-red', 'ukr-Cyrl', 'urd-Arab', 'uig-Arab', 'uzb-Cyrl', 'uzb-Latn', 'vie-Latn', 'wuu-Latn', 'xho-Latn', 'yor-Latn', 'yue-Latn', 'zha-Latn', 'zul-Latn']
    CEDICT = os.path.join(os.path.dirname(__file__), '../data/cedict_ts.u8')

    @staticmethod
    def supported_languages_message():
        """
        Returns a message indicating the supported languages for this wrapper.

        Returns:
            str: Message indicating the languages supported by the EpitranWrapper.
        """
        message = 'The EpitranWrapper uses the epitran library, which supports multiple backends.\n'
        message += 'For a list of supported languages, see https://github.com/dmort27/epitran#language-support\n'
        return message

    def __init__(self, language, keep_word_boundaries=True, verbose=False, use_folding=True, **wrapper_kwargs):
        """
        Initializes the EpitranWrapper with the specified language and options.

        Args:
            language (str): The language code for transcription.
            keep_word_boundaries (bool): If True, keeps word boundaries in the output.
            verbose (bool): If True, enables verbose logging.
            use_folding (bool): If True, applies folding to the phoneme output.
            **wrapper_kwargs: Additional keyword arguments for customization.
        """
        super().__init__(language, keep_word_boundaries, verbose, use_folding, **wrapper_kwargs)
        self.norm_punc = False
        self.ligatures = False
        self.epi = Epitran(self.language, tones=True, cedict_file=self.CEDICT, ligatures=self.ligatures)
        
    def check_language_support(self, language):
        """ 
        Checks if the specified language is supported by the EpitranWrapper.

        Args:
            language (str): The language code to check.

        Returns:
            bool: True if the language is supported, False otherwise.
        """
        if language in self.SUPPORTED_LANGUAGES:
            if 'cmn-' in language:
                if os.path.exists(self.CEDICT):
                    self.logger.debug(f'CEDICT found at {self.CEDICT}.')
                else:
                    self.logger.error(f'CEDICT not found at {self.CEDICT}. Please download the CC_CEDICT file from https://www.mdbg.net/chinese/dictionary?page=cedict and place it in {os.path.dirname(self.CEDICT)}.')
                    return False
            elif language == 'eng-Latn':
                try:
                    subprocess.run(['lex_lookup', 'hello'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    self.logger.error('Epitran requires Flite to be installed. Please install Flite and ensure that lex_lookup is in your system PATH. Instructions at https://github.com/dmort27/epitran#installation-of-flite-for-english-g2p')
                    return False
            return True
        return False

    def _transcribe(self, lines):
        """ 
        Transcribes input lines into IPA phonemes using the Epitran library.

        This method processes each line of text, applying necessary transformations
        and returning the phonetic transcription.

        Args:
            lines (list[str]): List of text strings to convert to phonemes.

        Returns:
            list[str]: List of transcribed lines. Lines that could not be transcribed
                        are returned as empty strings.
        """
        self.logger.debug(f'Using epitran backend with language code "{self.language}"...')
        
        transcribed_lines = []
        for line in lines:
            # Replace duplicate whitespace with single space and strip punctuation
            line = re.sub(r'\s+', ' ', line).strip()
            line = re.sub(r'[^\w\s]', '', line)

            if self.language == 'yue-Latn':
                line = self._transcribe_yue_latn(line)
            else:
                line = self.epi.trans_delimiter(line + ' ', delimiter='PHONE_BOUNDARY', normpunc=self.norm_punc, ligatures=self.ligatures)
                line = line.replace('PHONE_BOUNDARY ', ' WORD_BOUNDARY' if self.keep_word_boundaries else '')
                line = line.replace('WORD_BOUNDARY WORD_BOUNDARY', 'WORD_BOUNDARY')
                line = line.replace('PHONE_BOUNDARY', ' ')
            transcribed_lines.append(line)
        return transcribed_lines
    
    def _transcribe_yue_latn(self, line):
        """ 
        Transcribes Cantonese Jyutping to IPA phonemes.

        This method handles the specific case for Cantonese, where tone markers
        must be correctly positioned. It splits words into syllables for accurate
        transcription.

        Args:
            line (str): A line of Jyutping text to transcribe.

        Returns:
            str: The transcribed line in IPA phonemes.
        """
        words = [word for word in line.split()]
        words = [re.sub(r'\d', lambda x: x.group() + '_', word) for word in words]
        words = [word.split('_')[:-1] for word in words]
        words = [[self.epi.trans_delimiter(syll, normpunc=self.norm_punc, ligatures=self.ligatures).strip() for syll in word] for word in words]
        words = [' '.join(word) for word in words]
        words = [word.strip() + (' WORD_BOUNDARY' if self.keep_word_boundaries else ' ') for word in words]
        line = ' '.join(words)
        return line
    
    def _post_process_line(self, line):
        """ 
        Applies post-processing to the transcribed line.

        This method moves tone markers to the correct position for Mandarin and Cantonese.

        Args:
            line (str): A transcribed line to post-process.

        Returns:
            str: The post-processed line with tone markers correctly positioned.
        """
        line = super()._post_process_line(line)
        if self.language in ['cmn-Hans', 'cmn-Hant', 'cmn-Latn', 'yue-Latn']:
            line = _move_tone_marker_to_after_vowel_line(line)
        return line


def _move_tone_marker_to_after_vowel_line(line):
    """ 
    Moves the tone marker from the end of a Mandarin or Cantonese syllable to directly after the vowel.

    This function ensures that the tone marker is correctly positioned for phonetic representation.

    Args:
        line (str): A line containing syllables with tone markers.

    Returns:
        str: The line with tone markers repositioned.
    """
    vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    tone_symbols = ['˥', '˧˥', '˨˩', '˥˩', '˧', '˧˩̰', '˩˧', '˨', '˧˩̰', '˩˧', '˨˧', '˨˥'] 
    last_marker = -1
    line = line.split(' ')
    for i in range(len(line)):
        if line[i] in tone_symbols:
            for j in range(i-1, last_marker, -1):
                if line[j] in vowel_symbols or line[j] in tone_symbols:
                    line[j+1], line[i] = line[i], line[j+1]
                    break
            last_marker = i
    line = ' '.join(line)
    # Combine tone markers with previous vowel
    for tone in tone_symbols:
        line = line.replace(' ' + tone, tone)
    return line
