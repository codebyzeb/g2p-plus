""" Wrapper for the phonemizer library. """

import os
import re
import subprocess

from epitran import Epitran

from .wrapper import Wrapper
from ..dicts import FOLDING_EPITRAN
from ..utils import move_tone_marker_to_after_vowel_line

class EpitranWrapper(Wrapper):

    # TODO: Check support from epitran library instead of hardcoding.
    # See https://github.com/dmort27/epitran#language-support
    SUPPORTED_LANGUAGES = ['aar-Latn', 'aii-Syrc', 'amh-Ethi', 'amh-Ethi-pp', 'amh-Ethi-red', 'ara-Arab', 'ava-Cyrl', 'aze-Cyrl', 'aze-Latn', 'ben-Beng', 'ben-Beng-red', 'bxk-Latn', 'cat-Latn', 'ceb-Latn', 'ces-Latn', 'cjy-Latn', 'cmn-Hans', 'cmn-Hant', 'cmn-Latn', 'ckb-Arab', 'csb-Latn', 'deu-Latn', 'deu-Latn-np', 'deu-Latn-nar', 'eng-Latn', 'epo-Latn', 'fas-Arab', 'fra-Latn', 'fra-Latn-np', 'fra-Latn-p', 'ful-Latn', 'gan-Latn', 'got-Latn', 'hak-Latn', 'hau-Latn', 'hin-Deva', 'hmn-Latn', 'hrv-Latn', 'hsn-Latn', 'hun-Latn', 'ilo-Latn', 'ind-Latn', 'ita-Latn', 'jam-Latn', 'jav-Latn', 'kaz-Cyrl', 'kaz-Cyrl-bab', 'kaz-Latn', 'kbd-Cyrl', 'khm-Khmr', 'kin-Latn', 'kir-Arab', 'kir-Cyrl', 'kir-Latn', 'kmr-Latn', 'kmr-Latn-red', 'kor-Hang', 'lao-Laoo', 'lij-Latn', 'lsm-Latn', 'ltc-Latn-bax', 'mal-Mlym', 'mar-Deva', 'mlt-Latn', 'mon-Cyrl-bab', 'mri-Latn', 'msa-Latn', 'mya-Mymr', 'nan-Latn', 'nan-Latn-tl', 'nld-Latn', 'nya-Latn', 'ood-Lat-alv', 'ood-Latn-sax', 'ori-Orya', 'orm-Latn', 'pan-Guru', 'pol-Latn', 'por-Latn', 'quy-Latn', 'ron-Latn', 'run-Latn', 'rus-Cyrl', 'sag-Latn', 'sin-Sinh', 'sna-Latn', 'som-Latn', 'spa-Latn', 'spa-Latn-red', 'sqi-Latn', 'srp-Latn', 'swa-Latn', 'swa-Latn', 'swe-Latn', 'tam-Taml-red', 'tam-Taml', 'tel-Telu', 'tgk-Cyrl', 'tgl-Latn-red', 'tgl-Latn', 'tha-Thai', 'tir-Ethi', 'tir-Ethi-pp', 'tir-Ethi-red', 'tpi-Latn', 'tuk-Cyrl', 'tuk-Latn', 'tur-Latn', 'tur-Latn-bab', 'tur-Latn-red', 'ukr-Cyrl', 'urd-Arab', 'uig-Arab', 'uzb-Cyrl', 'uzb-Latn', 'vie-Latn', 'wuu-Latn', 'xho-Latn', 'yor-Latn', 'yue-Latn', 'zha-Latn', 'zul-Latn']
    CEDICT = os.path.join(os.path.dirname(__file__), '../../data/cedict_ts.u8')

    @staticmethod
    def supported_languages_message():
        message = 'The EpitranWrapper uses the epitran library, which supports multiple backends.\n'
        message += 'For a list of supported languages, see https://github.com/dmort27/epitran#language-support\n'
        return message

    def __init__(self, language, keep_word_boundaries=True, verbose=False, use_folding=True, **wrapper_kwargs):
        super().__init__(language, keep_word_boundaries, verbose, use_folding, **wrapper_kwargs)
        self.norm_punc = False
        self.ligatures = False
        self.epi = Epitran(self.language, tones=True, cedict_file=self.CEDICT, ligatures=self.ligatures)
        
    def check_language_support(self, language):
        """ Checks if the language is supported by the wrapper. """
        
        if language in self.SUPPORTED_LANGUAGES:
            if 'cmn-' in language:
                if os.path.exists(self.CEDICT):
                    self.logger.debug(f'CEDICT found at {self.CEDICT}.')
                else:
                    self.logger.error(f'CEDICT not found at {self.CEDICT}. Please download the CC_CEDICT file from https://www.mdbg.net/chinese/dictionary?page=cedict and place it in {os.path.dirname(self.CEDICT)}.')
                    return False
            elif language == 'eng-Latn':
                # Try running lex_lookup on the system
                try:
                    subprocess.run(['lex_lookup', 'hello'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    self.logger.error('Epitran requires Flite to be installed. Please install Flite and ensure that lex_lookup is in your system PATH. Instructions at https://github.com/dmort27/epitran#installation-of-flite-for-english-g2p')
                    return False
            return True
        return False

    def phonemize(self, lines):
        """ Uses epitram to phonemize text. Returns a list of phonemized lines. Lines that could not be phonemized are returned as empty strings."""

        self.logger.debug(f'Using epitram backend with language code "{self.language}"...')
        
        phonemized_lines = []
        for line in lines:
            # Replace duplicate whitespace with single space and strip punctuation
            line = re.sub(r'\s+', ' ', line).strip()
            line = re.sub(r'[^\w\s]', '', line)

            if self.language == 'yue-Latn':
                line = self._phonemize_yue_latn(line)
            else:
                line = self.epi.trans_delimiter(line + ' ', delimiter='PHONE_BOUNDARY', normpunc=self.norm_punc, ligatures=self.ligatures)
                line = line.replace('PHONE_BOUNDARY ', ' WORD_BOUNDARY' if self.keep_word_boundaries else '')
                line = line.replace('WORD_BOUNDARY WORD_BOUNDARY', 'WORD_BOUNDARY')
                line = line.replace('PHONE_BOUNDARY', ' ')
            phonemized_lines.append(line)

        if self.use_folding:
            phonemized_lines = self._post_process_epitran_output(phonemized_lines)
        else:
            self.logger.debug("Skipping folding dictionary post-processing, using uncorrected output from epitran.")

        return phonemized_lines
    
    def _phonemize_yue_latn(self, line):
        # For Cantonese, there is a bug in epitran that causes it not to recognise tone marks
        # unless they are at the end of the word, so we must split the word by syllable.
        words = [word for word in line.split()]
        words = [re.sub(r'\d', lambda x: x.group() + '_', word) for word in words]
        words = [word.split('_')[:-1] for word in words]
        words = [[self.epi.trans_delimiter(syll, normpunc=self.norm_punc, ligatures=self.ligatures).strip() for syll in word] for word in words]
        words = [' '.join(word) for word in words]
        words = [word.strip() + (' WORD_BOUNDARY' if self.keep_word_boundaries else ' ') for word in words]
        line = ' '.join(words)
        return line

    def _post_process_epitran_output(self, lines):
        """ Removes phone boundary markers, adds word boundary markers, removes extra spaces and corrects general espeak output. """

        if self.language not in FOLDING_EPITRAN:
            self.logger.debug(f'No folding dictionary found for language code: "{self.language}".')
        else:
            self.logger.debug(f'Applying folding dictionary for language code: "{self.language}".')

        for i in range(len(lines)):
            if lines[i] == '' or lines[i] == ' ':
                continue
            for key, value in FOLDING_EPITRAN['all'].items():
                lines[i] = lines[i].replace(key, value)
            if self.language in FOLDING_EPITRAN:
                lines[i] = ' ' + lines[i] + ' ' # For matching folding dictionary items that end or start with a space
                for key, value in FOLDING_EPITRAN[self.language].items():
                    lines[i] = lines[i].replace(key, value)
                lines[i] = lines[i].strip()
            if self.language in ['cmn-Hans', 'cmn-Hant', 'cmn-Latn', 'yue-Latn']:
                lines[i] = move_tone_marker_to_after_vowel_line(lines[i])

        return lines
