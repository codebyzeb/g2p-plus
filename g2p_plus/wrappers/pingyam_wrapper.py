""" 
Wrapper for the pingyam library for converting Cantonese Jyutping to IPA phonemes.

This wrapper utilizes the pingyam library to convert Cantonese text written in 
Jyutping romanization into International Phonetic Alphabet (IPA) notation. 
It specifically supports Cantonese language phonetic transcription.
"""

import os
import pandas as pd
import re

from g2p_plus.wrappers.wrapper import Wrapper

PINGYAM_PATH = os.path.join(os.path.dirname(__file__), '../data/pingyam/pingyambiu')

class PingyamWrapper(Wrapper):
    """
    A wrapper class for converting Cantonese Jyutping to IPA using the pingyam library.

    Class Attributes:
        SUPPORTED_LANGUAGES (list): Contains only 'cantonese' as this wrapper is
            specifically for Cantonese language.
    """

    SUPPORTED_LANGUAGES = ['cantonese']

    @staticmethod
    def supported_languages_message():
        """
        Returns a message indicating the supported language for this wrapper.

        Returns:
            str: Message indicating this wrapper only supports Cantonese.
        """
        message = 'The PingyamWrapper uses the pingyam library, which only supports `cantonese`.\n'
        return message
    
    def _transcribe(self, lines):
        """ 
        Converts Cantonese text from Jyutping to IPA phonemes using the pingyam library.

        This method processes each line of Jyutping text, converting it to IPA phonemes.
        It handles both empty lines and lines with unrecognized syllables.

        Args:
            lines (list[str]): List of Jyutping text strings to convert.

        Returns:
            list[str]: List of transcribed strings where each phoneme is separated by
                        spaces. Failed conversions return empty strings.

        Notes:
            - The method tracks the number of lines that could not be converted and logs a warning.
            - Word boundaries are added based on the `keep_word_boundaries` attribute.
        """
        broken = 0
        transcribed_utterances = []

        # Load pingyam database
        cantonese_dict = pd.read_csv(PINGYAM_PATH, sep='\t', header=None)[[5, 6]]
        cantonese_dict.columns = ['ipa', 'jyutping']
        cantonese_dict = cantonese_dict.set_index('jyutping').to_dict()['ipa']

        # Convert jyutping to IPA
        for line in lines:
            if line.strip() == '':
                transcribed_utterances.append('')
                continue
            transcribed = ''
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
                        syll = _move_tone_marker_to_after_vowel(syll)
                        transcribed += syll + ''
                transcribed += '_'
            if line_broken:
                transcribed = ''
            transcribed_utterances.append(transcribed)

        if broken > 0:
            self.logger.debug(f'WARNING: {broken} lines were not transcribed successfully by jyutping to ipa conversion.')
        
        # Separate phonemes with spaces and add word boundaries
        # The spaces between multi-character phonemes are fixed by the folding dictionary, which
        # also attaches tone markers to the vowels
        for i in range(len(transcribed_utterances)):
            transcribed_utterances[i] = ' '.join(list(transcribed_utterances[i]))
            transcribed_utterances[i] = transcribed_utterances[i].replace('_', 'WORD_BOUNDARY' if self.keep_word_boundaries else ' ')

        return transcribed_utterances
    
def _move_tone_marker_to_after_vowel(syll):
    """ 
    Moves the tone marker from the end of a Cantonese syllable to directly after the vowel.

    This function ensures that the tone marker is correctly positioned for phonetic representation.

    Args:
        syll (str): A Cantonese syllable that may contain a tone marker.

    Returns:
        str: The syllable with the tone marker repositioned.
    """
    cantonese_vowel_symbols = "eauɔiuːoɐɵyɛœĭŭiʊɪə"
    cantonese_tone_symbols = "˥˧˨˩"
    if not syll[-1] in cantonese_tone_symbols:
        print(syll, syll[-1])
        return syll
    tone_marker = len(syll) - 1
    # Iterate backwards
    for i in range(len(syll)-2, -1, -1):
        if syll[i] in cantonese_tone_symbols:
            tone_marker = i
            continue
        if syll[i] in cantonese_vowel_symbols:
            return syll[:i+1] + syll[tone_marker:] + syll[i+1:tone_marker]
    return syll