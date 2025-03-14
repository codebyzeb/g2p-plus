""" Convert orthographic text to a stream of IPA phonemes. """

from src.wrappers.epitran_wrapper import EpitranWrapper
from src.wrappers.phonemizer_wrapper import PhonemizerWrapper
from src.wrappers.pingyam_wrapper import PingyamWrapper
from src.wrappers.pinyin_to_ipa_wrapper import PinyinToIpaWrapper

WRAPPER_BACKENDS = {
    'epitran': EpitranWrapper,
    'phonemizer': PhonemizerWrapper,
    'pingyam': PingyamWrapper,
    'pinyin_to_ipa': PinyinToIpaWrapper,
}

def phonemize_utterances(lines, backend, language, keep_word_boundaries, verbose=False, use_folding=True, **wrapper_kwargs):
    """ Phonemizes lines using a specified wrapper and language.

    Args:
        lines (list of str): The lines to phonemize.
        backend (str): The backend to use for phonemization.
        language (str): The language to phonemize.
        keep_word_boundaries (bool): Whether to keep word boundaries.
        verbose (bool): Whether to print debug information.
        use_folding (bool): Whether to use folding dictionaries to correct the wrapper's output.
        **wrapper_kwargs: Additional keyword arguments.
    
    Returns:
        list of str: The phonemized lines.

    Raises:
        ValueError: If the backend is not supported.
        ValueError: If the language is not supported by the backend.
        ValueError: If an argument is not supported by the wrapper.
        ValueError: If an argument is not the correct type.

    The returned list will be the same length as `lines`. Each line will be a string of space-separated IPA phonemes,
    with 'WORD_BOUNDARY' separating words if keep_word_boundaries=True. Lines that could not be phonemized are returned as empty strings.

    E.g:
    Input: ['hello there!', 'this is a test.']
    Output: ['h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY', 'ð ɪ s WORD_BOUNDARY ɪ z WORD_BOUNDARY ə WORD_BOUNDARY t ɛ s t WORD_BOUNDARY']
    """

    if backend not in WRAPPER_BACKENDS:
        raise ValueError(f'Backend "{backend}" not supported. Supported backends: {list(WRAPPER_BACKENDS.keys())}')
    wrapper = WRAPPER_BACKENDS[backend](language=language, keep_word_boundaries=keep_word_boundaries, verbose=verbose, use_folding=use_folding, **wrapper_kwargs)
    return wrapper.phonemize(lines)

def character_split_utterances(lines):
    """ Used to split a line of orthographic text into characters separated by spaces.
    The resulting representation is similar to what is produced by phonemize_utterance, facilitating comparison.

    E.g:
    Input: ['hello there!', 'this is a test.']
    Output: ['h e l l o  WORD_BOUNDARY t h e r e WORD_BOUNDARY !', 't h i s  WORD_BOUNDARY i s  WORD_BOUNDARY a  WORD_BOUNDARY t e s t  WORD_BOUNDARY .']

    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip())]) + ' WORD_BOUNDARY' for line in lines]

def main():
    import argparse
    import sys

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

    parser = argparse.ArgumentParser(description="Phonemize utterances using a specified backend and language.", formatter_class=CustomHelpFormatter)
    parser.add_argument("backend", choices=WRAPPER_BACKENDS.keys(), help="The backend to use for phonemization.")
    parser.add_argument("language", help="The language to phonemize.")
    parser.add_argument("-k", "--keep-word-boundaries", action="store_true", help="Keep word boundaries in the output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print debug information.")
    parser.add_argument("-u", "--uncorrected", action="store_false", help="Use the wrapper's output without applying a folding dictionary to correct the phoneme sets.")
    parser.add_argument("-i", "--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Input file containing utterances (one per line). If not specified, reads from stdin.")
    parser.add_argument("-o", "--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Output file for phonemized utterances. If not specified, writes to stdout.")
    
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
        phonemized_lines = phonemize_utterances(
            lines,
            args.backend,
            args.language,
            args.keep_word_boundaries,
            args.verbose,
            args.uncorrected,
            **wrapper_kwargs
        )
        
        for line in phonemized_lines:
            args.output_file.write(line + '\n')
    
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()





