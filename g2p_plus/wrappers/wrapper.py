""" 
Abstract base class for G2P (Grapheme-to-Phoneme) wrappers.

This module provides a base class that all G2P wrappers must inherit from.
Each wrapper implements a specific backend (like Epitran, Phonemizer, etc.) and
must follow the interface defined here.
"""

from abc import ABC, abstractmethod
import logging
import os

FOLDING_DICTS_PATH = os.path.join(os.path.dirname(__file__), '../folding')

class Wrapper(ABC):
    """
    Abstract base class that defines the interface for G2P wrappers.

    Class Attributes:
        SUPPORTED_LANGUAGES (list): List of language codes supported by this wrapper
        WRAPPER_KWARGS_TYPES (dict): Maps kwarg names to their expected types
        WRAPPER_KWARGS_DEFAULTS (dict): Maps kwargs to their default values
        KWARGS_HELP (dict): Provides help text for each supported kwarg
    """

    SUPPORTED_LANGUAGES = []
    WRAPPER_KWARGS_TYPES = {}
    WRAPPER_KWARGS_DEFAULTS = {}
    KWARGS_HELP = {}
    
    @staticmethod
    @abstractmethod
    def supported_languages_message():
        """ 
        Returns information about languages supported by this wrapper.

        Returns:
            str: A formatted string describing the supported languages and any
                relevant details about language support for this wrapper.
        """
        pass

    def __init__(self, language, keep_word_boundaries=True, verbose=False, use_folding=True, **wrapper_kwargs):
        """ 
        Initializes a new G2P wrapper instance.
        
        Args:
            language (str): The language code for transcription (e.g. 'en', 'fr')
            keep_word_boundaries (bool): If True, marks word boundaries in output
            verbose (bool): If True, enables detailed logging output
            use_folding (bool): If True, applies post-processing rules from folding dictionaries
            **wrapper_kwargs: Additional backend-specific configuration options
        
        Raises:
            ValueError: If language is not supported or if wrapper_kwargs contains
                      invalid arguments or types
        """

        self.language = language
        self.keep_word_boundaries = keep_word_boundaries
        self.use_folding = use_folding
        self.verbose = verbose
        self.backend_name = self.__class__.__name__.replace('Wrapper', '').lower()

        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.debug(f'Initializing {self.__class__.__name__} with language "{language}" and wrapper_kwargs "{wrapper_kwargs}"')
        
        if not self.check_language_support(language):
            raise ValueError(f'Language "{language}" not supported by {self.__class__.__name__}. Supported languages: {self.get_supported_languages()}')
        
        # Check if wrapper_kwargs are supported
        for key, value in wrapper_kwargs.items():
            if key not in self.WRAPPER_KWARGS_TYPES:
                raise ValueError(f'{self.__class__.__name__} does not accept the "{key}" argument. Supported arguments: {self.WRAPPER_KWARGS_TYPES}')
            if not isinstance(value, self.WRAPPER_KWARGS_TYPES[key]):
                raise ValueError(f'Argument "{key}" must be of type {self.WRAPPER_KWARGS_TYPES[key].__name__}. Got {type(value).__name__} instead.')
            setattr(self, key, value)
        
        # Set default wrapper_kwargs
        for key, value in self.WRAPPER_KWARGS_DEFAULTS.items():
            if key not in wrapper_kwargs:
                setattr(self, key, value)

        # Get folding dicts
        self.folding_dicts = self._get_folding_dictionaries()


    def process(self, lines):
        """ 
        Converts text to phonemes using the configured G2P backend.

        Args:
            lines (list[str]): List of text strings to convert to phonemes

        Returns:
            list[str]: The transcribed versions of the input lines, with each phoneme
                      separated by spaces. Empty strings indicate lines that could not
                      be processed.
        """

        transcribed_lines = self._transcribe(lines)
        for i, line in enumerate(transcribed_lines):
            if line == '' or line == ' ':
                continue
            transcribed_lines[i] = self._post_process_line(line)
        return transcribed_lines

    def check_language_support(self, language):
        """ 
        Checks if a language is supported by this wrapper.
        
        Args:
            language (str): Language code to check

        Returns:
            bool: True if the language is supported, False otherwise
        """

        if language in self.SUPPORTED_LANGUAGES:
            return True
        return False

    def get_supported_languages(self):
        """ 
        Gets the list of languages supported by this wrapper.

        Returns:
            list[str]: List of supported language codes
        """
        return self.SUPPORTED_LANGUAGES

    @abstractmethod
    def _transcribe(self, lines):
        """ 
        Core transcription method that must be implemented by each wrapper.
        
        Args:
            lines (list[str]): List of text strings to convert to phonemes
            
        Returns:
            list[str]: Transcribed versions of the input lines. Each phoneme should be
                      separated by spaces. If keep_word_boundaries is True, 'WORD_BOUNDARY'
                      should be inserted between words.

        Examples:
            With keep_word_boundaries=True:
                Input: 'hello there!'
                Output: 'h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY'

            With keep_word_boundaries=False:
                Input: 'hello there!'
                Output: 'h ə l oʊ ð ɛ ɹ'
        """
        pass

    def _post_process_line(self, line):
        """ 
        Applies folding dictionary rules to a transcribed line.

        Args:
            line (str): A transcribed line to post-process

        Returns:
            str: The post-processed line with folding rules applied
        """
        for dict in self.folding_dicts:
            line = ' ' + line + ' ' # For matching items that are at the beginning or end of the line
            for key, value in dict.items():
                line = line.replace(key, value)
            line = line.strip()
        return line

    def _get_folding_dictionaries(self):
        """
        Loads folding dictionaries for post-processing transcribed output.

        The method loads two types of dictionaries if they exist:
        1. A main dictionary for the backend (backend_name.csv)
        2. A language-specific dictionary (language_code.csv)

        Returns:
            list[dict]: List of loaded folding dictionaries, where each dictionary
                       maps patterns to their replacements
        """
        if not self.use_folding:
            self.logger.debug(f"Skipping folding dictionary post-processing, using uncorrected output from {self.backend_name}.")
            return []
        
        # Load main folding dictionary
        main_dict_path = os.path.join(FOLDING_DICTS_PATH, f'{self.backend_name}/{self.backend_name}.csv')
        if os.path.exists(main_dict_path):
            self.logger.debug(f'Found main folding dictionary for {self.backend_name} at {main_dict_path}.')
        else:
            self.logger.debug(f'No folding dictionary for {self.backend_name} found at {main_dict_path}.')
            return []
        dict_paths = [main_dict_path]

        # Load language specific dict
        lang_dict_path = os.path.join(FOLDING_DICTS_PATH, f'{self.backend_name}/{self.language}.csv')
        if os.path.exists(lang_dict_path):
            dict_paths.append(lang_dict_path)
            self.logger.debug(f'Found language-specific folding dictionary at {lang_dict_path}.')
        elif self.backend_name not in ['pinyin_to_ipa', 'pingyam']:
            self.logger.debug(f'No folding dictionary for {self.language} found at {lang_dict_path}.')

        dicts = []
        for dict_path in dict_paths:
            dict = {}
            with open(dict_path, 'r') as f:
                next(f)
                for line in f:
                    # Very important not to strip the line, as the keys may contain leading or trailing spaces
                    # which are significant for the folding process
                    line = line.replace('\n', '')
                    key, value = line.split(',')
                    dict[key] = value
            dicts.append(dict)

        return dicts