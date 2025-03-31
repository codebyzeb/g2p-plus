"""Command-line interface and core functions for G2P+ (Grapheme-to-Phoneme Plus).

This module provides the main functionality for converting text (graphemes) to 
phonetic transcriptions using various G2P backends. It includes:

- transcribe_utterances(): Core function for converting text to phonemes
- character_split_utterances(): Utility for character-level text splitting
- Command-line interface for easy text-to-phoneme conversion

The module supports multiple G2P backends (e.g., Epitran, Phonemizer) and languages,
with configurable options for word boundaries and phoneme set normalization.

Example Usage:
    >>> from g2p_plus.main import transcribe_utterances
    >>> text = ['hello there!']
    >>> phonemes = transcribe_utterances(text, 'phonemizer', 'en-us', True)
    >>> print(phonemes[0])
    'h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY'
"""

import argparse
import sys

from g2p_plus.wrappers import WRAPPER_BACKENDS

def transcribe_utterances(lines, backend, language, keep_word_boundaries, verbose=False, use_folding=True, **wrapper_kwargs):
    """ Transcribes text lines into phonetic transcriptions using a specified backend.

    Args:
        lines (list of str): Lines of text to convert to phonemes.
        backend (str): The G2P backend to use (e.g. 'epitran', 'espeak').
        language (str): Language code for transcription (format depends on backend).
        keep_word_boundaries (bool): If True, inserts 'WORD_BOUNDARY' between words.
        verbose (bool, optional): Print debug information. Defaults to False.
        use_folding (bool, optional): Apply folding dictionaries to normalize phoneme sets. Defaults to True.
        **wrapper_kwargs: Additional backend-specific arguments.
    
    Returns:
        list of str: Transcribed lines, where each line contains space-separated IPA phonemes.
            Words are separated by 'WORD_BOUNDARY' if keep_word_boundaries=True.
            Lines that fail to transcribe are returned as empty strings.

    Raises:
        ValueError: If backend is not supported
        ValueError: If language is not supported by the backend
        ValueError: If wrapper_kwargs contains invalid arguments
        ValueError: If arguments have incorrect types

    Examples:
        >>> lines = ['hello there!']
        >>> transcribe_utterances(lines, 'phonemizer', 'en-us', True)
        ['h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY']
    """

    if backend not in WRAPPER_BACKENDS:
        raise ValueError(f'Backend "{backend}" not supported. Supported backends: {list(WRAPPER_BACKENDS.keys())}')
    wrapper = WRAPPER_BACKENDS[backend](language=language, keep_word_boundaries=keep_word_boundaries, verbose=verbose, use_folding=use_folding, **wrapper_kwargs)
    return wrapper.process(lines)

def character_split_utterances(lines):
    """ Splits text lines into space-separated characters with word boundaries.

    This function provides a character-level representation that mirrors the format
    of transcribed output, making it useful for alignment and comparison tasks.

    Args:
        lines (list of str): Lines of text to split into characters.

    Returns:
        list of str: Lines split into space-separated characters with 'WORD_BOUNDARY'
            markers between words and at the end of each line.

    Examples:
        >>> lines = ['hello there!']
        >>> character_split_utterances(lines)
        ['h e l l o WORD_BOUNDARY t h e r e ! WORD_BOUNDARY']
    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip())]) + ' WORD_BOUNDARY' for line in lines]

def main():
    """ Command-line interface for text-to-phoneme conversion.
    
    Reads text from stdin or a file, converts it to phonemes using the specified
    backend and language, and writes the results to stdout or a file.

    Command-line Arguments:
        backend: The G2P backend to use
        language: Language code for transcription
        -k/--keep-word-boundaries: Keep word boundary markers
        -v/--verbose: Print debug information
        -u/--uncorrected: Skip phoneme set normalization (folding dictionaries)
        -i/--input-file: Input file (default: stdin)
        -o/--output-file: Output file (default: stdout)
        Additional backend-specific arguments can be passed as --key=value

    Example Usage:
        python -m g2p_plus.main epitran spa-Latn -k -v < input.txt > output.txt
        python -m g2p_plus.main phonemizer en-us -i text.txt -o phonemes.txt
    """

    class CustomHelpFormatter(argparse.HelpFormatter):
        def __init__(self, prog):
            super().__init__(prog, max_help_position=40, width=80)

        # Print supported languages when --help is called
        def format_help(self):
            help_text = super().format_help()
            help_text += "\nBackends:\n"
            for backend in WRAPPER_BACKENDS.keys():
                help_text += f"\n{backend}:\n"
                wrapper_class = WRAPPER_BACKENDS[backend]
                help_text += "  " + wrapper_class.supported_languages_message().replace('\n', '\n' + ' ' * 2)
                if len(wrapper_class.KWARGS_HELP) > 0:
                    help_text += "Additional arguments:\n"
                    for key, value in wrapper_class.KWARGS_HELP.items():
                        help_text += f"    {key}: {value}\n"
            help_text += "\n\nExample usage:\n"
            help_text += "  python phonemize.py epitran --language eng-Latn --keep-word-boundaries --verbose < input.txt > output.txt\n"
            return help_text

    parser = argparse.ArgumentParser(description="Transcribe utterances using a specified backend and language.", formatter_class=CustomHelpFormatter)
    parser.add_argument("backend", choices=WRAPPER_BACKENDS.keys(), help="The backend to use for G2P transcription.")
    parser.add_argument("language", help="The language code to use for G2P conversion (specific to the backend).")
    parser.add_argument("-k", "--keep-word-boundaries", action="store_true", help="Keep word boundaries in the output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print debug information.")
    parser.add_argument("-u", "--uncorrected", action="store_false", help="Use the wrapper's output without applying a folding dictionary to correct the phoneme sets.")
    parser.add_argument("-i", "--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Input file containing utterances (one per line). If not specified, reads from stdin.")
    parser.add_argument("-o", "--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Output file for transcribed utterances. If not specified, writes to stdout.")
    
    args, unknown = parser.parse_known_args()

    # Convert remaining unknown args to wrapper_kwargs
    wrapper_kwargs = {}
    for arg in unknown:
        if arg.startswith(("--")):
            try:
                key, value = arg.strip('--').split('=')
            except ValueError:
                print(f"Error: Argument '{arg}' must be in the form '--key=value'.", file=sys.stderr)
                sys.exit(1)
            if key in WRAPPER_BACKENDS[args.backend].WRAPPER_KWARGS_TYPES:
                try:
                    wrapper_kwargs[key] = WRAPPER_BACKENDS[args.backend].WRAPPER_KWARGS_TYPES[key](value)
                except ValueError:
                    print(f"Error: Argument '{key}' must be of type {WRAPPER_BACKENDS[args.backend].WRAPPER_KWARGS_TYPES[key].__name__}. Got '{value}' instead.", file=sys.stderr)
                    sys.exit(1)

    lines = args.input_file.readlines()
    lines = [line.strip() for line in lines]

    try:
        transcribed_lines = transcribe_utterances(
            lines,
            args.backend,
            args.language,
            args.keep_word_boundaries,
            args.verbose,
            args.uncorrected,
            **wrapper_kwargs
        )
        
        for line in transcribed_lines:
            args.output_file.write(line + '\n')
    
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()





